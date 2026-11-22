# ProduceCandidate

The expansion of `[ProduceCandidate]` (inside system `ImplementationPackage`).

Interface hash `82b9eb13e8729a19` · body hash `9e5e739e123a6a22`.

## Components

- `[ImplementAndPackage]` (service) — [implementandpackage.md](implementandpackage.md)

## Boundary

The flows that cross into or out of this system: its contract.

- `[BuildDispatch] -> [ProduceCandidate] : {ApprovedScope} => {CandidateBundle}` — sync call
- `[ImplementAndPackage] => {CandidateBundle}` — return

## Depends on

- `EngineeringPlan` — [engineeringplan/](../engineeringplan/README.md)
