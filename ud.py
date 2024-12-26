import json
from typing import Optional
from urllib.parse import urljoin

import aiohttp


class UnitedDomain:
    def __init__(
        self, cookie: str, csrf: str, base_url="https://www.united-domains.de/pfapi/"
    ):
        self._cookie = cookie
        self._csrf = csrf

        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def open(self):
        if self.session is not None:
            return

        headers = {"Cookie": self._cookie, "Http-X-Csrf-Token": self._csrf}

        self.session = aiohttp.ClientSession(headers=headers)

    async def close(self):
        if self.session is None:
            return

        await self.session.close()

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *args):
        _ = args
        await self.close()

    async def get_domains(self) -> list[dict]:
        assert self.session is not None

        url = urljoin(self.base_url, "configurable-domains")

        async with self.session.get(url) as resp:
            if resp.status != 200:
                body = await resp.read()
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    pass

                raise Exception("Unable to get list of domains", resp.status, body)

            body = await resp.json()

        return body["data"]

    async def get_subdomains(self, domain_id: str):
        assert self.session is not None

        url = urljoin(self.base_url, f"dns/domain/{domain_id}/records")
        async with self.session.get(url) as resp:
            if resp.status != 200:
                body = await resp.read()
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    pass

                raise Exception("Unable to get list of sub domains", resp.status, body)

            body = await resp.json()

        return body["data"]

    async def add_sub_domain(
        self,
        domain: str,
        domain_id: str,
        subdomain: str,
        rtype: str,
        ipaddr: str,
        lock_state: dict,
        ttl: int = 600,
    ):
        assert self.session is not None

        url = urljoin(self.base_url, f"dns/domain/{domain_id}/records")

        payload = {
            "record": {
                "id": None,
                "type": rtype,
                "sub_domain": subdomain,
                "domain": domain,
                "ttl": ttl,
                "filter_value": "",
                "standard_value": False,
                "address": ipaddr,
                "webspace": False,
                "formId": f"{rtype}0",
            },
            "domain_lock_state": lock_state,
        }

        async with self.session.put(url, json=payload) as resp:
            if resp.status != 200:
                body = await resp.read()
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    pass

                raise Exception("Unable to add subdomain", resp.status, body)
            body = await resp.json()

        return body["data"]
