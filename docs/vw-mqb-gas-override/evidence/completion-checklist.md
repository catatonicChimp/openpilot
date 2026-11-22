# MQB Plan Completion and Approval Gates

This is the execution checklist for completing the design, not a claim that the vehicle fix is approved. All investigation is read-only until an implementation is separately approved.

## Settled Scope

- Investigate a minimal MQB-only zero-request override patch against an upstream-based openpilot revision.
- Treat current working StarPilot behavior as comparison evidence, not proof that openpilot is fixed.
- Preserve independent Panda authorization, genuine disengagement, existing brake/standstill semantics, and urgent fault alerts.
- Keep MQB revision/ECU compatibility explicit; no positive-acceleration or shared braking-grace change.

The upstream-based target is a planning assumption, not a user decision that "stock" means a patched fork. Confirm release-versus-fork deployment before implementation.

## Work Packages and Exit Criteria

| Package | Action | Exit evidence | Status |
| --- | --- | --- | --- |
| P1 Vendor definitions | Read-only revision and signal comparison | Source hashes, line/cell citations, compatibility register | Initial pass complete; receiver/comment/CRC review remains |
| P2 Source semantics | Trace CS/CC scheduling, events, MQB authorization, Panda dependencies and conflation | Pinned source findings in protocol-contract.md | Initial pass complete; installed revision mapping remains |
| P3 Route evidence | Match failing/working traces, driver inputs, ACC/TSK states, rejections and counters | Route IDs/timestamps, revisions, preserved logs and transition table | Blocked on owner identifiers/access |
| P4 Authority policy | Define eligible session and prioritized fault/loss-of-authority/disengagement decisions | Decision table covering preEnabled, softDisabling, stock-long, restart, stale input and brake/cancel timing | Pending P3 and target revision |
| P5 Transition policy | Define immediate press entry, release bridge and non-resumption exit | Measured timing evidence, explicit guards, no indefinite latch or invented timeout | Pending P3/P4 |
| P6 Command contract | Specify every changed field, standstill/HMS/start/stop behavior and variant restrictions | State-to-message table with vendor/stock-trace citations | Pending P3/P5 |
| P7 Sigil model | Separate workflow/runtime units; ordered initialization; state-aware exclusive branches and revision-bound approvals | Clean lint; checked outcomes including invalid-input/failure paths; no unexplained dropped events | Draft updated; strict checks still block |
| P8 Tests and build plan | Specify failing-first transition, encoding, safety and firmware checks | Test inventory, exact commands and dependencies pinned to chosen target | Coverage inventory drafted; commands deferred until target pinned |
| P9 Validation and contribution | Replay/bench, rollback review, approved controlled testing, result review, upstream coordination | Revision-bound results and explicit limitations | Not authorized; gates must pass in order |

## Required Owner Evidence

1. Failing and working route IDs with approximate timestamps; provide paths if logs are already local or on the NAS.
2. Installed StarPilot branch/commit for each route; hardware/radar firmware and Panda build identity where available.
3. Deployment intent: unmodified official openpilot release, or an upstream-based fork with a minimal unmerged fix. If the official release lacks the fix, these are different deliverables.

Do not deliberately reproduce faults on public roads to fill these gaps. Existing captures are preferred. No public upload of vendor datasets is required or authorized.

## Modeling Acceptance Scenarios

- Initialization precedes every runtime decision; restart starts without retained override state.
- Steady inactive/active/faulted samples are valid, not dropped events.
- Gas entry supersedes stale active requests only within independently eligible sessions.
- Release bridging is entered only from a valid override episode, never from unrelated non-active longitudinal control.
- Simultaneous fault/cancel/brake/gas is resolved by an explicit priority rule compatible with platform authorization.
- Fault remains dominant until confirmed cleared; a generic disengagement does not erase fault evidence.
- Missing or invalid input and non-resumption have reviewed outcomes; do not simulate them as success.
- Override cannot accidentally propagate stale starting/stopping/HMS commands.
- Workflow approval requires both evidence tracks, and pass/fail/unavailable outcomes are mutually exclusive.
- Candidate changes invalidate affected approvals; producing results alone does not accept them.

