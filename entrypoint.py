import urllib.parse
import json
from pathlib import Path

with open("vless.url") as f:
    raw = f.read().strip()

uri = raw.replace("vless://", "")
userinfo, hostinfo = uri.split("@")
uuid = userinfo
hostport, params = hostinfo.split("?", 1)
host, port = hostport.split(":")

query = urllib.parse.parse_qs(params)

get = lambda k: query[k][0] if k in query else None

config = {
    "log": {"loglevel": "warning"},
    "inbounds": [
        {
            "port": 10808,
            "listen": "0.0.0.0",
            "protocol": "socks",
            "settings": {"auth": "noauth"}
        }
    ],
    "outbounds": [
        {
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": host,
                        "port": int(port),
                        "users": [
                            {
                                "id": uuid,
                                "encryption": "none",
                                "flow": get("flow")
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": get("type"),
                "security": get("security"),
                "realitySettings": {
                    "publicKey": get("pbk"),
                    "shortId": get("sid"),
                    "serverName": get("sni"),
                    "fingerprint": get("fp"),
                    "spiderX": urllib.parse.unquote(get("spx") or "/")
                }
            }
        }
    ]
}

Path("/gen").mkdir(parents=True, exist_ok=True)
with open("/gen/config.json", "w") as f:
    json.dump(config, f, indent=2)