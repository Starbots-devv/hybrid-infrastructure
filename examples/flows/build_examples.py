"""Build three self-contained, synthetic input bundles; no network or credentials."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "hybrid-saving"
DATE = "2026-10-17T00:00:00Z"
UNTIL = "2026-11-01T00:00:00Z"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, document):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def ref(directory, name):
    return {"path": name, "sha256": sha256((directory / name).read_bytes()).hexdigest()}


def plan(identity, scenario_id):
    return {
        "format": "starbots-finops-1",
        "scenario_id": scenario_id,
        "client_id": identity,
        "project_id": "synthetic-evaluation",
        "observed_at": DATE,
        "valid_until": UNTIL,
        "currency": "USD",
        "start_month": "2026-10",
        "tax_status": "pre_tax_unknown",
        "source_uri": f"synthetic://flows/{identity}/{scenario_id}/finops",
        "line_rules": [],
        "promotions": [],
    }


def line(template, scenario_id, resource, amount, *, view="both", period="monthly", service=None):
    result = deepcopy(template)
    result.update(
        id=resource,
        resource_id=resource,
        allocation_id=resource,
        quantity="1",
        unit="one_time" if period == "one_time" else "month",
        unit_rate=str(amount),
        period=period,
        view=view,
        service=service or resource.replace("-", " ").title(),
        source={"uri": f"synthetic://flows/{scenario_id}/{resource}", "label": "Synthetic fixture assumption; no vendor quote"},
        assumptions=["Nominal USD, no FX or inflation; tax UNKNOWN.", "Explicit synthetic full-cost allocation."],
    )
    return result


def node(template, resource, service):
    result = deepcopy(template)
    result.update(id=resource, role=service, service=service, provider="Synthetic architecture model")
    return result


def make_flow(number, identity, title, baseline_lines, proposal_lines, investment, proposal_id, *, tco_extra=0, description):
    directory = ROOT / f"flow-{number:02d}"
    profile = read(SOURCE / "profile.json")
    profile.update(id=f"{identity}-profile", client_id=identity, project_id="synthetic-evaluation")
    pp = profile["payload"]
    pp["company_name"] = title + " — fictional organization"
    pp["current_system"]["description"] = description
    pp["current_system"]["resource_ids"] = [item[0] for item in baseline_lines]
    pp["inventory"] = [node(profile["payload"]["inventory"][0], resource, service) for resource, _, service in baseline_lines]
    pp["goals"] = ["Compare complete 12- and 36-month synthetic costs before changing architecture", "Retain a managed data source and demonstrate recovery independently"]
    pp["commercial"]["monthly_budget"] = "900"
    pp["commercial"]["horizon_months"] = 36
    pp["workloads"][0]["assumptions"] = ["One synthetic request or job per second; service time is unmeasured.", "No conversion from users to requests; retry amplification needs a load test."]
    if number != 1:
        pp["workloads"][0]["id"] = "api-requests"
        pp["workloads"][0]["kind"] = "api"
    write(directory / "profile.json", profile)
    profile_ref = ref(directory, "profile.json")

    scenario_refs = []
    finops_refs = {}
    cases = [
        ("current", "current", baseline_lines),
        (proposal_id, "hybrid", proposal_lines),
    ]
    if number == 1:
        cases.append(("local-only", "local-only", [
            ("compute", 30, "Local worker and queue"), ("db", 20, "Local database"),
            ("network", 20, "Local network"), ("observability", 10, "Monitoring"),
            ("power", 30, "Power"), ("operations", 40, "Operations labor"),
        ]))
    for scenario_id, scenario_source, items in cases:
        is_proposal = scenario_id == proposal_id
        scenario = read(SOURCE / f"scenario-{scenario_source}.json")
        scenario.update(id=scenario_id, client_id=identity, project_id="synthetic-evaluation")
        sp = scenario["payload"]
        sp["subject_revision"] = f"{identity}-synthetic-v1"
        sp["demand_case"] = description
        sp["required_capacity_profile_digest"] = profile_ref["sha256"]
        if not is_proposal:
            sp["resource_nodes"] = [node(sp["resource_nodes"][0], rid, service) for rid, _, service in items]
        else:
            sp["resource_nodes"] = [node(sp["resource_nodes"][0], rid, service) for rid, _, service in items]
            if number != 3:
                sp["resource_nodes"].append(node(sp["resource_nodes"][0], "local-worker", "Optional local worker host"))
        sp["action_groups"] = [{"resource_id": entry["id"], "actions": ["keep"]} for entry in sp["resource_nodes"]]
        # Local, explicit edges. Endpoint resolution and TLS remain required inputs.
        edge = deepcopy(sp["connection_edges"][0])
        edge.update(source=sp["resource_nodes"][0]["id"], destination=sp["resource_nodes"][1]["id"])
        edge["cost_line_ids"] = ["network"] if any(rid == "network" for rid, _, _ in items) else [items[1][0]]
        if number == 3 and is_proposal:
            edge.update(protocol="HTTPS", port=443, id="vm-network")
            edge["permissions"] = ["Egress only to approved backup or application endpoint"]
        sp["connection_edges"] = [edge]
        if is_proposal and number != 3:
            worker_edge = deepcopy(edge)
            worker_edge.update(id="local-worker-queue", source="local-worker", destination="compute", protocol="HTTPS", port=443, trust_boundary="Local-to-cloud")
            sp["connection_edges"].append(worker_edge)
            if any(rid == "db" for rid, _, _ in items):
                db_edge = deepcopy(edge)
                db_edge.update(id="local-worker-db", source="local-worker", destination="db", protocol="PostgreSQL over TLS", port=5432, trust_boundary="Local-to-cloud")
                sp["connection_edges"].append(db_edge)
        sp["failure_domains"][0]["resource_ids"] = ["local-worker"] if is_proposal and number != 3 else [sp["resource_nodes"][0]["id"]]
        sp["capacity_inputs"]["assumptions"] = ["Synthetic steady-state slots and two-second service time; no measured benchmark.", "Retry bursts, I/O ceilings and tail latency require separate tests."]
        if scenario_id == "local-only":
            sp["operational_model"]["fallback"] = "No independent fallback is modeled; local power and network are one failure domain."
        elif is_proposal and number != 3:
            sp["operational_model"]["fallback"] = "Retain the durable cloud queue and restore managed consumers; cloud fallback is included in the proposed cost."
        else:
            sp["operational_model"]["fallback"] = "Retain the current managed service until a separately tested recovery path exists."
        if number == 2 and is_proposal:
            sp["trust_boundaries"] = ["Optional local worker", "Managed SaaS/API", "Managed database"]
            sp["operational_model"]["alerts"].extend(["Transfer volume and egress", "Fallback capacity"])
        if number == 3 and is_proposal:
            sp["trust_boundaries"] = ["Self-managed VM", "Managed backup endpoint"]
            sp["operational_model"]["fallback"] = "Remain on the managed service until VM backup, patching and support owners are verified."
            sp["implementation_steps"][2]["required_inputs"].extend(["Named VM patching owner", "Tested backup retention", "Managed feature replacement inventory"])
            sp["migration_rollback"]["data_state"] = "Managed application remains authoritative until a consistent snapshot, replay boundary, and VM restore test are independently verified."
            sp["migration_rollback"]["cutover"] = "Use a separately approved maintenance window only after backup, feature parity, and rollback rehearsal."
            sp["migration_rollback"]["rollback_actions"] = ["Stop VM writes", "Reconcile accepted writes", "Resume the managed service at the reviewed boundary"]

        cost = read(SOURCE / f"prices-{scenario_source}.json")
        cost.update(id=f"prices-{scenario_id}", client_id=identity, project_id="synthetic-evaluation")
        cp = cost["payload"]
        cp["source_id"] = f"synthetic-{identity}-{scenario_id}"
        template = cp["lines"][0]
        cp["lines"] = [line(template, scenario_id, rid, amount, service=service) for rid, amount, service in items]
        if is_proposal and tco_extra:
            cp["lines"].append(line(template, scenario_id, "hardware", tco_extra, view="allocated_tco", service="Allocated existing hardware ownership"))
            sp["resource_nodes"].append(node(sp["resource_nodes"][0], "hardware", "Allocated existing hardware ownership"))
            sp["action_groups"].append({"resource_id": "hardware", "actions": ["keep"]})
        if is_proposal:
            cp["lines"].append(line(template, scenario_id, "migration", investment, period="one_time", service="Transition and training"))
            sp["resource_nodes"].append(node(sp["resource_nodes"][0], "migration", "Transition and training"))
            sp["action_groups"].append({"resource_id": "migration", "actions": ["keep"]})
        price_name = f"prices-{scenario_id}.json"
        write(directory / price_name, cost)
        sp["input_cost_snapshot_refs"] = [ref(directory, price_name)]
        scenario_name = f"scenario-{scenario_id}.json"
        write(directory / scenario_name, scenario)
        scenario_refs.append(ref(directory, scenario_name))
        plan_name = f"finops-{scenario_id}.json"
        write(directory / plan_name, plan(identity, scenario_id))
        finops_refs[scenario_id] = ref(directory, plan_name)

    write(directory / "bundle.json", {
        "schema_version": "1.1.0", "client_id": identity, "project_id": "synthetic-evaluation",
        "profile": profile_ref, "scenarios": scenario_refs, "baseline_id": "current",
        "security_assessments": [], "finops": finops_refs,
    })


def build():
    make_flow(1, "synthetic-northstar-parts", "Northstar Parts", [
        ("compute", 320, "Cloud workers and durable queue"), ("db", 100, "Managed database"),
        ("network", 80, "Network and egress"), ("observability", 40, "Monitoring and security"),
        ("operations", 180, "Operations labor"),
    ], [
        ("compute", 100, "Cloud control and fallback"), ("db", 100, "Managed database"),
        ("network", 50, "Network and egress"), ("observability", 40, "Monitoring and security"),
        ("power", 50, "Local power and connectivity"), ("operations", 160, "Operations labor"),
    ], 1200, "hybrid", tco_extra=40, description="Recoverable asynchronous jobs; managed database stays in cloud; local worker has cloud fallback")
    make_flow(2, "synthetic-hidden-costs", "Cedar API", [
        ("compute", 220, "Managed SaaS/API compute"), ("db", 100, "Managed database"),
        ("network", 60, "Network"), ("observability", 40, "Monitoring and security"),
        ("operations", 100, "Operations labor"),
    ], [
        ("compute", 120, "Optional local worker and API compute"), ("db", 100, "Managed database"),
        ("network", 30, "Base network"), ("observability", 40, "Monitoring and security"),
        ("transfer", 110, "Data transfer and egress"), ("operations", 80, "Additional operations labor"),
        ("power", 65, "Power and replacement reserve"), ("fallback", 75, "Cloud fallback"),
    ], 400, "hidden-costs", description="Managed SaaS/API with database and optional worker; full transfer, operations, power, and fallback cost")
    make_flow(3, "synthetic-stay-managed", "Maple Service", [
        ("compute", 110, "Managed application"), ("db", 60, "Managed data and backup"),
        ("network", 30, "Network"), ("observability", 20, "Managed security and monitoring"),
        ("operations", 40, "Operations labor"),
    ], [
        ("compute", 120, "Self-managed VM"), ("network", 60, "Backup, network, and security"),
        ("operations", 125, "VM operations and maintenance"),
    ], 600, "vm", description="Managed application already meets modeled objectives; VM alternative transfers backup and patching responsibility")


if __name__ == "__main__":
    build()
