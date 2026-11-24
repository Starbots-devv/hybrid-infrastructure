"""Deterministic, in-memory worker-loss drill; never a queue or database adapter."""

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Lease:
    job_id: str
    attempt: int
    worker: str
    expires_at: int


class LocalRecoveryDrill:
    """Model lease expiry, bounded admission, and one committed effect per job ID."""

    def __init__(self, *, queue_limit: int, lease_seconds: int, fallback_enabled: bool):
        if queue_limit < 1 or lease_seconds < 1:
            raise ValueError("Queue limit and lease duration must be positive")
        self.queue_limit = queue_limit
        self.lease_seconds = lease_seconds
        self.fallback_enabled = fallback_enabled
        self.now = 0
        self.local_available = True
        self.backpressure_rejections = 0
        self.effects: dict[str, str] = {}
        self._pending = deque()
        self._leased: dict[str, Lease] = {}
        self._payloads: dict[str, str] = {}
        self._attempts: dict[str, int] = {}

    @property
    def queue_depth(self) -> int:
        return len(self._pending) + len(self._leased)

    def submit(self, job_id: str, payload: str) -> bool:
        if not job_id or job_id in self._payloads:
            raise ValueError("Job IDs must be nonempty and unique")
        if self.queue_depth >= self.queue_limit:
            self.backpressure_rejections += 1
            return False
        self._payloads[job_id] = payload
        self._attempts[job_id] = 0
        self._pending.append(job_id)
        return True

    def lease(self, worker: str) -> Lease | None:
        if worker not in ("local", "cloud"):
            raise ValueError("The drill supports local and cloud worker labels only")
        if (worker == "local" and not self.local_available) or (worker == "cloud" and not self.fallback_enabled):
            return None
        if not self._pending:
            return None
        job_id = self._pending.popleft()
        attempt = self._attempts[job_id] + 1
        self._attempts[job_id] = attempt
        lease = Lease(job_id, attempt, worker, self.now + self.lease_seconds)
        self._leased[job_id] = lease
        return lease

    def commit(self, lease: Lease, effect: str) -> bool:
        self._require_live(lease)
        if lease.job_id in self.effects:
            return False
        self.effects[lease.job_id] = effect
        return True

    def ack(self, lease: Lease) -> None:
        self._require_live(lease)
        del self._leased[lease.job_id]

    def fail_local(self) -> None:
        self.local_available = False

    def advance(self, seconds: int) -> None:
        if seconds < 0:
            raise ValueError("Time cannot move backward")
        self.now += seconds
        expired = [lease for lease in self._leased.values() if lease.expires_at <= self.now]
        for lease in reversed(expired):
            del self._leased[lease.job_id]
            self._pending.appendleft(lease.job_id)

    def _require_live(self, lease: Lease) -> None:
        if self._leased.get(lease.job_id) != lease or lease.expires_at <= self.now:
            raise ValueError("Only the current unexpired lease can commit or acknowledge")
