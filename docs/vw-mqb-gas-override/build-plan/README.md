# Export of vw-mqb-gas-override-plan.sigil

Exported from `vw-mqb-gas-override-plan.sigil` (spec hash `1a2827eb9b2ff3d7`) by sigil export.

- `manifest.json` is the contract: per system, its interface hash, body hash, components and what it depends on. It is written last; a folder without it is no finished export.
- `<system>/README.md` describes a system: its components, its boundary (the flows that cross it) and what it depends on.
- `<system>/<component>.md` states one component: kind, description, interface, requirements and lifecycle, as the spec writes them.
- `<system>/system.json` holds the same, machine-readable.

## Systems

- `vw-mqb-gas-override-plan` (top) — [vw-mqb-gas-override-plan/](vw-mqb-gas-override-plan/README.md) — depends on `EngineeringPlan`
- `EngineeringPlan` (expansion) — [engineeringplan/](engineeringplan/README.md) — depends on `EvidencePackage`, `ImplementationPackage`, `PolicyPackage`, `ValidationPackage`
- `EvidencePackage` (expansion) — [evidencepackage/](evidencepackage/README.md) — depends on `EngineeringPlan`, `PolicyPackage`
- `ImplementationPackage` (expansion) — [implementationpackage/](implementationpackage/README.md) — depends on `EngineeringPlan`, `ProduceCandidate`
- `PolicyPackage` (expansion) — [policypackage/](policypackage/README.md) — depends on `EngineeringPlan`
- `ProduceCandidate` (expansion) — [producecandidate/](producecandidate/README.md) — depends on `EngineeringPlan`
- `ValidationPackage` (expansion) — [validationpackage/](validationpackage/README.md) — depends on `EngineeringPlan`
