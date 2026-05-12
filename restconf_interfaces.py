import requests
import json
import urllib3

urllib3.disable_warnings()

# Router info
router = "https://192.168.1.56"
auth = ("admin", "cisco123")

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Function to push config
def push_config(url, payload):
    response = requests.put(
        url,
        auth=auth,
        headers=headers,
        data=json.dumps(payload),
        verify=False
    )

    print(f"\nURL: {url}")
    print("STATUS:", response.status_code)

    if response.text:
        print(response.text)

# 1. GigabitEthernet1
url = f"{router}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1"

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

push_config(url, payload)

# 2. Disable GigabitEthernet2
url = f"{router}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"

payload = {
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet2",
        "enabled": False
    }
}

push_config(url, payload)

# 3. Loopback0
url = f"{router}/restconf/data/ietf-interfaces:interfaces/interface=Loopback0"

payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback0",
        "type": "iana-if-type:softwareLoopback",
        "description": "Loopback via RESTCONF",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.10.1.1",
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
}

push_config(url, payload)

# 4. Hostname
url = f"{router}/restconf/data/Cisco-IOS-XE-native:native/hostname"

payload = {
    "Cisco-IOS-XE-native:hostname": "Router1"
}

push_config(url, payload)

# 5. Banner MOTD
url = f"{router}/restconf/data/Cisco-IOS-XE-native:native/banner"

payload = {
    "Cisco-IOS-XE-native:banner": {
        "motd": {
            "banner": "Authorized access only!"
        }
    }
}

push_config(url, payload)

# 6. Create VLAN 10
url = f"{router}/restconf/data/Cisco-IOS-XE-native:native/vlan"

payload = {
    "Cisco-IOS-XE-native:vlan": {
        "vlan-list": [
            {
                "id": 10,
                "name": "Students"
            }
        ]
    }
}

push_config(url, payload)

# 7. Assign VLAN to GigabitEthernet3
url = f"{router}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=3"

payload = {
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": "3",
        "switchport": {
            "mode": {
                "access": {}
            },
            "access": {
                "vlan": 10
            }
        }
    }
}

push_config(url, payload)

# GET current interfaces
url_get = f"{router}/restconf/data/ietf-interfaces:interfaces"

response_get = requests.get(
    url_get,
    auth=auth,
    headers=headers,
    verify=False
)
print("\n--- CURRENT CONFIG ---")
print(json.dumps(response_get.json(), indent=4))
