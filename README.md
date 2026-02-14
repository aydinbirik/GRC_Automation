# GRC Automation Engine – CI/CD Compliance Guardrails

## Overview

This project demonstrates how compliance controls can be enforced directly inside CI/CD pipelines using policy-as-code and deterministic evaluation logic.

It was built as part of preparing an AI security system (PrecogX.ai) for SOC 2 and GDPR readiness by embedding compliance guardrails into engineering workflows instead of relying on manual evidence collection.

---

## Problem

Traditional compliance approaches rely on:

- Screenshots
- Manual reviews
- Spreadsheet-based tracking
- Periodic evidence gathering

This creates audit drift, human error, and delayed detection of control violations.

Modern cloud-native environments require compliance to be automated and embedded directly into development pipelines.

---

## Solution

This repository implements a lightweight GRC automation engine that:

- Defines controls as YAML policy-as-code
- Evaluates pull request events deterministically
- Validates actors against allowlists and identity status
- Generates structured audit artifacts
- Fails CI/CD jobs when controls are violated
- Uploads evidence artifacts even on failure

Compliance becomes proactive and enforced — not reactive.

---

## Controls Implemented

### SOC 2

- **CC6.1 – Logical Access Control**
  - Pull request actors must be allowlisted
  - Actor must be ACTIVE in identity system
  - Noncompliant changes are blocked automatically

### GDPR-lite Mapping

- **Article 5 – Data Governance Principles (conceptual alignment)**
- **Article 32 – Security of Processing (artifact integrity & secure handling model)**

---

## Architecture

Policy (YAML)  
↓  
Signal Collection (GitHub + Okta JSON)  
↓  
Evaluator Engine (Python)  
↓  
CLI Interface  
↓  
GitHub Actions (CI/CD Enforcement)  
↓  
Audit Artifact (JSON)

---

### Example Audit Artifact

```json
{
  "artifact_version": "1.0",
  "generated_at_epoch": 1771101345,
  "event_type": "pull_request",
  "repo": "precogx-backend",
  "actor": "alice@company.com",
  "control_id": "CC6.1",
  "result": "PASS",
  "reason": "Actor is allowlisted and ACTIVE"
}

---

## How Enforcement Works

1. A pull request is opened.
2. GitHub Actions triggers automatically.
3. The compliance engine evaluates control CC6.1.
4. If noncompliant:
   - The job fails.
   - The PR is blocked (if branch protection is enabled).
   - Audit artifact is still uploaded.
5. If compliant:
   - Job passes.
   - PR may proceed.

### Exit Code Behavior

- `0` → PASS  
- `1` → FAIL  

This enables deterministic CI enforcement.

---

## Capabilities Demonstrated

- Policy-as-Code (YAML control definitions)
- Deterministic control evaluation
- Identity validation logic
- CI/CD compliance gate
- Automated audit artifact generation
- Structured evidence format
- Exit-code driven enforcement
- GitHub Actions integration

---

## Differentiation from Traditional GRC Platforms

Platforms such as Vanta and Drata primarily focus on evidence aggregation and audit workflow management.

This project demonstrates enforcement-first compliance:

- Controls are evaluated at execution time.
- Violations are blocked automatically.
- Evidence is generated programmatically.
- Compliance logic is embedded in engineering workflows.

This approach reduces manual effort, improves control reliability, and strengthens audit defensibility.

---

## Project Context

This engine was designed as part of preparing an AI security platform (PrecogX.ai) for SOC 2 and GDPR readiness by embedding compliance guardrails directly into development workflows.

It is intentionally lightweight, deterministic, and automation-focused.
