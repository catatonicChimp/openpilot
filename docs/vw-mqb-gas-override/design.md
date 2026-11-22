# VW MQB: Preserve ACC Engagement During Driver Gas Override

Status: Draft for review; not an approved safety specification or implementation.
Engineering work specification: `vw-mqb-gas-override-plan.sigil` is a separate binding `#!spec` for deliverables and approval gates. Its exported skeleton is in `vw-mqb-gas-override-build-plan/`. The runtime design remains craft and unapproved pending evidence; the engineering specification does not erase those blockers or authorize deployment.
Date: 2026-11-22
Owner/test vehicle: Andrew Taylor; 2016 VW Golf Mk7, DSG, higher-end pACC radar (owner description; exact radar firmware and ACC type to record).

Deployment clarification from owner: currently runs StarPilot with a personal override fix; intends to move to stock openpilot. Installation uses a gateway harness. Before/after routes are available, but route IDs, timestamps, deployed commits and firmware identity have not yet been supplied. Use the current stock openpilot architecture as the proposed implementation target, while treating StarPilot behavior as separate evidence. Determine whether "stock" means unmodified release or a narrowly patched upstream-based fork: an unmerged custom fix cannot be present in an unmodified release by assumption.

## Purpose

Prevent the repeatable cruise fault associated with accelerator overrides during openpilot longitudinal control on the test vehicle. Keep the vehicle's ACC session in the proper override state instead of briefly disengaging and reengaging it.

The owner reports that without a fix, repeated override-related faults make opLong effectively unusable on this vehicle. The existing personal branch resolves the problem in the owner's testing; coverage across other MQB vehicles is not established.

## Proposed Decision

### Candidate Implementation (2026-11-22)

`openpilot/opendbc_repo` branch `mqb-gas-override-candidate`, commit `d8f0de2e`: override eligibility is gated on MQB opLong with cruise available and no ACC fault; override forces zero acceleration, standby stopping and HUD state; the release bridge is bounded to two ACC message periods and followed by three standby periods before active resumes. Safety policy is unchanged. Tests cover release, standdown, re-press, and fault/unavailable clearing. This is still an unapproved candidate: the bound requires the owner's before/after routes and vehicle validation before it can satisfy the runtime policy gate.

### Dataset Evidence Update (2026-11-22)

See [protocol contract and compatibility register](mqb-evidence/protocol-contract.md), [chronological DBC comparison](mqb-evidence/revision-comparison.md), and the reproducible extraction scripts in `mqb-evidence/`.

Read-only analysis covers 44 archived ACAN/FCAN DBCs (2011-2021) and eight selected workbooks. Confirmed: override enum, main acceleration encoding, neutral/error sentinels, 20 ms message periods, Start/Stop and coasting meanings. Raw zero request is 1444; raw 2046 is neutral, not an ordinary 3.01 m/s^2 request.

Compatibility review is now a required gate: flag differences in semantics, reserved-bit reuse, hold functions, curve fields, ACC type, engine/transmission/ESP/radar firmware and gateway/harness topology. Stable layouts do not establish behavioral compatibility. Later pACC curve fields have nonzero init codes, and early coasting labels differ; audit these before broadening validation beyond this Golf.

The reviewed vendor definitions do not prove the exact override companion-field combination, release debounce, or a safe persistent latch. Keep those as unverified behavior requirements requiring stock traces and control-state review. The current state machine is conceptual, not exhaustive or deployment-ready.

Implement a narrow MQB-only zero-acceleration override fix, based on the existing `vw-mqb-gas-override` branch. Strengthen entry/release transition handling and regression coverage before proposing it upstream.

Do not depend on a general change allowing positive acceleration during driver override. Do not treat this document as authorization to deploy unvalidated vehicle-control changes.

## Evidence and Related Work

Evidence was reviewed on 2026-11-22. GitHub statuses can change.

