"""Checks derived predicates, including contradictory claims and candidate changes."""
from dataclasses import fields, replace
from itertools import product
import unittest

from runtime_contract import ApprovalRegistry, Candidate, Request, RuntimeSession, State, active_command_eligible


class RuntimeContractTests(unittest.TestCase):
    def test_retained_state_after_independent_watchdog_revocation(self):
        for state in State:
            session = RuntimeSession(state)
            stale_allowed_request = Request(state, True, True, False, True, True, State.ACTIVE)
            self.assertEqual(session.attempt(stale_allowed_request), state in (State.ACTIVE, State.OVERRIDE))
            session.watchdog_revoke()
            # Even repeated fresh-looking requests and contradictory active claims fail.
            for _ in range(3):
                self.assertFalse(session.attempt(stale_allowed_request))
            self.assertEqual(session.retained_state, state)

    def test_output_prerequisites_exhaustive(self):
        checked = 0
        for state, fresh, authority, fault, permit, safety, claim in product(
            State, (False, True), (False, True), (False, True),
            (False, True), (False, True), State,
        ):
            request = Request(state, fresh, authority, fault, permit, safety, claim)
            result = active_command_eligible(request)
            if not fresh or not authority or fault or state in (State.INACTIVE, State.FAULTED):
                self.assertFalse(result, request)
            elif permit and safety:
                self.assertTrue(result, request)
            else:
                self.assertFalse(result, request)
            # The claim is irrelevant: state/authority must be independent prerequisites.
            self.assertEqual(result, active_command_eligible(replace(request, claimed_output_state=State.ACTIVE)))
            checked += 1
        self.assertEqual(checked, 512)

    def test_revoke_authority_after_previous_success(self):
        request = Request(State.OVERRIDE, True, True, False, True, True, State.ACTIVE)
        self.assertTrue(active_command_eligible(request))
        self.assertFalse(active_command_eligible(replace(request, authority_valid=False)))
        self.assertFalse(active_command_eligible(replace(request, state=State.FAULTED)))
        self.assertFalse(active_command_eligible(replace(request, inputs_fresh=False)))

    def test_every_identity_field_mutation_invalidates_both_actions(self):
        original = Candidate('controller-A', 'safety-A', 'headers-A', 'firmware-A', 'config-A', 'golf-A')
        for field in fields(Candidate):
            registry = ApprovalRegistry(original)
            for action in ('build', 'vehicle-test'):
                registry.approve(action)
                self.assertTrue(registry.can_execute(action))
            changed = replace(original, **{field.name: getattr(original, field.name) + '-changed'})
            registry.change_candidate(changed)
            self.assertEqual(registry.invalidations, 1)
            for action in ('build', 'vehicle-test'):
                effects = []
                self.assertFalse(registry.execute(action, effects.append))
                self.assertEqual(effects, [])
            # Returning to old contents must not resurrect an old approval.
            registry.change_candidate(original)
            self.assertFalse(registry.can_execute('build'))
            self.assertFalse(registry.can_execute('vehicle-test'))

    def test_new_action_specific_approval_uses_exact_snapshot(self):
        candidate = Candidate('c', 's', 'h', 'f', 'cfg', 'group')
        registry = ApprovalRegistry(candidate)
        self.assertFalse(registry.can_execute('build'))
        registry.approve('build')
        effects = []
        self.assertTrue(registry.execute('build', effects.append))
        self.assertEqual(effects, [candidate])
        self.assertFalse(registry.execute('vehicle-test', effects.append))
        registry.change_candidate(candidate)  # no actual change does not revoke approval
        self.assertTrue(registry.can_execute('build'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
