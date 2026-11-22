# EvidencePackage

The expansion of `[EvidencePackage]` (inside system `EngineeringPlan`).

Leaf responsibilities are bounded offline work packages, not network services. Each result includes a manifest and citations; unavailable inputs yield blockers.

Interface hash `c6efffdd78ca4b0f` · body hash `55fd704f57efd89c`.

## Components

- `[AssembleEvidence]` (service) — [assembleevidence.md](assembleevidence.md)

## Boundary

The flows that cross into or out of this system: its contract.

- `[EvidencePackage] -> [PolicyPackage] : {EvidenceBundle} => {PolicyDecision}` — sync call
- `[AssembleEvidence] => {EvidenceBundle}` — return

## Depends on

- `EngineeringPlan` — [engineeringplan/](../engineeringplan/README.md)
- `PolicyPackage` — [policypackage/](../policypackage/README.md)
