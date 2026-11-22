# [EvidencePackage]

Kind: service. Lives in system `EngineeringPlan` (folder `engineeringplan/`).

## Description

Leaf responsibilities are bounded offline work packages, not network services. Each result includes a manifest and citations; unavailable inputs yield blockers.

## Interface

- `[EvidencePackage] -> [PolicyPackage] : {EvidenceBundle} => {PolicyDecision}` — sync call

## Requirements

None stated.
