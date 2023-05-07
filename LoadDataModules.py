from itertools import cycle
import variables
import json


def LoadWorldProxies():
    with open("data/world_proxies.json") as f:
        json_ = json.load(f)
        for proxy in json_:
            ip = proxy["ip"]
            port = proxy["port"]
            variables.WORLD_PROXIES.append(f"{ip}:{port}")

def LoadLocalProxies():
    with open("data/local_proxies.json") as f:
        json_ = json.load(f)
        for proxy in json_:
            ip = proxy["ip"]
            port = proxy["port"]
            protocol = proxy["protocols"][0]
            append = [f"{ip}:{port}", protocol]
            variables.LOCAL_PROXIES.append(append)
        variables.PROXY_POOL = cycle(variables.LOCAL_PROXIES)

LoadWorldProxies()
LoadLocalProxies()