| Source | Finding | Implication |
| --- | --- | --- |
| [opendbc issue #2874](https://github.com/commaai/opendbc/issues/2874) | Reports MQB cruise faults when feathering the throttle with opLong. Discussion identifies brief disengage/reengage transitions and possible rejected CAN frames. | Same failure family; state transitions and safety timing both require examination. |
| [opendbc PR #3135](https://github.com/commaai/opendbc/pull/3135) | Open with merge conflicts at review time. Implements VW override signalling. Discussion proposes narrowing the required safety changes to VW. | Closest upstream coordination point. |
| [opendbc PR #3165](https://github.com/commaai/opendbc/pull/3165) | Open with merge conflicts at review time. Broad multi-brand positive-acceleration override changes, shared safety changes, and braking grace period. | Larger scope than needed for the proposed zero-request MQB fix. |
| [openpilot PR #37557](https://github.com/commaai/openpilot/pull/37557) | Merged 2026-06-16. Prioritizes immediate-disable alerts over user-disable alerts. | Addresses silent fault reporting, not fault prevention. Verify inclusion in each tested fork. |
| [Personal branch](https://github.com/catatonicChimp/opendbc/tree/vw-mqb-gas-override) | Implements MQB override state, active ACC fields, a zero-request safety exception, release latching, and regression tests. Owner reports success. | Starting point, not independently validated production evidence. |

The issue discussion includes a report that a two-frame disabled interval faulted one vehicle while a three-frame interval did not. Do not generalize that threshold to all ACC variants. A combined test branch reportedly fixed reproduction, but that does not isolate the necessity of each constituent change.

The personal branch's comments describe a one-frame standby transition on release followed by a delayed latched fault. Preserve this as an owner/implementation finding until supporting traces are attached and independently reviewed. No tests were executed as part of drafting this document.

## Scope and Non-Goals

In scope:

- MQB longitudinal CAN state and acceleration-request consistency.
- Entry into gas override using the latest observed vehicle state.
- Release latching while the control state catches up.
- A narrowly scoped MQB zero-request safety exception.
- Controller, message, safety, and transition regression tests.

Out of scope:

- Positive acceleration during driver override.
- PQ, MLB, or MEB behavioral changes without separate evidence and validation.
- Shared braking grace periods or broad longitudinal safety relaxation.
- Counter/checksum bypasses, suppressing faults, or automatic recovery from a latched ECU fault.
- Radar swaps, stopping-distance behavior, or Start/Stop steering faults.

## Core Invariants

Watchdog follow-up: `mqb-evidence/protocol-contract.md` now classifies persistent inactive/fault waits, observed authority loss, process stoppage, generic communication soft-disable, and pedal-release bridging separately. AuthorityLost has an explicit lifecycle path; it cannot clear Faulted. Source heartbeat thresholds and the three-second soft-disable timer are not release-bridge deadlines. No arbitrary timer is approved by this update.

1. Driver override is not the same as disengagement: relinquish longitudinal actuation without unnecessarily terminating the ACC session.
2. Faults and genuine disengagement take priority over override. A latch must never preserve engagement through cancel, brake-related disengagement, loss of authorization, or faults.
3. In the proposed override state, request exactly 0.0 m/s^2 and encode the ACC fields required for that state consistently.
4. Do not pass stale positive or negative `actuators.accel` through an override path.
5. Apply this behavior only when MQB openpilot longitudinal control is configured and authorized.
6. Normal bounded acceleration resumes only when pedal and control-side override indications are clear and longitudinal control is active again.
7. Preserve existing disengaged/inactive behavior and normal steering safety behavior.

A zero acceleration request is a protocol value, not a guarantee of zero physical acceleration or braking. Vehicle behavior, driver pedal input, gradients, and ECU arbitration still determine actual motion.

## Inputs and Definitions to Verify

| Input | Intended role | Review requirement |
| --- | --- | --- |
| `CS.out.gasPressed` | Latest controller-visible pedal indication | Establish freshness relative to Panda's received pedal state. |
| `CC.cruiseControl.override` | Control-side override indication | Verify its exact meaning in the target revision; do not assume it is gas-only. |
| `CC.longActive` | Permission/state for normal longitudinal actuation | Verify ordering on pedal press, release, enable, and disengagement. |
| `CC.enabled` | Candidate engagement input | Not sufficient by assumption; inspect actual control-state semantics. |
| `CS.out.accFaulted` | Vehicle fault indication | Must override any engagement/override request. |
| Cruise availability, cancel/brake/disengagement signals | Select disengaged state and invalidate latch | Define authoritative guards from the target revision. |

Define `eligible_for_override` from verified engagement, health, platform, and longitudinal configuration semantics. It must not be inferred from a previously latched override alone. A true cancel/brake/fault must win even if a delayed `CC` still appears engaged.

## Proposed State Resolution

Resolve one MQB command state per controller update. Use that decision consistently when constructing acceleration and HUD messages; retain existing transmission schedules.

Priority is: fault, genuine disengagement/ineligibility, override, normal active, then existing standby/off behavior.

| Condition | Command state | Request |
| --- | --- | --- |
| Faulted | Existing fault representation | Inactive |
| Genuinely disengaged/ineligible | Existing standby/off representation | Inactive |
| Eligible and pedal or valid control-side override is asserted | Override | Zero |
| Eligible, override latched, waiting for normal longitudinal reactivation | Override | Zero |
| Eligible, override inputs clear, normal longitudinal active | Active | Existing bounded request |
| Otherwise | Existing standby/off representation | Inactive |

### Immediate Entry

The current personal branch enters override only when `CC.longActive` is false. Review and improve this: the pedal can already be pressed while the latest `CarControl` still reports active longitudinal control.

When eligible, enter override immediately on the latest observed gas press, even if `longActive` remains true. Force both the override state and zero acceleration, rather than merely changing the state flag.

### Guarded Release Latch

After pedal release, do not emit standby simply because `longActive` has not returned yet. Hold override until both override indications are clear and normal longitudinal control resumes, unless a higher-priority disengagement or fault ends eligibility.

The following is conceptual logic, not build-ready code:

```python
if faulted or not eligible_for_override:
    override_latched = False
elif gas_pressed or valid_control_override:
    override_latched = True
elif override_latched and not long_active:
    override_latched = True
else:
    override_latched = False
```

Open design issue: if normal control never resumes while eligibility remains nominally true, a latch could persist indefinitely. Review real control states to establish whether this is a legitimate sustained override or a loss-of-authority condition. Define the exit before implementation approval; do not add an arbitrary timeout that recreates the standby fault or silently invents disengagement behavior.

### Message Consistency

- Keep engaged-state fields consistent with `ACC_OVERRIDE` in both relevant acceleration messages (`ACC_06` / `ACC_07`, subject to target DBC verification).
- Do not combine override status with inactive acceleration encoding where the vehicle expects an active request.
- Preserve required engine/coasting inhibition fields according to verified stock traces; avoid assuming all active-state flags should be copied blindly.
- Derive HUD override indication from the same resolved command state.
- Verify fault-first priority and disengagement behavior in helper functions.
- Check counter continuity and checksum validity independently of state selection.

## Safety Policy

Retain the existing longitudinal checks. Add only the MQB-specific exception needed to transmit exactly zero while the driver presses gas and controls are allowed, within the existing MQB longitudinal mode/message allowlists.

During gas override under this narrow policy:

- Zero request: permitted only with existing control authorization.
- Inactive sentinel: retain existing allowed behavior.
- Positive or negative nonzero active requests: rejected.
- Controls disallowed: the exception must not authorize active zero requests.

Review the actual encoded zero value for each checked acceleration field, units, rounding, and sentinel handling. Confirm all existing checks remain enforced. Treat the policy as a narrow value exception, not proof that the safety layer validates the entire semantic ACC state.

### Remaining Timing Race

Panda may receive a pedal press before the controller observes it. A braking command already in flight can still be rejected. Immediate controller entry reduces stale requests but cannot guarantee elimination of every rejection.

Measure this separately. Do not introduce a grace period or relax braking restrictions just to silence rejections without an independently reviewed safety rationale. If zero requests on release encounter a mismatch in observed pedal state, verify that normal checks permit the required transition while controls remain authorized.

## Test Matrix

Tests must cover decoded outgoing messages and temporal sequences, not just helper return values.

| Scenario | Required assertion |
| --- | --- |
| Gas press with stale `longActive=True` and a negative request | Override and zero on the first controller update observing gas. |
| Gas press with stale positive request | No stale positive request passes through override. |
| Sustained gas with delayed control state | Continuous override; consistent engaged fields. |
| Gas released while `longActive=False` | No intermediate standby frame. |
| Control override remains after physical release | Continue valid override until indications clear. |
| Both override indications clear and `longActive=True` | Resume active, bounded requests. |
| Rapid repeated press/release and phase offsets | No unintended standby/active flapping. |
| Cancel, brake-related disengagement, or fault during override | Clear latch and emit existing authorized inactive/fault behavior. |
| Disengagement with stale gas/control indications | No re-entry or continued engagement from the latch. |
| New engagement after prior override/disengagement | No stale latch leaks into the new session. |
| No normal-control resumption | Apply the explicitly reviewed loss-of-authority policy. |
| Controls allowed/disallowed crossed with pedal state | Zero exception only under the intended authorization. |
| Zero, inactive, positive, negative, and boundary encodings | Preserve safety limits and reject unauthorized requests. |
| CAN counter wrap and transmission phase offsets | Valid checksums and expected counter sequence. |
| PQ/MLB/MEB and stock longitudinal | No behavioral change from the MQB-only patch. |

Include genuine-disengagement precedence when gas is simultaneously asserted. Decode both acceleration messages and HUD state, and assert required active/inactive fields. Exercise sequences across actual ACC transmission intervals, not only consecutive controller frames.

## Validation and Evidence Package

Prefer recorded-route analysis, automated tests, replay, and bench/HIL validation before any controlled vehicle evaluation. Do not intentionally provoke repeated faults on public roads.

Record for each before/after run:

- Vehicle model/year/transmission, radar part number and firmware, and decoded ACC type.
- openpilot/fork commit, opendbc commit, Panda firmware revision/build identity, configuration and longitudinal settings.
- Route ID, preserved rlogs, and precise failure/override timestamps.
- Outgoing ACC state, acceleration requests, and relevant engaged-state fields.
- `gasPressed`, control-side override, `enabled`, `longActive`, cancel/brake, and fault indications.
- TSK status transitions, Panda rejection data, and outgoing counter/checksum continuity.

Separate two acceptance questions: does the ECU state-transition fault disappear, and do safety-related message gaps remain? Do not equate fewer faults with complete protocol correctness.

Check that the tested fork includes the urgent takeover alert behavior from openpilot #37557. Alerting remains an independent safety requirement even after fault prevention improves.

## Expected Implementation Locations

Paths are relative to the opendbc repository; verify against the target revision before editing.

| File | Expected responsibility |
| --- | --- |
| `opendbc/car/volkswagen/carcontroller.py` | MQB eligibility, override latch, request selection, consistent command-state use. |
| `opendbc/car/volkswagen/mqbcan.py` | Encode override and engaged-state fields; preserve fault priority. |
| `opendbc/car/volkswagen/pqcan.py` and `mlbcan.py` | Signature compatibility only if required; no new behavior. |
| `opendbc/car/volkswagen/tests/test_volkswagen.py` | Controller transitions and decoded message regressions. |
| `opendbc/safety/modes/volkswagen_mqb.h` | Narrow zero-request exception. |
| `opendbc/safety/tests/test_volkswagen_mqb.py` | Authorization, value boundaries, and pedal-state tests. |

Build/deployment integration must identify the corresponding Panda firmware changes. Do not assume a Python-only controller update is sufficient when safety policy changes are required.

## Review and Build Plan

Detailed work packages, exit criteria, owner evidence and modeling scenarios are tracked in [completion checklist](mqb-evidence/completion-checklist.md). The basic source trace now includes safety enable/cancel/brake rules, opendbc firmware inclusion and topic conflation; see the follow-up results in the protocol contract. No msgq transport change is proposed.

1. Pin target revisions; inspect engagement/override semantics and relevant contribution/safety requirements. Preserve unrelated local edits, including the pending submodule URL change.
2. Attach traces supporting the personal branch's entry/release diagnosis and identify exact ACC hardware.
3. Agree on eligibility guards, fault/disengagement priority, and behavior if normal control never resumes.
4. Add failing transition/message/safety tests for the agreed behavior.
5. Implement the smallest MQB-only change, with no unrelated refactors or broader safety changes.
6. Run targeted VW controller/safety tests and the applicable full regression suite. Record commands, revisions, results, and limitations.
7. Validate replay/bench evidence and only then plan controlled vehicle testing with an explicit rollback path and known-good controller/firmware pair.
8. Comment on #2874 and coordinate with #3135's participants before opening a competing PR. Present zero-request override separately from positive-acceleration support.

## Review Checklist / Open Questions

### Completeness Review Update

The Sigil companion is now `#!craft`, not a final binding specification. It explicitly joins protocol and compatibility evidence, distinguishes validation rejection from infrastructure unavailability, requires a vehicle-results acceptance step, and records revision-bound validation outcomes. Passing syntax checks is not approval to implement or deploy.

Source inspection in the current local checkout confirms:

- `openpilot/selfdrive/controls/controlsd.py:96` derives `CC.enabled` from selfdrive state.
- `openpilot/selfdrive/controls/controlsd.py:102` derives `longActive` from enabled, absence of longitudinal override events, and longitudinal configuration.
- `openpilot/selfdrive/controls/controlsd.py:161` derives `cruiseControl.override` from enabled and not longActive; it is not an independent physical gas signal.
- `openpilot/selfdrive/selfdrived/events.py:731` maps gas override to longitudinal override; `pedalPressed` is a user-disable event.
- `openpilot/selfdrive/selfdrived/selfdrived.py:252` distinguishes accelerator-disengage settings and brake rising-edge/moving conditions. Do not replace this with unconditional brake disengagement at standstill.
- Current VW controller `update_gas_override` still uses `enabled && !longActive`; immediate entry and independent authority remain proposed improvements, not implemented behavior.

Before implementation, pin actual commit IDs for these references and inspect their complete event/scheduling context. The current review does not establish a complete authority predicate.

Required additions to the test plan: coherent/fresh input snapshots, restart without stale override, simultaneous fault/cancel/gas, standstill hold with stale start/stop requests, and loss of longitudinal control without resumption. Review every companion field independently; zero acceleration alone does not neutralize hold/start/stop semantics.

Fault state now persists through a generic disengagement event in the conceptual lifecycle; it clears only on explicit fault-cleared-and-disengaged evidence. Authority decisions must be mutually exclusive and prioritized. Normal steady-state updates must preserve state without being mistaken for missing control input.

Unresolved authority, stale-input deadlines and persistent-latch recovery remain blocking policy questions. Do not add arbitrary timeouts, invent runtime matrix-version detection, or promote the document to `#!spec` to make the checker pass.

Approvals bind the controller/safety/firmware/configuration/target-group identity and supporting evidence. Candidate changes invalidate downstream approvals. Validation failure and inability to execute tests both block advancement. Vehicle results require explicit acceptance; producing a report alone is not success. Recovery requires a tested known-good firmware/controller pair and a reviewed rollback procedure.

- [ ] Confirm exact radar variant, firmware, ACC type, and target software revisions.
- [ ] Verify `CC.enabled`, `longActive`, and `cruiseControl.override` semantics and update ordering.
- [ ] Define authoritative cancel, brake, fault, and loss-of-authorization guards despite delayed control state.
- [ ] Resolve the non-resuming-control/latch persistence case.
- [ ] Verify required stock override fields for this ACC variant.
- [ ] Establish whether stale in-flight messages still cause meaningful counter gaps or faults.
- [ ] Verify all safety boundaries, encoded zero values, and inactive sentinels.
- [ ] Confirm urgent takeover alert behavior is present in the tested fork.
- [ ] Attach before/after evidence and test results; no universal MQB compatibility claim yet.
- [ ] Agree upstream submission ownership and whether to update #3135 or open a focused successor.

## Definition of Done

### Latest Design Checks

#### Structural Follow-Up (supersedes the earlier counts below)

Latest approval ownership cleanup: ImplementationApprovalGate is a standalone unit, and its shared RuntimePolicyDecision contract is declared at the common outer level. Strict check no longer reports unreached approval gates or unit cycles. Verification: 5 reference tests and 29 named Sigil assertions pass; lint clean; strict 0 errors, 4 wait-policy warnings, 8 informational items. Intentional memory retention is not an actuation lease; runtime approval still blocks absent input-deadline and non-resumption policies. This supersedes older reachability caveats and counts below.

Latest retention/actuation update: an explicit RuntimePolicyReview gate blocks implementation approval until input-liveness and release-non-resumption evidence is accepted. Runtime policy-missing branches produce no commands. Reference-model watchdog sequences now test repeated requests after independent authority revocation in every retained state; all fail eligibility without erasing state memory. Five reference-model tests and 29 named Sigil assertions pass; strict findings are 0 errors, 4 wait warnings and 8 informational items. Exact owner/bench evidence requirements are tabulated in the completion checklist. The remaining policy decisions are blocked, not silently selected.

Computed contract follow-up: the plan now includes a small executable reference model, not vehicle code. Four unittest methods cover 512 computed output-prerequisite combinations and approval invalidation for every candidate identity field. Caller-claimed active state cannot override retained Faulted/Inactive, revoked authority, stale input or a present fault. Changing candidate identity after approval blocks build and vehicle testing, including after reverting to the old identity. See `mqb-evidence/runtime_contract.py`, `mqb-evidence/test_runtime_contract.py` and `mqb-evidence/contract-test-results.txt`. Sigil branch simulation alone cannot compute these relationships. Actual target implementation and concurrency/timing validation remain required.

Latest output/identity follow-up: authority-loss/fault decision branches bypass command generation regardless of allowed permit/safety selections. Active/override commands pass a retained-state output check whose equality to actual resolver state must be proven by implementation tests. Build and vehicle execution now have identity gates before their side effects, not only before submission. `verify-plan.py` passes 26 named assertions; strict check remains 0 errors, 4 wait warnings, 7 information items. These tests do not prove opaque predicate correctness, hash computation or concurrent mutation exclusion. See completion checklist for precise limits.

Latest liveness update: Runtime has explicit InputLiveness and CommandPermit gates plus exclusive Panda outcomes. Independent watchdog paths are modeled outside the controller episode; no new timeout threshold is asserted. The verification script checks absent/invalid updates produce no CANOutput, retained fault/override memory does not itself authorize output, denied permits/rejected safety do not transmit, and the authorized positive-control case does transmit. Strict check is now 0 errors, 4 wait warnings, 7 informational findings. Existing queue/in-flight frames and concurrent watchdog latency remain bench-evidence tasks, not guarantees supplied by these simulations.

Latest boundary verification supersedes all older counts: 0 strict errors, 4 runtime wait-policy warnings, 6 informational findings at budget 5000. Conditional boundary summaries resolve every expansion-escape finding. `mqb-evidence/verify-plan.py` reruns lint, strict checks, and nine combined gate assertions; all pass their expected submission-reachability assertions. See `mqb-evidence/strict-check.txt` and `mqb-evidence/validation-summary.txt`. The remaining wait/authority decisions still require explicit policy and deployment/trace evidence; they are not waived.

Latest validation follow-up supersedes the counts in this subsection: exclusive per-stage gates and candidate identity/invalidation now pass nine combined gate assertions. See `mqb-evidence/validation-summary.txt` and the completion checklist. Strict checking currently reports 0 errors, 14 warnings and 5 information items; gate-boundary declaration warnings remain structural work, distinct from four unresolved runtime wait-policy warnings. Owner evidence is not claimed to block structural refinement.

Separated EvidenceReview, Runtime and Validation expansions. Runtime construction now precedes input processing. A single branch on StateDecision.kind selects a command event; state-specific transitions preserve fault dominance and handle ordinary steady-state decisions. Repeated initialization preserves an existing session/fault, rather than erasing it. This is a proposed model contract, not implemented vehicle behavior.

Strict checking with `--mode spec --all --budget 3000` now reports zero errors, four warnings and five informational findings, with no exploration-budget warning. Remaining warnings are state wait/freshness policies; information concerns unit size and capacity. They are not waived. The model still leaves the internal authority predicate opaque and blocked on route/deployment evidence; exclusive branch selection does not prove predicate correctness.

Simulation reports 26 scenarios OK, zero failed/cut. Five additional combined scenarios were checked: override persists; override resumes active; a normal active decision cannot clear Faulted; explicit fault-cleared/disengaged returns Inactive; and the complete workflow approval/pass chain reaches submission review. Combined results have no ignored events or bounds. The isolated MoreEvidenceRequired path still hits the review-loop base-case bound, so it does not prove indefinite review-loop behavior. These model runs do not validate CAN timing or safety code.

Artifacts: `mqb-evidence/strict-check.txt` and `mqb-evidence/combined-scenario-1.json` through `combined-scenario-5.json`. The previous craft sketch is retained as `mqb-evidence/pre-structure-review.sigil` for comparison. No runtime policy was selected solely to silence a checker; timeouts and authority decisions remain unresolved.

Source follow-up is recorded with pinned revisions in `mqb-evidence/protocol-contract.md`. Newly identified guard hazards: `CC.enabled` includes preEnabled and softDisabling, and `CC.cruiseControl.cancel` may be set during normal non-PCM opLong. Neither is sufficient alone as a runtime authorization/disengagement predicate. Fresh CS and latest CC are asynchronous; pair them with timestamps/identity rather than requiring equal-age samples. `sendcan.valid` is not alone an output gate in the inspected pandad send thread.

- Syntax lint: clean as part of `lint --deep`; craft checks still report unresolved ordering/wait policies and structural/capacity questions.
- `view --sim all`: 31 scenarios report OK, no cut runs. This is not a behavioral pass: some event scenarios are ignored in states where guards should have prevented their emission, and downstream validation branches are not all reached by isolated scenarios.
- Strict `check --mode spec --all`: 4 errors, 10 warnings and 4 informational findings. Errors concern out-of-context lifecycle events; warnings include initialization ordering and undeclared wait behavior. Exploration also left 135 overlap runs unrun at the default budget. No exhaustive exploration claim is made.
- Next model work: encode state-aware mutually exclusive decisions; structurally enforce initialization before input handling; separate evidence/runtime/validation units; run combined gate and lifecycle scenarios; resolve authority/freshness/non-resumption policy before spec promotion.

No arbitrary timeout or event-ignore self-loop was added to silence findings. No vehicle code changed and no build skeleton was exported.

Review questions are resolved; controller and safety tests pass with recorded results; required CAN fields and transitions are evidenced; fault/disengagement precedence is preserved; no unintended non-MQB changes occur; and the actual tested controller/Panda revision pair is documented. Success on this Golf is reported as vehicle-specific validation unless broader coverage is obtained.
