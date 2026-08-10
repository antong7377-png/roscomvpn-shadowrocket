#!/usr/bin/env python3
"""Rebuild roscomvpn-full.conf: combine routing rules + current VLESS nodes.
Run via GitHub Actions after convert.py updates the .list files."""

import urllib.request, urllib.parse, json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# Fetch current VLESS nodes from our CLEAN subscription proxy
# (:2097 strips spx=/host= that 3x-ui injects and Shadowrocket rejects)
SUB_URLS = {
    "AVG-443":    "http://galyaev.ru:2097/sqed0gateb1jjobw",
    "AVG2-443":   "http://galyaev.ru:2097/5t4gx9i7wg8j7zeu",
    "AVY-46791":  "http://galyaev.ru:2097/u2zvf24ie77t9qzk",
    "GRPC-2083":  "http://galyaev.ru:2097/grpc5c59792b",
    "XHTTP-2087": "http://galyaev.ru:2097/xhttp5c59792",
}

def fetch_node(name, url):
    try:
        req = urllib.request.Request(url)
        ctx = __import__('ssl')._create_unverified_context()
        data = urllib.request.urlopen(req, context=ctx, timeout=15).read()
        import base64
        lines = base64.b64decode(data).decode().splitlines()
        for line in lines:
            if line.startswith("vless://"):
                # strip spx= + host= for Shadowrocket compat
                p = urllib.parse.urlparse(line)
                q = dict(urllib.parse.parse_qsl(p.query))
                q.pop("spx", None)
                q.pop("host", None)
                q.setdefault("encryption", "none")
                return f"vless://{p.username}@{p.hostname}:{p.port}?{urllib.parse.urlencode(q)}#{name}"
        return None
    except Exception as e:
        print(f"WARN: failed to fetch {name}: {e}")
        return None

# Build [Proxy] section
nodes = []
for name, url in SUB_URLS.items():
    node = fetch_node(name, url)
    if node:
        nodes.append(node)

proxy_section = "[Proxy]\n" + "\n".join(nodes)
proxy_section += "\n\n[Proxy Group]\nRoscomVPN = select, " + ", ".join(SUB_URLS.keys())

# Read routing rules from roscomvpn.conf
with open(os.path.join(BASE, "roscomvpn.conf")) as f:
    routing = f.read()

# Extract everything from [General] through [Rule] and [URL Rewrite]
# Replace [General] header info
header = f"""#!name=RoscomVPN + Пульс (AVG/XHTTP)
#!desc=VLESS Reality x5 + RoscomVPN split-tunneling | Auto-updated daily
#!update-url=https://cdn.jsdelivr.net/gh/antong7377-png/roscomvpn-shadowrocket@main/roscomvpn-full.conf

"""

# Find [General] section start
gen_start = routing.find("[General]")
rule_end = routing.find("[URL Rewrite]")
if rule_end == -1:
    rule_end = len(routing)

general_and_rules = routing[gen_start:rule_end]

# Build final config
final = header + general_and_rules + "\n" + proxy_section + "\n" + routing[rule_end:]

with open(os.path.join(BASE, "roscomvpn-full.conf"), "w") as f:
    f.write(final)

print(f"Rebuilt roscomvpn-full.conf with {len(nodes)} nodes")
for n in nodes:
    print(f"  {n[:80]}...")