## Stop Conditions

### Safety/Firmware Inspection Outcome (latest)

Implementation follow-up (candidate commit `d8f0de2e`, branch `mqb-gas-override-candidate`): the controller now bounds the release bridge at two ACC message periods and then stands down to standby for three periods before active can resume. The bound is derived from the documented CS→selfdrived→controlsd→controller lag and the issue-thread report that three disabled ACC frames were tolerated while two faulted. It is a candidate policy, not an approved one: vehicle validation and the owner's before/after traces are still required. Safety policy was left unchanged because it was already minimal; no timestamp or grace-period safety change was added.

Safety exception verified present and covered by passing tests compiled from current sources. Two owner-visible risks are now recorded rather than resolved: (1) zero accel is legal even without gas, so a latched override that outlives pedal release would keep emitting ACC_OVERRIDE with safety's approval; (2) standalone Panda builds pin upstream opendbc, so only firmware built against the openpilot editable submodule contains the exception. Firmware provenance evidence is still required before any device test.

### Approval Reachability Resolution (latest)

ImplementationApprovalGate now has one top-level definition. RuntimePolicyDecision is declared at the common outer level because both EvidenceReview and the approval gate consume its contract. This removes the erroneous cross-unit dependency cycle and the prior unreached-gate finding without waiving either. The approved scenario reaches validation; the unapproved runtime-policy scenario cannot reach build or submission.

Full verification passes: 5 executable reference tests, 29 named Sigil assertions, syntax lint clean; strict check at budget 5000 has 0 errors, 4 wait-policy warnings, 8 information items, no SGC172 expansion escape, SGC175 unreached or SGC176 unit cycle. Results in strict-check.txt supersede older counts.

Retention semantics remain explicit and distinct from actuation: Inactive/Faulted cannot automatically activate/clear, state memory may persist without input, and no new active request is authorized by memory alone. A state diagram's absence of a timeout does not specify an infinite request stream. Active/Override liveness and non-resumption approval remain blocked on reviewed target data; no timeout or risk waiver has been invented. There is no additional source fact in the inspected revisions that establishes the missing vehicle-specific release deadline.

### Retention Versus Actuation Approval (latest)

Final rerun for this update: five reference tests and all 29 named Sigil assertions pass. Strict checking reports 0 errors, 4 wait warnings, 9 informational findings; one informational reachability finding concerns the nested ImplementationApprovalGate boundary summary despite the approved-path execution log reaching it. This is a remaining model presentation/reachability limitation, not a claim of a completely clean spec. Earlier count of eight informational findings is superseded.

RuntimePolicyReview is now an exclusive approval gate before ImplementationReview. Absent input-deadline or non-resumption evidence goes to a blocker record; hypothetical approval in simulation is not actual authorization. Runtime has explicit policyMissing and nonResumptionUnapproved branches with no command generation.

The executable model now tests a sequence, not just independent booleans: start in each retained state, independently revoke authority, then attempt three fresh-looking permitted requests with an active caller claim. Every post-revocation attempt is denied and state memory is preserved. This proves the reference contract only, not concurrent production scheduling or in-flight-frame cancellation. Five unittest methods pass alongside 29 Sigil assertions (28 earlier/expanded scenarios plus the policy-approval blocker). Strict check remains 0 errors, 4 wait warnings, 8 informational findings.

Final evidence needed for policy selection:

| Decision | Required information | Why source alone is insufficient |
| --- | --- | --- |
| Target authority mapping | Actual installed StarPilot revisions and intended openpilot release/fork revision | Current source checkout is not necessarily installed software; pre-enable/soft-disable semantics may differ. |
| Input age limits and response | Device build, logs with timestamps and representative bench/load measurements | Existing heartbeat/transport limits do not define acceptable actuation age. |
| Release bridge and non-resumption exit | Failing/working route IDs or local log paths, timestamps, revisions and corresponding ACC/TSK/pedal/control transitions | Cannot select duration or fault-safe transition from signal definitions or an uncorrelated success report. |
| Standstill/HMS companion fields | Stock/on-car captures matched to radar/ESP firmware and ACC type | Encodings alone do not determine safe hold/release interactions. |

