#!/usr/bin/env python3

import asyncio
import sys
import argparse
import json


from ud import UnitedDomain

from utils import get_credentials

async def main():
    parser = argparse.ArgumentParser("Show all domains")

    parser.add_argument("browser_request", help="Path to file from browser request")

    args = parser.parse_args()

    cookie, csrf = get_credentials(args.browser_request)

    async with UnitedDomain(cookie, csrf) as udclient:
        domains = await udclient.get_domains()

        print(json.dumps(domains, indent=2))




if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
