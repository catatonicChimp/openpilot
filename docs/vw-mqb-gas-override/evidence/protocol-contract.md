# MQB Gas Override: Evidence and Compatibility Contract

Status: provisional, reviewed 2026-11-22. No controller or safety changes authorized by this document.

## Sources and Reproduction

Dataset root: `/Volumes/nas/devel/vw-mib/datasets/Volkswagen/03_CAN_KMatrix/kmatrix_all`.

`extract.py` reads DBC text and XLSX ZIP/XML without evaluating formulas or modifying originals. `vendor-extract.json` records source paths, SHA-256 hashes, DBC line references, worksheet names and cell coordinates. `compare.py` produces `revision-comparison.md` in chronological order.

Coverage: 44 archived ACAN/FCAN DBC files spanning November 2011 through June 2021, plus eight workbooks (2015, 2016 and 2021 selections). This is not all MQB buses, all archived revisions, MQB Evo, or all ECU variants. DBC comparison covers selected message IDs, signal positions/widths/endianness/sign/scales/offsets and value tables; receiver lists, comments, ranges, timing attributes and checksum sequences are extracted where present but not automatically compared. Workbook descriptions were spot-reviewed, not exhaustively interpreted.

No openpyxl dependency was installed: standard-library XML extraction was sufficient. Workbooks contain pre-existing broken named references; no recalculation or resave was attempted. Cached/formula-derived values, if encountered, are not independently recalculated evidence.

## Confirmed Definitions

References below use V7.16F workbooks under `0850_Antrieb/Archiv` (ACAN) and `0854_Fahrwerk/Archiv` (FCAN), filenames ending `20151104_MH.xlsx`. Sheet names include trailing spaces; trimmed names are shown here.

| Item | Evidence | Design consequence |
| --- | --- | --- |
| ACC state | ACAN `MQB_ACAN`, `AD20:AE20`: 2 standby, 3 active, 4 override, 6 reversible fault, 7 irreversible fault | Preserve fault distinction; override is not standby. |
| Acceleration request | ACAN `MQB_ACAN`, row 13; FCAN `MQB_FCAN`, row 17 | Both use 11-bit unsigned, scale 0.005, offset -7.22. DBC start bits: 24 in ACC_06, 53 in ACC_07. |
| Neutral/error | Same rows, logical values 2046 neutral and 2047 error | Raw 1444 represents zero; raw 2046 maps arithmetically to 3.01 but means neutral, not positive acceleration. Raw 2047 is an error code, not ordinary 3.015. |
| Stop distance | FCAN row 7 | Scale 0.01; raw 2046 neutral and 2047 error. Do not confuse neutral 20.46 with a physical distance command. |
| Secondary acceleration | FCAN row 14 | `ACC_Folgebeschl`: scale 0.03, offset -4.6; raw 254 is neutral (arithmetic 3.02). Not the main acceleration request. |
| Start/Stop | ACAN `AD12:AE12` | 0 stop permitted; 1 stop prohibited without a start request; 2 start requested; 3 system fault. Boolean assignment means a specific mode, not generic enable. |
| Coasting | FCAN `AD11:AE11` | 0 coasting permitted, 1 no transition into coasting, 2 coasting not permitted, 3 coasting request. Distinguish these meanings. |
| ACC type | ACAN `AD19:AE19` | 0 basic, 1 FollowToStop, 2 StopAndGo, 3 not coded. Owner's pACC description does not prove this field's value. |
| TSK status | ACAN `AD3115:AE3115` | 3 active, 4 override, 5 brake-only, 6 reversible off, 7 irreversible off. Feedback is not equivalent to the ACC command enum. |
| Periods | Column E on the corresponding V7.16 rows | ACC_06, ACC_07 and TSK_06 specify 20 ms cycles. Does not establish debounce/fault thresholds. |
| Integrity | ACC_06 row 5 and ACC_07 row 5 comments; BZ rows 6 | CRC comments give counter-indexed sequences and refer to separate end-to-end requirements. Four-bit BZ is not permission to skip values; retain existing algorithm until verified. |
| Diagnostic feedback | ACAN `BF848`, `ESP_Konsistenz_ACC_Botschaft` | Reports checksum/CRC, counter and long-timeout checks, also requests above a calibrated threshold. Useful additional trace channel; not a unique diagnosis. |

### Important topology qualification

In these matrices ACC_06 is on ACAN (0x122), ACC_07 on FCAN (0x12E); gateway routing matters. FCAN lists the redundant ACC_07 acceleration field's receiver as `Daempfer`, whereas other ACC_07 fields target brake ECUs. Do not claim that every ACC_07 field directly drives the same ECU. Confirm actual harness placement, gateway routing and firmware behavior from captures.

## Compatibility Risk Register

