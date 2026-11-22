# EngineeringPlan

The expansion of `[EngineeringPlan]` (inside system `vw-mqb-gas-override-plan`).

Interface hash `1b9ca8b1fb41c701` · body hash `75c4c59354c9cba5`.

## Components

- `[ApprovedWork]` (service) — [approvedwork.md](approvedwork.md)
- `[DecisionRecord]` (service) — [decisionrecord.md](decisionrecord.md)
- `[EvidencePackage]` (service) — [evidencepackage.md](evidencepackage.md)
- `[ImplementationPackage]` (service) — [implementationpackage.md](implementationpackage.md)
- `[PolicyBlock]` (service) — [policyblock.md](policyblock.md)
- `[PolicyPackage]` (service) — [policypackage.md](policypackage.md)
- `[ValidationPackage]` (service) — [validationpackage.md](validationpackage.md)
- `{ApprovedScope}` (data) — [approvedscope.md](approvedscope.md)
- `{CandidateBundle}` (data) — [candidatebundle.md](candidatebundle.md)
- `{EvidenceBundle}` (data) — [evidencebundle.md](evidencebundle.md)
- `{PolicyDecision}` (data) — [policydecision.md](policydecision.md)
- `{ValidationDecision}` (data) — [validationdecision.md](validationdecision.md)

## Boundary

The flows that cross into or out of this system: its contract.

- `[AcceptanceDispatch] -> [DecisionRecord] : {AcceptedEvidence}` — sync call
- `[BuildBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call
- `[PlanRunner] -> [EngineeringPlan] : {EvidenceBundle} => {ValidationDecision}` — sync call
- `[ValidationBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call
- `[AssembleEvidence] => {EvidenceBundle}` — return
- `[EvaluateCandidate] => {ValidationDecision}` — return
- `[EvaluateReadiness] => {PolicyDecision}` — return
- `[ImplementAndPackage] => {CandidateBundle}` — return

## Flows inside

- `[ApprovedWork] -> [ImplementationPackage] : {ApprovedScope} => {CandidateBundle}` — sync call
- `[EvidencePackage] -> [PolicyPackage] : {EvidenceBundle} => {PolicyDecision}` — sync call
- `[PolicyBlock] -> [DecisionRecord] : {BlockerRecord}` — sync call
- `{CandidateBundle} -> [ValidationPackage] : {CandidateBundle} => {ValidationDecision}` — sync call

## Control blocks

- branch `{PolicyDecision}.status`

## Depends on

- `EvidencePackage` — [evidencepackage/](../evidencepackage/README.md)
- `ImplementationPackage` — [implementationpackage/](../implementationpackage/README.md)
- `PolicyPackage` — [policypackage/](../policypackage/README.md)
- `ValidationPackage` — [validationpackage/](../validationpackage/README.md)
