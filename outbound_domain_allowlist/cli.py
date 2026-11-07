"""CLI for outbound-domain-allowlist."""
import sys
import argparse
from .allowlist import OutboundDomainAllowlist


def main():
    parser = argparse.ArgumentParser(description="Outbound Domain Allowlist")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        allowlist = OutboundDomainAllowlist(["api.github.com", "*.openai.com", "pypi.org"])
        urls = [
            "https://api.github.com/repos",
            "https://chat.openai.com/v1",
            "http://169.254.169.254/latest/meta-data",
            "https://evil-attacker-site.com"
        ]
        for u in urls:
            res = allowlist.evaluate_url(u)
            print(f"URL: {u} -> Allowed: {res.allowed} ({res.reason})")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
