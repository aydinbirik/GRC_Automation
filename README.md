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

## Example Audit Artifact

```json