Until supplied, these are approval blockers. Intentional retention does not permit an infinite actuation lease. No risk acceptance, arbitrary threshold, production atomicity or completed-spec claim is inferred from model success.

### Computed Contract Verification (latest)

Sigil simulator implementation was inspected: its branch engine chooses scenario arms and does not evaluate state-field predicates. Accordingly, no branch-selection run is claimed to prove retained-state or digest equality. Added `runtime_contract.py` and `test_runtime_contract.py`, an executable planning/reference model separate from vehicle-control code.

Four unittest methods check: all 512 combinations of retained state, freshness, independent authority, fault, permit, safety and caller-claimed state; revocation after previous success; mutation of each of six candidate identity fields revokes build and vehicle-test approvals; reverting identity does not revive approvals; missing/action-specific approvals and exact approved snapshots. These compute prerequisites instead of selecting an output-state branch. `verify-plan.py` now runs them and saves `contract-test-results.txt` before Sigil scenario checks.

Reference model requirement: caller OutputState cannot grant actuation. Candidate change is an explicit serialized lifecycle operation; real check/use atomicity, fault input acquisition and freshness detection require target implementation tests. This model neither validates production code nor establishes a release-bridge timeout. It is intentionally not imported by vehicle software.

### Contradictory Permission and Side-Effect Identity Update

AuthorityLost and fault decisions no longer enter the active-command encoding pipeline even when CommandPermit=allowed and SafetyOutcome=authorized are selected. Active/override decisions additionally pass a retained-state output check. OutputState must be derived from resolver state, not supplied independently by implementation callers. Sigil's opaque component simulation does not compute that equality; retained-fault denial tests use the conservative faulted output-check result and do not prove the derivation. That equality requires a real implementation unit test.

BuildIdentityGate precedes CandidateImplementation and VehicleIdentityGate precedes ControlledVehicleValidation. Both block stale/missing approval identity and only permit a matching snapshot; candidate digests must match the reviewed inputs and be checked immediately before the side effect. Actual digest computation and concurrent mutation prevention remain implementation requirements, not simulator capabilities.

Verification now runs 26 named cases: nine validation paths, four build/vehicle identity denials and thirteen runtime paths. All expected assertions pass, syntax lint is clean, strict checking has 0 errors, 4 wait warnings and 7 information items. Authority-loss/fault contradiction cases block CANOutput; positive authorized control reaches it. Side-effect denial cases do not reach build/vehicle execution or submission. This supersedes earlier scenario counts.

### Independent Liveness and Output Gating (latest)

Runtime now gates decision processing on InputLiveness and encoding on CommandPermit; Panda authorizes/rejects via an exclusive outcome. Missing/invalid input produces no new command. WatchdogHost is an independent entry modeling host apply inhibition, immediate/soft-disable paths, firmware SILENT and engaged-mismatch revocation without introducing new numeric timers. This specifies proposed responsibilities, not proof of installed implementation behavior.

Verification script now additionally checks runtime missing/invalid input, permit denial, Panda rejection, positive authorized output, authority loss and independent watchdog scenarios. Missing updates preserve Override/Faulted memory without output; retaining memory does not retain actuation authority. Tests exercise selected branches, not predicate computation or real queues. Watchdog-only runs have no runtime output episode and are not proof of concurrent cutoff latency.

Latest strict check: 0 errors, 4 wait warnings, 7 informational items. The four warnings remain visible: persistent state memory is intentional, but an approved fresh-input/non-resuming bridge duration is still absent. State memory and output authorization are separate. No risk acknowledgement was invented to suppress these findings.

### Runtime Wait Classification Update

Source-backed distinctions and citations are in protocol-contract.md under Watchdog and Event Classification. Inactive must not time-activate; Faulted must not time-clear. Observed authority loss now has an explicit guarded decision and lifecycle transitions. Four combined state-start scenarios assert Inactive/Active/Override become Inactive on authority loss, while Faulted remains Faulted; zero dropped events/bounds. Artifacts: `authority-loss-*.json`.

