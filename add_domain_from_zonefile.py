#!/usr/bin/env python3

import argparse
import asyncio
import sys

from ud import UnitedDomain
from utils import get_credentials, parse_zonefile


def is_domain_present(domaindb, rtype: str, subdomain: str):
    for obj in domaindb[rtype]:
        if obj["sub_domain"] == subdomain:
            return True

    return False


async def main():
    parser = argparse.ArgumentParser("Show all domains")

    parser.add_argument("browser_request", help="Path to file from browser request")
    parser.add_argument("zonefile", help="Path to zonefile")

    args = parser.parse_args()

    cookie, csrf = get_credentials(args.browser_request)

    zone = parse_zonefile(args.zonefile)

    async with UnitedDomain(cookie, csrf) as udclient:
        domains = await udclient.get_domains()

        domain_by_name = {}

        for domain in domains:
            name = domain["domain"]

            domain_by_name[name] = domain

        target_domain: str = zone["domain"]

        domain_id = domain_by_name[target_domain]["id"]
        lock_state = domain_by_name[target_domain]["domain_lock_state"]

        domaindb = await udclient.get_subdomains(domain_id)

        for rtype, specs in zone["records"].items():
            for subdomain, ipaddr in specs:
                if is_domain_present(domaindb, rtype, subdomain):
                    print(f"Subdomain {subdomain!r} already present")
                    continue

                print(f"Adding {subdomain!r} ({rtype!r}) with ip {ipaddr!r}")
                await udclient.add_sub_domain(
                    target_domain, domain_id, subdomain, rtype, ipaddr, lock_state
                )
                await asyncio.sleep(2)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
