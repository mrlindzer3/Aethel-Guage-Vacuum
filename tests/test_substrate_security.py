# ──────────────────────────────────────────────────────────────────────────
# FILE: tests/test_substrate_security.py
# ROLE: Cryptographic Access and Ternary Gatekeeper Unit Tests
# ARCHITECTURE: Automated Verification and Quality Assurance Framework
# ──────────────────────────────────────────────────────────────────────────

import unittest
import numpy as np
from core.email_auth_gate import EmailAuthGate
from core.ternary_logic_unit import TernaryLogicUnit

class TestSubstrateSecurity(unittest.TestCase):
    def setUp(self):
        self.node_count = 640
        self.target_email = "mr.lindzer3@gmail.com"
        self.auth_gate = EmailAuthGate(admin_email=self.target_email)
        self.tlu = TernaryLogicUnit(node_count=self.node_count)

    def test_unauthenticated_execution_isolation(self):
        """Validates that the gatekeeper completely blocks unauthenticated runtime executions."""
        # The account status is unverified at initial allocation state
        self.assertFalse(self.auth_gate.is_account_created)
        
        # Verify that running a calculation pass throws an absolute PermissionError
        with self.assertRaises(PermissionError):
            self.auth_gate.enforce_gatekeeper_protection()

    def test_cryptographic_email_handshake_flow(self):
        """Validates the two-way token verification loop using the target email profile."""
        # Step 1: Initiate an authorized registration handshake request
        challenge_token = self.auth_gate.initiate_account_request()
        self.assertIsNotNone(challenge_token)
        self.assertEqual(len(challenge_token), 8)  # Verify length constraints

        # Step 2: Test an invalid response pass to ensure the security wall holds
        failed_attempt = self.auth_gate.verify_email_response_handshake("INVALID_TOKEN")
        self.assertFalse(failed_attempt)
        self.assertFalse(self.auth_gate.is_account_created)

        # Step 3: Mirror the correct challenge token to complete the registration handshake
        successful_attempt = self.auth_gate.verify_email_response_handshake(challenge_token)
        self.assertTrue(successful_attempt)
        self.assertTrue(self.auth_gate.is_account_created)

        # Step 4: Ensure the protection constraint passes without raising exceptions
        try:
            self.auth_gate.enforce_gatekeeper_protection()
        except PermissionError:
            self.fail("Security gate un-intuitively threw a PermissionError on an authenticated user.")

if __name__ == "__main__":
    unittest.main()