All nine validation assertions still pass after this runtime change. Strict result remains 0 errors, 4 warnings and 6 informational findings. Wait warnings are not waived: no-event persistence versus loss-of-input observation still needs explicit model representation, and persistent release bridging lacks a reviewed deadline/outcome. Existing watchdogs are documented but are not used as substitute timing evidence.

Only owner-supplied identifiers/access can close route comparison and actual deployed-build mapping. Target intent also remains unconfirmed. Timing measurements and the existing implementation's failure behavior must then inform the release/non-resumption policy; do not choose a timeout from heartbeat constants.

### Boundary Verification Update (latest result)

Conditional boundary summaries now declare approval, failure-recording and pass-to-next-gate dependencies without adding unconditional calls. All SGC172 expansion-boundary findings are resolved. Reproducible verification: `python3 mqb-evidence/verify-plan.py`.

Latest strict result at budget 5000: 0 errors, 4 runtime wait-policy warnings, 6 informational capacity/unit-size findings; no hidden findings or exploration-budget warning. All nine combined validation assertions still pass, with no ignored events or bounds. Failed/unavailable automated, bench and vehicle stages, stale identity and missing identity cannot reach submission. The stale identity scenario reaches the invalidation record. This supersedes earlier structural-warning counts.

These assertions cover the named combined paths, not all possible boundary-summary deviations or actual implementation behavior. Candidate identity comparison remains an opaque specified responsibility: the simulator does not calculate hashes. No owner-risk acknowledgement or arbitrary timeout has been added.

### Exclusive Validation and Candidate Identity Follow-Up

Validation stages now use exclusive outcome branches in separately invoked gate expansions. Pass invokes the next gate directly; fail/unavailable records the outcome and stops that episode. Candidate identity checking precedes submission; mismatch invokes approval invalidation, missing identity blocks, and only a match advances. Identity includes controller/safety revisions, resolved headers, firmware, configuration and target group. Implementations must snapshot these inputs per approval and recheck before each real side effect, not merely at final submission.

Nine combined scenarios are saved as `validation-*.json`, with `validation-summary.txt`: one success reaches submission; automated/bench/vehicle failure and unavailable outcomes, stale identity and missing identity do not. All nine have zero ignored events and zero bounds. These supersede earlier combined validation scenarios that used independent outputs.

Strict check at budget 5000 has zero errors, 14 warnings and five informational findings. Four warnings are runtime wait policies; the other ten are expansion-boundary declarations for recording/invalidation paths introduced by gate decomposition. These structural declarations still need refinement without introducing unconditional failure-recording calls. They are not owner-evidence blockers. No complete-plan or build-ready claim is made.

Owner-dependent runtime decisions: route IDs/paths and timestamps establish actual press/release gaps and whether faults precede rejection; deployed software/firmware identifies applicable engagement and safety semantics; deployment intent chooses official versus patched-fork target. Freshness thresholds additionally require timing/bench evidence, not simply owner preference. Non-resumption exit and standstill/HMS commands require trace review before approval. The model keeps these unresolved rather than selecting arbitrary wait limits.

Structural follow-up: workflow/runtime/validation units are separated; initialization ordering and dropped-event strict errors are resolved in the revised model. Strict check at budget 3000: 0 errors, 4 wait-policy warnings, 5 structural/capacity information items, no exploration-budget finding. Five combined scenario artifacts demonstrate state-preserving override, normal resumption, fault dominance, explicit fault clearance and workflow gate progression. P7 remains pending final predicate/freshness policy and review-loop semantics; do not interpret these runs as on-car validation.

Do not promote to a binding #!spec or export a build skeleton until P3-P7 are resolved and the chosen behavior is explicitly reviewed. A clean syntax linter or an OK simulator label alone does not establish coverage. Document hidden, ignored, bounded and unexplored runs. Do not invent vehicle facts to close the plan.
