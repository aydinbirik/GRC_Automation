from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from typing import Any, Dict, Optional
import json
import yaml
import time




def load_yaml(path: str) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def okta_lookup_status(okta_data: Dict[str, Any], email: str) -> Optional[str]:
    for u in okta_data.get("users", []):
        if u.get("email") == email:
            return u.get("status")
    return None


def evaluate_cc6_1(soc2_policy: Dict[str, Any], github_event: Dict[str, Any], okta_data: Dict[str, Any]) -> Dict[str, Any]:
    actor = github_event.get("actor")

    allowlist = soc2_policy.get("allowlists", {}).get("repo_devs", [])
    if actor not in allowlist:
        return {
            "control_id": "CC6.1",
            "result": "FAIL",
            "reason": f"Actor '{actor}' is not in allowlist.repo_devs"
        }

    status = okta_lookup_status(okta_data, actor)
    if status != "ACTIVE":
        return {
            "control_id": "CC6.1",
            "result": "FAIL",
            "reason": f"Actor '{actor}' is not ACTIVE in Okta (status={status})"
        }

    return {
        "control_id": "CC6.1",
        "result": "PASS",
        "reason": "Actor is allowlisted and ACTIVE"
    }
def generate_audit_artifact(decision: Dict[str, Any], github_event: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_version": "1.0",
        "generated_at_epoch": int(time.time()),
        "event_type": github_event.get("event_type"),
        "repo": github_event.get("repo"),
        "actor": github_event.get("actor"),
        "control_id": decision.get("control_id"),
        "result": decision.get("result"),
        "reason": decision.get("reason")
    }


def main() -> None:
    soc2_policy = load_yaml(str(BASE_DIR / "policies" / "soc2.yaml"))
    github_event = load_json(str(BASE_DIR / "sample_data" / "github_event.json"))
    okta_data = load_json(str(BASE_DIR / "sample_data" / "okta_users.json"))

    decision = evaluate_cc6_1(soc2_policy, github_event, okta_data)
   
    artifact = generate_audit_artifact(decision, github_event)

    output_path = BASE_DIR / "artifacts"
    output_path.mkdir(exist_ok=True)

    artifact_file = output_path / "audit_artifact.json"
    artifact_file.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    print("\n=== CC6.1 Evaluation Result ===")
    print(json.dumps(decision, indent=2))

    print("\nAudit artifact written to:")
    print(str(artifact_file))


if __name__ == "__main__":
    main()