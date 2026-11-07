"""Core Outbound Domain Allowlist implementation."""
import re
from urllib.parse import urlparse
from typing import List, Dict, Any


class EgressDecision:
    def __init__(self, allowed: bool, url: str, reason: str):
        self.allowed = allowed
        self.url = url
        self.reason = reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed": self.allowed,
            "url": self.url,
            "reason": self.reason
        }


class OutboundDomainAllowlist:
    BLOCKED_IPS = ["127.0.0.1", "localhost", "169.254.169.254", "0.0.0.0"]

    def __init__(self, allowed_domains: List[str]):
        self.allowed_domains = allowed_domains

    def evaluate_url(self, url: str) -> EgressDecision:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()

        if not hostname:
            return EgressDecision(False, url, "Malformed URL: missing hostname")

        # 1. SSRF & Private IP blocking
        if hostname in self.BLOCKED_IPS or hostname.startswith("192.168.") or hostname.startswith("10."):
            return EgressDecision(False, url, f"SSRF Protection: Blocked private address '{hostname}'")

        # 2. Port restrictions (only 80 or 443 permitted)
        if parsed.port and parsed.port not in [80, 443]:
            return EgressDecision(False, url, f"Disallowed port: {parsed.port}")

        # 3. Match against allowed domains
        for pattern in self.allowed_domains:
            if pattern.startswith("*."):
                suffix = pattern[2:]
                if hostname == suffix or hostname.endswith("." + suffix):
                    return EgressDecision(True, url, f"Matches wildcard allowlist: {pattern}")
            elif hostname == pattern:
                return EgressDecision(True, url, f"Matches domain allowlist: {pattern}")

        return EgressDecision(False, url, f"Domain '{hostname}' not in allowlist")
