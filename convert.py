#!/usr/bin/env python3
"""Convert v2fly domain lists to Shadowrocket RULE-SET format."""
import os

GEOSITE_DIR = "geosite/data"
GEOIP_DIR = "geoip/data"
OUT_DIR = "."

CATEGORIES = {
    'win-spy': 'REJECT',
    'torrent': 'REJECT',
    'category-ads': 'REJECT',
    'telegram': 'PROXY',
    'youtube': 'PROXY',
    'google-play': 'PROXY',
    'github': 'PROXY',
    'twitch-ads': 'PROXY',
    'google-deepmind': 'PROXY',
    'category-ru': 'DIRECT',
    'whitelist': 'DIRECT',
    'microsoft': 'DIRECT',
    'apple': 'DIRECT',
    'epicgames': 'DIRECT',
    'riot': 'DIRECT',
    'escapefromtarkov': 'DIRECT',
    'steam': 'DIRECT',
    'twitch': 'DIRECT',
    'pinterest': 'DIRECT',
    'faceit': 'DIRECT',
    'gemini': 'PROXY',
    'private': 'DIRECT',
}

def convert_v2fly(filepath, action):
    rules = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('domain:'):
                rules.append(f"DOMAIN-SUFFIX,{line[7:]},{action}")
            elif line.startswith('full:'):
                rules.append(f"DOMAIN,{line[5:]},{action}")
            elif line.startswith('regexp:'):
                continue
            elif '.' in line and not line[0].isdigit():
                rules.append(f"DOMAIN-SUFFIX,{line},{action}")
    return rules

def convert_cidr(filepath, action):
    rules = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            cidr = line if '/' in line else f"{line}/32"
            rules.append(f"IP-CIDR,{cidr},{action},no-resolve")
    return rules

def main():
    for cat, action in CATEGORIES.items():
        fp = os.path.join(GEOSITE_DIR, cat)
        if os.path.exists(fp):
            rules = convert_v2fly(fp, action)
            out = os.path.join(OUT_DIR, f"{cat}.list")
            with open(out, 'w') as f:
                f.write('\n'.join(rules) + '\n')
            print(f"  {cat}.list: {len(rules)} rules ({action})")
        else:
            print(f"  SKIP {cat}: not found at {fp}")

    fp = os.path.join(GEOIP_DIR, "private.txt")
    if os.path.exists(fp):
        rules = convert_cidr(fp, "DIRECT")
        out = os.path.join(OUT_DIR, "ip-private.list")
        with open(out, 'w') as f:
            f.write('\n'.join(rules) + '\n')
        print(f"  ip-private.list: {len(rules)} rules (DIRECT)")
    else:
        print(f"  SKIP ip-private: not found at {fp}")

if __name__ == '__main__':
    main()
