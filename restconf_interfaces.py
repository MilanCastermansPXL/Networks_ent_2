import requests
import json

router = "https://192.168.1.56"
auth = ("admin", "cisco123")

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# BASE
router = "https://<your-router-ip>"

# 1. GigabitEthernet1 configuratie
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

# 2. GigabitEthernet2 disable
url = f"{router}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"
payload = {
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet2",
        "enabled": False
    }
}

# 3. Loopback0 configuratie
url = f"{router}/restconf/data/ietf-interfaces:interfaces/interface=Loopback0"
payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback0",
        "type": "iana-if-type:softwareLoopback",
        "description": "loopback made via RESTCONF",
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

# 4. Hostname instellen
url = f"{router}/restconf/data/ietf-system:system/hostname"
payload = {
    "ietf-system:hostname": "Router1"
}

# 5. Banner MOTD
url = f"{router}/restconf/data/Cisco-IOS-XE-native:native/banner"
payload = {
    "Cisco-IOS-XE-native:banner": {
        "motd": {
            "banner": "Authorized access only!"
        }
    }
}

# 6. User authentication
url = f"{router}/restconf/data/ietf-system:system/authentication/user"
payload = {
    "ietf-system:user": [
        {
            "name": "admin",
            "password": "password123"
        }
    ]
}

# 7. VLAN 10 aanmaken
url = f"{router}/restconf/data/Cisco-IOS-XE-native:native/vlan"
payload = {
    "Cisco-IOS-XE-vlan:vlan": {
        "vlan-list": [
            {
                "id": 10,
                "name": "Students"
            }
        ]
    }
}

# 8. Switchport GigabitEthernet3 VLAN assignment
url = f"{router}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=3"
payload = {
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": "3",
        "switchport-config": {
            "switchport": {
                "mode": {
                    "access": {}
                },
                "access": {
                    "vlan": {
                        "vlan": 10
                    }
                }
            }
        }
    }
}



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