| Flag | Observed revision difference | Required treatment |
| --- | --- | --- |
| C01: early coasting semantics | V7.10 FCAN labels value 2 as dropping coasting and 3 as system error; V7.11 changes labels to coasting not permitted / coasting request | Never copy later value meanings onto earlier revisions without review. A label change alone does not prove firmware behavior changed. |
| C02: added control fields | V7.16 ACAN adds `ACC_DynErhoehung` at bit 14 and `ACC_Freilaufstrategie_TSK` at bit 15; FCAN adds `ACC_Boost` at bit 24 | Previously unused bits acquire semantics. Audit defaults and stock traffic; do not enable them through blanket active-field copying. |
| C03: later hold takeover | V7.23.02 FCAN adds HMS value 7 `HMS_uebernehmen` | Existing 0-5 meanings remain in compared tables, but later hold interactions need separate review; do not emit 7 as a generic release. |
| C04: later curve fields | V7.25 FCAN adds curve distance bits 40-45 and speed-delta bits 46-49; init codes are 62 and 11 | Default zero is not the documented no-curve-adjustment encoding. Determine whether omission matters before claiming later pACC compatibility. Do not change these fields as part of the override fix without evidence. |
| C05: state 5 applicability | V7.08 calls ACC state 5 undefined; later tables label shutdown reaction. V7.16 ACAN BF20 says this applies from MLBevo and is undefined for older projects | Table presence does not prove applicability to this Golf. Do not use state 5 to solve latch recovery without platform evidence. |
| C06: ECU and ACC variants | Receiver lists differ by revision and include conventional, hybrid, BEV engines, DQ/AL transmissions and multiple ESP families | Review receiver/sender applicability separately; no generic MQB compatibility approval from layout stability. |
| C07: main-switch field | V7.10 introduces TSK main-switch feedback at bits 42-43 | Early revisions may lack a proposed eligibility guard; do not interpret reserved zero as valid authority information. |

The main request layout, zero conversion, and override enum remain stable across the compared DBCs. This supports decoder reuse, not proof of identical transitions, calibrations, fault tolerance or compatibility across cars.

## Implementation Mapping and Remaining Gaps

Current `openpilot/opendbc_repo/opendbc/car/volkswagen/mqbcan.py` selects Start/Stop 1 and coasting 2 when enabled, retains gradient limits, and uses neutral secondary acceleration. Vendor definitions explain these values, but the reviewed cells do not mandate that exact combination during override. Preserve the working branch as evidence and validate each changed companion field against stock captures.

Do not equate every engaged-state field with an enable boolean. In particular, stopping, starting, HMS hold/release, and stale actuator long-control states require explicit precedence during pedal override. Include standstill/ESP-hold cases in tests without assuming gas press should request brake release.

No reviewed vendor passage establishes the one-frame release fault, precise re-entry delay, mandatory zero during override, or a safe indefinite override latch. These remain trace/control-semantics questions. Zero is our conservative proposed request policy, not a discovered universal VW override requirement.

## Compatibility Gate Before Broadening Scope

For each target group, record engine/gearbox/ESP/radar firmware, ACC type, harness topology, candidate matrix revision, semantic differences, stock evidence, controller/safety tests and validation status. Use `unknown`, `definition-reviewed`, `bench-validated`, or `vehicle-validated`; never infer vehicle validation from a dataset match.

Review groups: early MQB, 2015-2016 Golf-like conventional DSG, later MQB with additional hold/curve functions, manual/FollowToStop/basic ACC, and hybrid/BEV variants. These are proposed review groups, not proven compatibility classifications. Keep unrelated MQB Evo/PQ/MLB/MEB outside this approval.

Unresolved compatibility risks block a broad compatibility claim. Whether to use existing platform/firmware flags or a narrower rollout needs a separate decision after evidence review; do not invent runtime matrix-version detection.

Next: inspect target control semantics and stock traces; complete workbook receiver/comment/range/checksum review; attach exact vehicle identities and resolve eligibility/latch policy before implementation.

## Completeness Check Follow-Up

### Safety Policy and Firmware Inspection (2026-11-22)

Candidate implementation: branch `mqb-gas-override-candidate`, commit `d8f0de2e`. The release latch is now bounded to two ACC message periods with a three-period standby before active resumes, so the unbounded-override consequence above is addressed in the controller rather than by widening safety. The chosen counts come from pipeline lag plus the reported 3-frame tolerance; they remain vehicle-validation requirements.

Opened read-only; no branch, policy or device was changed by this inspection.

