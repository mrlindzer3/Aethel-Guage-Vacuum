# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/auth_gatekeeper.py
# ROLE: HMAC Token Validator & Leaky-Bucket Rate Limiter
# ARCHITECTURE: Cryptographic Security & Resource Governor
# ──────────────────────────────────────────────────────────────────────────

import hmac
import hashlib
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AuthGatekeeper")

class SecurityGatekeeper:
    def __init__(self, secret_key: str = "spacetime_secret_key_2026"):
        self.secret_key = secret_key.encode('utf-8')
        self.rate_limits = {}  # Format: {tenant_id: [timestamps]}
        self.max_requests_per_window = 10
        self.window_seconds = 1.0

    def verify_token(self, tenant_id: str, payload_string: str, provided_signature: str) -> bool:
        """
        Validates that the incoming matrix data was signed by an authorized tenant key.
        """
        message = f"{tenant_id}:{payload_string}".encode('utf-8')
        expected_signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        
        is_valid = hmac.compare_digest(expected_signature, provided_signature)
        if not is_valid:
            logger.warning(f"🔒 SECURITY ALERT: Invalid signature detected from tenant: {tenant_id}")
        return is_valid

    def check_rate_limit(self, tenant_id: str) -> bool:
        """
        Applies a strict leaky-bucket filter to protect the physical loop substrate.
        """
        current_time = time.time()
        if tenant_id not in self.rate_limits:
            self.rate_limits[tenant_id] = []

        # Prune expired timestamps outside our safety window
        self.rate_limits[tenant_id] = [t for t in self.rate_limits[tenant_id] if current_time - t < self.window_seconds]

        if len(self.rate_limits[tenant_id]) >= self.max_requests_per_window:
            logger.warning(f"🚫 RATE LIMIT: Tenant '{tenant_id}' choked. Exceeded capacity bounds.")
            return False

        self.rate_limits[tenant_id].append(current_time)
        return True
