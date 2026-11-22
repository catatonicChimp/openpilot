# vw-mqb-gas-override-plan

The top level of the spec: every component no expansion or tree holds.

MQB zero-request gas-override engineering work specification. This specifies deliverables and gates, not approved vehicle-control behavior. Runtime design: vw-mqb-gas-override.sigil (craft; unresolved policies remain blocked). Evidence contract: mqb-evidence/protocol-contract.md. Test inventory and owner inputs: mqb-evidence/completion-checklist.md. No deployment, firmware flashing, public-road reproduction or dataset publishing authorized.

Interface hash `4f53cda18c2baa0c` · body hash `7f6d4e8b6bcf42b6`.

## Components

- `[EngineeringPlan]` (service) — [engineeringplan.md](engineeringplan.md)
- `[PlanRunner]` (service) — [planrunner.md](planrunner.md)
- `{AcceptedEvidence}` (data) — [acceptedevidence.md](acceptedevidence.md)
- `{BlockerRecord}` (data) — [blockerrecord.md](blockerrecord.md)

## Boundary

No flow crosses it.

## Flows inside

- `[PlanRunner] -> [EngineeringPlan] : {EvidenceBundle} => {ValidationDecision}` — sync call

## Depends on

- `EngineeringPlan` — [engineeringplan/](../engineeringplan/README.md)