- local `opendbc/safety/modes/volkswagen_mqb.h:155` contains the narrow exception: exactly zero accel is allowed when `controls_allowed && gas_pressed_prev`, on both ACC_06 and ACC_07. `opendbc/safety/longitudinal.h` still blocks other longitudinal requests while gas is pressed.
- `opendbc.safety.tests.test_volkswagen_mqb`: 72 tests pass (9 skipped); `TestVolkswagenMqbLongSafety.test_accel_safety_check_gas_override` and `test_accel_safety_check` both pass. The harness compiles `libsafety` from the current C sources at import (`libsafety_py.py:25-53`), so these results exercise the checked-out code rather than a prebuilt library.
- Probe of the compiled policy: after a gas press in the same safety cycle, zero ACC_06, inactive ACC_06 and (next cycle) zero ACC_06 are all permitted. There is no safety-internal one-frame rejection of zero. Any press/release race is between separate observations (CarState vs Panda reception), not inside `tx_hook`.
- Probe without gas, controls allowed: zero ACC_06, zero ACC_07 and negative accel are all permitted, because zero lies inside the ordinary longitudinal range. Consequence: the existing override latch would still transmit `ACC_OVERRIDE` with zero after gas release if `longActive` never returns, and safety would not reject it. This is a genuine non-resumption behavior, not merely a rejected-frame problem. It remains an explicit policy blocker; no timeout was added.
- Firmware provenance: `panda/SConscript:4,98,161` imports the Python `opendbc` package and puts `opendbc.INCLUDE_PATH` on the include path. `openpilot/pyproject.toml:166` overrides opendbc to the editable `opendbc_repo` submodule, so a firmware build from the openpilot tree uses local safety. But `panda/pyproject.toml:17` pins `opendbc @ git+...@6cd8a71d...` for standalone builds. A standalone Panda build would compile upstream safety without this exception and must not be used to validate or ship the candidate.
- Do not treat the local checkout's successful safety tests as evidence that a deployed device runs that code. Firmware signature/build artifact and resolved include path still need recording.

### Pinned Source Inspection

Local revisions inspected: openpilot `11e2cfc7057d0dc3bfa9a3f0e90ae30bb78b64ec`; opendbc `abd636fd6bd66e60c372f658b9811fe69b2a1f92`; Panda checkout `5e8131ec962f6c2d88adda4ec7166e5d308f095e`; msgq checkout `42554d0a6f1cb2e87238c994760078be36cfdb27`. These identify local source, not the deployed device/firmware. Panda/msgq internals still need the dependency/runtime trace; their presence does not prove which safety implementation is compiled into the device.

- openpilot `openpilot/selfdrive/car/card.py:157,210,235`: nominal 100 Hz CAN-driven loop; publishes current carState while applying latest carControl, and calls apply while carControl is alive. This supports asynchronous lag, not atomic CS/CC snapshots.
- openpilot `openpilot/cereal/messaging/__init__.py:258`: alive uses 10 expected service periods. Distinguish receive freshness, payload log timestamp, validity, frequency and cross-topic consistency. Do not invent a tighter deadline without measuring and reviewing the existing failure path.
- openpilot `openpilot/selfdrive/pandad/pandad.cc:68`: send thread gates sendcan on age less than one second and fake-send mode; this path does not inspect Event.valid. Therefore card's sendcan valid flag is not alone a transmission inhibit. One second is transport filtering, not an acceptable controller freshness target.
- openpilot `openpilot/selfdrive/controls/controlsd.py:162`: cruiseControl.cancel is true when car cruise is enabled and either openpilot is disabled OR pcmCruise is false. It is not a safe standalone cancel/authority guard for non-PCM opLong. Inspect physical cancel button events and platform safety enable/cancel logic instead.
- openpilot `openpilot/selfdrive/selfdrived/state.py:8,93`: enabled includes preEnabled, enabled, softDisabling and overriding. Do not assume CC.enabled means fully active. Review pre-enable and soft-disable behavior explicitly.
- openpilot `openpilot/selfdrive/car/car_events.py:142,155`: standstill brake produces preEnableStandstill; physical cancel edges generate buttonCancel under the stated configuration guard. Preserve these distinctions.

Next source tasks: trace MQB physical cancel and enable authorization into safety; identify board firmware dependency/build provenance; inspect msgq queue/conflation and timestamp semantics; compare current source with actual installed fork. Do not use carControl.cancel as the proposed unconditional latch-clear signal.

### Follow-Up Results: Safety, Firmware and Messaging

#### Watchdog and Event Classification Follow-Up

Pinned openpilot source `openpilot/selfdrive/selfdrived/events.py:856` maps communication failure/average-frequency failure to SOFT_DISABLE and NO_ENTRY. StateMachine in `state.py:7,48` uses a three-second soft-disable timer while the condition persists; enabled remains true during that phase. Do not silently replace this system policy with an MQB-specific immediate disable for every generic communication event.

