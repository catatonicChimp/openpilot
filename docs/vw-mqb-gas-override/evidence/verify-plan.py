"""Run structural checks and assert selected validation paths do not advance."""
import json
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent
DOC = BASE.parent / 'vw-mqb-gas-override.sigil'
CLI = Path.home() / '.config/opencode/skills/sigil/scripts/bin/sigil'


def run(*args):
    return subprocess.run(['python3', str(CLI), *args], capture_output=True, text=True)


preconditions = ['ImplementationOutcome.status=approved', 'VehicleApproval.status=approved',
                 'AcceptanceOutcome.status=accepted', 'ApprovalIdentity.status=match',
                 'BuildIdentity.status=match', 'VehicleIdentity.status=match',
                 'RuntimePolicyDecision.status=approved']
cases = [('success', None), ('automated-fail', 'AutomatedOutcome.status=fail'),
         ('automated-unavailable', 'AutomatedOutcome.status=unavailable'),
         ('bench-fail', 'BenchOutcome.status=fail'),
         ('bench-unavailable', 'BenchOutcome.status=unavailable'),
         ('vehicle-fail', 'VehicleOutcome.status=fail'),
         ('vehicle-unavailable', 'VehicleOutcome.status=unavailable'),
         ('stale', 'DEFAULT_STALE'), ('missing', 'ApprovalIdentity.status=missing')]
summary = []
contracts = subprocess.run(['python3', '-m', 'unittest', 'discover', '-s', str(BASE),
                            '-p', 'test_runtime_contract.py', '-v'], capture_output=True, text=True)
(BASE / 'contract-test-results.txt').write_text(contracts.stdout + contracts.stderr)
print(contracts.stdout + contracts.stderr, end='')
assert contracts.returncode == 0, 'Executable contract tests failed'
for name, change in cases:
    choices = preconditions.copy()
    if change:
        key = 'ApprovalIdentity.status' if change == 'DEFAULT_STALE' else change.split('=')[0]
        choices = [x for x in choices if not x.startswith(key + '=')]
        if change != 'DEFAULT_STALE':
            choices.append(change)
    result = run('view', str(DOC), '--sim', '+'.join(choices), '--json')
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    (BASE / f'validation-{name}.json').write_text(result.stdout)
    log = '\n'.join(data['log'])
    reached = '-> [UpstreamSubmissionReview]' in log
    assert reached == (name == 'success'), (name, log)
    assert not data.get('ignored') and not data.get('bounds'), name
    if name == 'stale':
        assert 'InvalidationRecord' in log
    summary.append(f'{name}: submission={reached}, ignored=0, bounds=0')

print('\n'.join(summary))
(BASE / 'validation-summary.txt').write_text('\n'.join(summary) + '\n')
blocked_policy = [x for x in preconditions if not x.startswith('RuntimePolicyDecision.status=')]
result = run('view', str(DOC), '--sim', '+'.join(blocked_policy), '--json')
assert result.returncode == 0, result.stderr
data = json.loads(result.stdout)
assert not any('[CandidateImplementation]' in line or '-> [UpstreamSubmissionReview]' in line
               for line in data['log'])
(BASE / 'policy-approval-blocked.json').write_text(result.stdout)
print('runtime policy unapproved: build blocked, submission blocked')
for gate, side_effect in [('BuildIdentity', '[CandidateImplementation]'),
                          ('VehicleIdentity', '[ControlledVehicleValidation]')]:
    for status in ['stale', 'missing']:
        choices = [x for x in preconditions if not x.startswith(gate + '.status=')]
        if status != 'stale':  # stale is the conservative first/default branch
            choices.append(gate + '.status=' + status)
        result = run('view', str(DOC), '--sim', '+'.join(choices), '--json')
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        log = '\n'.join(data['log'])
        assert not any(side_effect in line for line in data['log']), (gate, status, log)
        assert '-> [UpstreamSubmissionReview]' not in log
        (BASE / f'identity-{gate}-{status}.json').write_text(result.stdout)
        print(f'{gate} {status}: side effect blocked, submission blocked')
runtime_cases = [
    ('missing-override', 'MQBStateResolver=Override', False),
    ('missing-faulted', 'MQBStateResolver=Faulted', False),
    ('invalid', 'InputLiveness.status=invalid', False),
    ('input-policy-missing', 'InputLiveness.status=policyMissing', False),
    ('nonresumption-unapproved', 'InputLiveness.status=fresh+StateDecision.kind=nonResumptionUnapproved+CommandPermit.status=allowed+SafetyOutcome.status=authorized', False),
    ('permit-denied', 'InputLiveness.status=fresh+StateDecision.kind=active', False),
    ('authority-lost', 'InputLiveness.status=fresh+StateDecision.kind=authorityLost', False),
    ('panda-reject', 'InputLiveness.status=fresh+StateDecision.kind=active+CommandPermit.status=allowed', False),
    ('authorized', 'InputLiveness.status=fresh+StateDecision.kind=active+OutputState.kind=active+CommandPermit.status=allowed+SafetyOutcome.status=authorized', True),
    ('authority-lost-contradiction', 'InputLiveness.status=fresh+StateDecision.kind=authorityLost+CommandPermit.status=allowed+SafetyOutcome.status=authorized', False),
    ('fault-contradiction', 'InputLiveness.status=fresh+StateDecision.kind=fault+CommandPermit.status=allowed+SafetyOutcome.status=authorized', False),
    ('retained-fault-denial', 'MQBStateResolver=Faulted+InputLiveness.status=fresh+StateDecision.kind=active+CommandPermit.status=allowed+SafetyOutcome.status=authorized', False),
    ('watchdog-control-dead', 'WatchdogStatus.kind=controlDead', False),
    ('watchdog-heartbeat-lost', 'WatchdogStatus.kind=heartbeatLost', False),
    ('watchdog-authority-revoked', 'WatchdogStatus.kind=engagedMismatch', False),
]
for name, scenario, expected_output in runtime_cases:
    result = run('view', str(DOC), '--sim', scenario, '--json')
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    (BASE / f'runtime-{name}.json').write_text(result.stdout)
    log = '\n'.join(data['log'])
    emitted = '-> [CANOutput]' in log
    assert emitted == expected_output, (name, log)
    assert not data.get('ignored') and not data.get('bounds'), name
    if name == 'missing-override':
        assert data['states'] == ['[MQBStateResolver] Override']
    if name == 'missing-faulted':
        assert data['states'] == ['[MQBStateResolver] Faulted']
    print(f'{name}: CANOutput={emitted}, ignored=0, bounds=0')
lint = run('lint', str(DOC))
print(lint.stdout, end='')
assert lint.returncode == 0
check = run('check', str(DOC), '--mode', 'spec', '--all', '--budget', '5000')
(BASE / 'strict-check.txt').write_text(check.stdout + check.stderr)
print(check.stdout + check.stderr, end='')
assert check.returncode < 2, 'Strict structural errors remain'
assert 'SGC172' not in check.stdout + check.stderr, 'Expansion boundaries remain unresolved'
assert 'SGC175' not in check.stdout + check.stderr, 'An unreachable unit remains'
assert 'SGC176' not in check.stdout + check.stderr, 'A unit dependency cycle remains'
