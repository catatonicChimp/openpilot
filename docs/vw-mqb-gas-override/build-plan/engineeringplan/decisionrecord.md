# [DecisionRecord]

Kind: service. Lives in system `EngineeringPlan` (folder `engineeringplan/`). Also written in: `ImplementationPackage`, `ValidationPackage`.

## Interface

- `[AcceptanceDispatch] -> [DecisionRecord] : {AcceptedEvidence}` — sync call
- `[BuildBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call
- `[PolicyBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call
- `[ValidationBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call

## Requirements

None stated.
