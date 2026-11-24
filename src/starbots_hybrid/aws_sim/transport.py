"""Closed in-memory subset of STS/SQS, with no SDK or network imports."""
from copy import deepcopy

from ..io import digest, fail, json_bytes


class SimulatedTimeout(TimeoutError):
    pass


class InMemorySQS:
    def __init__(self, *, account_id, region):
        self.account_id = account_id
        self.region = region
        self.queues = {}
        self.reads = []
        self.mutations = []
        self.fault = None
        self._read_budget = None
        self._read_count = 0

    def begin_read_budget(self, limit):
        self._read_budget = limit
        self._read_count = 0

    def _read(self, operation):
        if self._read_budget is not None and self._read_count >= self._read_budget:
            fail('QUERY_BUDGET', 'Simulated SQS read budget exhausted')
        self._read_count += 1
        self.reads.append(operation)

    def get_caller_identity(self):
        self._read('GetCallerIdentity')
        return {'account_id': self.account_id}

    def get_queue_url(self, name):
        self._read('GetQueueUrl')
        return f'synthetic://sqs/{self.region}/{name}' if name in self.queues else None

    def get_queue_attributes(self, name):
        self._read('GetQueueAttributes')
        return deepcopy(self.queues[name]['attributes'])

    def list_queue_tags(self, name):
        self._read('ListQueueTags')
        return deepcopy(self.queues[name]['tags'])

    def state_digest(self, name):
        queue = self.queues.get(name)
        return digest(json_bytes({'exists': queue is not None, 'queue': queue}))

    def create_queue(self, *, name, attributes, tags):
        if self.fault == 'before_effect_timeout':
            raise SimulatedTimeout('synthetic timeout before effect')
        if name in self.queues:
            fail('DRIFT_DETECTED', 'Queue already exists')
        self.mutations.append('CreateQueue')
        self.queues[name] = {'attributes': deepcopy(attributes), 'tags': deepcopy(tags)}
        if self.fault == 'after_effect_timeout':
            raise SimulatedTimeout('synthetic timeout after effect')
        if self.fault == 'postcondition_mismatch':
            self.queues[name]['attributes']['VisibilityTimeout'] = '31'
        return f'synthetic://sqs/{self.region}/{name}'