The same events file at lines 911, 922, 931 and 941 maps ACC fault, controls mismatch, invalid CAN and missing CAN bus to IMMEDIATE_DISABLE. `selfdrived.py:333` checks safety configuration, safety RX validity and mismatch persistence; `:379` distinguishes canTimeout/canValid. Their observations can be delayed relative to physical Panda authorization. The proposed override resolver must never manufacture authority to bridge such a loss.

Pinned Panda `board/main.c:112` sets heartbeat thresholds to five ignition-on and two ignition-off 1 Hz counts. Lines 175-222 tick the counter, check engaged mismatch, and on missing heartbeats clear engaged state and select SAFETY_SILENT. These are firmware liveness safeguards, not the controller's acceptable CS/CC age or a safe release-bridge duration. Exact timeout phase depends on counter scheduling/receipt; verify device build before applying these facts.

Wait classification:

| State / condition | Proposed plan requirement | Evidence still needed |
| --- | --- | --- |
| Inactive, no engagement | Persist inactive; never time-activate | No route needed to prohibit automatic activation. |
| Faulted, fault not cleared | Persist fault; never time-clear | No route needed to prohibit automatic fault clearance. |
| Explicit authorization revoked, immediate-disable or genuine disengagement | Clear override episode; no active request; preserve fault reporting where applicable | Wire authoritative observations from selected target; simultaneous-event tests. |
| Active/Override and processing stops | Do not generate new commands from this component; existing host/firmware watchdogs act independently | Bench review of actual queued/repeated output and installed build. |
| Generic commIssue soft-disable | Preserve existing system state-machine behavior; do not equate enabled with fully healthy | Selected revision and service-specific input classification. |
| Pedal released, control not yet resumed | A temporary bridge may preserve override only while authority remains independently valid | Failing/working routes plus load/bench timing; finite policy still unapproved. |

The Sigil AuthorityLost branch now represents observed revocation, not an invented timeout. It returns active/override to inactive and leaves Faulted faulted. Internal source predicates and missing-data detection remain opaque and must be implemented only after target-version review. Four wait warnings remain explicit rather than accepting an unreviewed indefinite hold policy.

- opendbc `opendbc/safety/modes/volkswagen_common.h:92`: TSK statuses 3/4/5 count as engaged; 2 also counts as main-on. In opLong mode, this helper does not require stock cruise engagement to authorize controls, but clears authorization when main-on is false. Do not gate opLong solely on TSK active, or the fix could prevent ordinary engagement.
- Same file, line 108: Set/Resume falling edges assign controls_allowed from main-on. MQB `volkswagen_mqb.h:74` decodes these buttons and clears controls on physical cancel bit 13. Lines 88-103 decode raw gas and combine engine brake switch with ESP brake pressure.
- opendbc `opendbc/safety/safety.h:312`: brake rising edge clears controls; a held brake also clears while moving. Heartbeat mismatch handling at line 296 independently clears controls after three mismatch checks. Do not confuse this mechanism with the still-separate heartbeat transport timeout or invent its scheduling interval.
- Panda `board/main.c:13` includes opendbc safety.h. `SConscript:161` and Python API use opendbc.INCLUDE_PATH for protocol compatibility hashes. The build environment's resolved Python package matters: local checkout identity alone does not prove which safety code produced a firmware binary. Require resolved include path, firmware signature/build artifact hash and deployed signature evidence.
- openpilot cereal SubMaster creates conflated subscriptions (`openpilot/cereal/messaging/__init__.py:213`) and records payload logMonoTime (line 254). msgq provides configurable conflation (`msgq/ipc_py.cc:70`) with tests in `msgq/tests/test_messaging.py:26`. Latest-value semantics are per topic, not a cross-topic atomic snapshot. No msgq change is proposed.
- pandad sendcan uses a non-conflated subscriber (`pandad.cc:54`) and an age filter. Inspect queue backlog and ordering with logs/bench measurements; do not change conflation or transport queues to hide the fault.

Source review therefore closes the basic authorization and build-dependency questions, but deployment mapping, control-data ages under load, firmware signature provenance, and fault/working trace interpretation remain evidence tasks. Existing safety authorization stays independent; no controller mirror may replace Panda's decision.

The design now distinguishes physical gas evidence from the derived control override flag; adds coherent input and prioritized authority decisions; preserves Faulted through disengagement; requires explicit acceptance of vehicle results; and binds validation records/approvals to candidate and firmware identity. Standstill hold, stale inputs, restart and variant tests are explicit requirements.

These refinements do not resolve the missing ECU transition evidence or final authority/latch policy. The state-machine event source is still schematic: conditional event emitters do not yet encode mutually exclusive guards tied to the current state. Strict checking exposes impossible/out-of-context events; do not suppress these by adding broad self-loops without deciding their actual behavior.
