import json
from typing import Any
import re

A_AAAA_RECORDS_REG = re.compile(r"^([^@][\w\.-]+)\s+IN\s+(A|AAAA)\s+(.*)$")
ORIG_REG = re.compile(r"^\$ORIGIN\s+(.*)\.$")

def get_browser_headers(data: dict[str, Any]):
    for key in data.keys():
        if key.startswith("Request Headers "):
            return key

    raise KeyError("Request Headers not found")


def get_headers(data: dict[str, Any], key: str, header: str):
    for obj in data[key]["headers"]:
        if obj["name"] == header:
            return obj["value"]

    raise KeyError(f"No {header!r} found in {key!r}")

def get_credentials(path: str) -> tuple[str, str]:
    """
    Returns the cookie and csrf from firefox
    request headers export
    """

    with open(path, "r") as fp:
        browser = json.load(fp)


    key = get_browser_headers(browser)

    cookie = get_headers(browser, key, "Cookie")
    csrf = get_headers(browser, key, "Http-X-Csrf-Token")

    return cookie, csrf

def parse_zonefile(path: str):
    res = {"domain": None, "records": {}}

    with open(path, "r") as fp:
        while True:
            line = fp.readline()
            if line == "":
                break

            line = line.strip()

            m = ORIG_REG.search(line)

            if m is not None:
                if res["domain"] is not None:
                    raise Exception("$ORIGIN already present")

                res["domain"] = m.group(1)
                continue

            m = A_AAAA_RECORDS_REG.search(line)

            if m is not None:
                subdomain, rtype, ipaddr = m.groups()

                if rtype not in res["records"]:
                    res["records"][rtype] = []

                res["records"][rtype].append((subdomain, ipaddr))


    return res
