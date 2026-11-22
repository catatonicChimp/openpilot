# VW MQB gas-override planning bundle

Archived 2026-11-22 before a machine upgrade.

- `design.md` — design and evidence notes.
- `plan.sigil` — binding engineering-work spec (exported to `build-plan/`).
- `runtime.sigil` — runtime design, still `#!craft`; unresolved timing policies
  remain explicit blockers and it is **not** an approved safety specification.
- `evidence/` — vendor-protocol contract, compatibility register, revision
  comparison, reference-model tests and scenario results.
- `build-plan/` — exported skeleton from `plan.sigil`.

Candidate implementation lives on `opendbc` branch `vw-testing-full`
(commit `d8f0de2e`) and the openpilot branches `vw-testing` / `vw-testing-full`.
