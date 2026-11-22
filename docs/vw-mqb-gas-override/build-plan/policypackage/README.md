# PolicyPackage

The expansion of `[PolicyPackage]` (inside system `EngineeringPlan`).

Interface hash `0a08df5efeeb1698` · body hash `76de035440ea60b2`.

## Components

- `[EvaluateReadiness]` (service) — [evaluatereadiness.md](evaluatereadiness.md)

## Boundary

The flows that cross into or out of this system: its contract.

- `[EvidencePackage] -> [PolicyPackage] : {EvidenceBundle} => {PolicyDecision}` — sync call
- `[EvaluateReadiness] => {PolicyDecision}` — return

## Depends on

- `EngineeringPlan` — [engineeringplan/](../engineeringplan/README.md)
