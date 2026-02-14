import argparse
import json
import sys
from pathlib import Path

from controlops.evaluator import (
    BASE_DIR,
    evaluate_cc6_1,
    generate_audit_artifact,
    load_json,
    load_yaml,
)


def main() -> None:
    parser = argparse.ArgumentParser(prog="controlops")
    parser.add_argument("--github", default=str(BASE_DIR / "sample_data" / "github_event.json"))
    parser.add_argument("--okta", default=str(BASE_DIR / "sample_data" / "okta_users.json"))
    parser.add_argument("--soc2", default=str(BASE_DIR / "policies" / "soc2.yaml"))
    parser.add_argument("--out", default=str(BASE_DIR / "artifacts" / "audit_artifact.json"))
    args = parser.parse_args()

    print("[controlops] Using inputs:")
    print(f"  soc2:   {args.soc2}")
    print(f"  github: {args.github}")
    print(f"  okta:   {args.okta}")
    print(f"  out:    {args.out}\n")

    soc2_policy = load_yaml(args.soc2)
    github_event = load_json(args.github)
    okta_data = load_json(args.okta)

    print(f"[controlops] Loaded GitHub actor: {github_event.get('actor')}")

    decision = evaluate_cc6_1(soc2_policy, github_event, okta_data)
    artifact = generate_audit_artifact(decision, github_event)

    out_path = Path(args.out)
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    print(json.dumps(decision, indent=2))
    print(f"\n[controlops] Overall: {decision['result']}")
    print(f"Artifact written: {out_path}")

    if decision["result"] != "PASS":
        print("[controlops] Noncompliant -> exiting with code 1")
        sys.exit(1)


if __name__ == "__main__":
    main()