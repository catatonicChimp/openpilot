# ValidationPackage

The expansion of `[ValidationPackage]` (inside system `EngineeringPlan`).

Interface hash `df0d1aeee32c1ab6` · body hash `60fab2c641b7eda0`.

## Components

- `[AcceptanceDispatch]` (service) — [acceptancedispatch.md](acceptancedispatch.md)
- `[EvaluateCandidate]` (service) — [evaluatecandidate.md](evaluatecandidate.md)
- `[ValidationBlock]` (service) — [validationblock.md](validationblock.md)

## Boundary

The flows that cross into or out of this system: its contract.

- `[AcceptanceDispatch] -> [DecisionRecord] : {AcceptedEvidence}` — sync call
- `[ValidationBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call
- `{CandidateBundle} -> [ValidationPackage] : {CandidateBundle} => {ValidationDecision}` — sync call
- `[EvaluateCandidate] => {ValidationDecision}` — return

## Control blocks

- branch `{ValidationDecision}.status`

## Depends on

- `EngineeringPlan` — [engineeringplan/](../engineeringplan/README.md)
