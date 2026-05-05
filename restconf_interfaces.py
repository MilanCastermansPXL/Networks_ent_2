import requests
import json

router = "https://192.168.1.10"
auth = ("admin", "cisco123")

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# 1. CONFIGURATIE PUSHEN (interface GigabitEthernet1)
payload = {
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet1",
        "description": "Configured via RESTCONF",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.10.10.1",
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
}

url = f"{router}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1"

response = requests.put(
    url,
    auth=auth,
    headers=headers,
    data=json.dumps(payload),
    verify=False
)

print("STATUS CODE:", response.status_code)
print(response.text)

# 2. OPERATIONAL DATA OPHALEN
url_get = f"{router}/restconf/data/ietf-interfaces:interfaces"

response_get = requests.get(
    url_get,
    auth=auth,
    headers=headers,
    verify=False
)

print("\n--- CURRENT CONFIG ---")
print(json.dumps(response_get.json(), indent=4))
