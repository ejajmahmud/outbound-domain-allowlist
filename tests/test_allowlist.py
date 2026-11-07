"""Tests for outbound-domain-allowlist."""
import unittest
from outbound_domain_allowlist.allowlist import OutboundDomainAllowlist


class TestDomainAllowlist(unittest.TestCase):
    def setUp(self):
        self.al = OutboundDomainAllowlist(["api.internal.com", "*.trusted.org"])

    def test_ssrf_blocking(self):
        res = self.al.evaluate_url("http://169.254.169.254/creds")
        self.assertFalse(res.allowed)
        self.assertIn("SSRF", res.reason)

    def test_wildcard_domain(self):
        res = self.al.evaluate_url("https://sub.trusted.org/data")
        self.assertTrue(res.allowed)

    def test_disallowed_domain(self):
        res = self.al.evaluate_url("https://untrusted.xyz")
        self.assertFalse(res.allowed)
