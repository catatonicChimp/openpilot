# ImplementationPackage

The expansion of `[ImplementationPackage]` (inside system `EngineeringPlan`).

Interface hash `918922e83ef8cb6b` · body hash `8c905b76bd93457f`.

## Components

- `[BuildBlock]` (service) — [buildblock.md](buildblock.md)
- `[BuildDispatch]` (service) — [builddispatch.md](builddispatch.md)
- `[CheckBuildApproval]` (service) — [checkbuildapproval.md](checkbuildapproval.md)
- `[ProduceCandidate]` (service) — [producecandidate.md](producecandidate.md)
- `{BuildReadiness}` (data) — [buildreadiness.md](buildreadiness.md)

## Boundary

The flows that cross into or out of this system: its contract.

- `[ApprovedWork] -> [ImplementationPackage] : {ApprovedScope} => {CandidateBundle}` — sync call
- `[BuildBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call

## Flows inside

- `[BuildDispatch] -> [ProduceCandidate] : {ApprovedScope} => {CandidateBundle}` — sync call
- `[CheckBuildApproval] => {BuildReadiness}` — return

## Control blocks

- branch `{BuildReadiness}.status`

## Depends on

- `EngineeringPlan` — [engineeringplan/](../engineeringplan/README.md)
- `ProduceCandidate` — [producecandidate/](../producecandidate/README.md)
