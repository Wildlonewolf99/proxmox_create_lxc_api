import os
import requests

# Proxmox server details
proxmox_server = "https://192.168.101.14:8006"
api_token = "root@pam!Praveen_API=478ecf40-8eb0-4fac-bc16-84a2bdb327c1"

# Headers for authentication
headers = {
    "Authorization": f"PVEAPIToken={api_token}",
    "Content-Type": "application/json"
}

# API endpoint for getting the next available VMID
vmid_url = f"{proxmox_server}/api2/json/cluster/nextid"

# Make the API request to get the next available VMID
response = requests.get(vmid_url, headers=headers,  verify=False)

if response.status_code == 200:
    vmid = response.json().get("data")
    if vmid is not None:
        print(f"Next available VMID: {vmid}")
    else:
        print("No VM ID found in the response.")
        print(response.text)  # Print the response text for troubleshooting

    # Export variables
    os.environ["APINODE"] = "192.168.101.14"
    os.environ["TARGETNODE"] = "wildlonewolfprox"

    # Step 2: Save an Authorization Cookie on the Filesystem
    auth_url = f"https://{os.environ['APINODE']}:8006/api2/json/access/ticket"
    auth_data = {
        "username": "root@pam",
        "password": "Praveen_99"
    }

    response = requests.post(auth_url, data=auth_data, verify=False)
    if response.status_code == 200:
        cookie = f"PVEAuthCookie={response.json()['data']['ticket']}"
        with open("cookie", "w") as file:
            file.write(cookie)

        csrf_token = response.json()["data"]["CSRFPreventionToken"]
        with open("csrftoken", "w") as file:
            file.write(f"CSRFPreventionToken: {csrf_token}")

        # Prompt user for container parameters
        container_name = input("Enter the container name: ")
        ram = input("Enter desired RAM (MB): ")
        hostname = input("Enter hostname: ")
        password = input("Enter password: ")
        cpu_cores = input("Enter number of CPU cores: ")
        swap = input("Enter swap size (MB): ")
        disk_size = input("Enter disk size (GB): ")

        # Step 4: Test auth credentials
        status_url = f"https://{os.environ['APINODE']}:8006/api2/json/nodes/{os.environ['TARGETNODE']}/status"
        headers = {
            "Cookie": cookie
        }

        status_response = requests.get(status_url, headers=headers, verify=False)
        print("Node Status:")
        print(status_response.json())

        # Step 5: Creates a LXC Container
        container_url = f"https://{os.environ['APINODE']}:8006/api2/json/nodes/{os.environ['TARGETNODE']}/lxc"
        headers = {
            "Cookie": cookie,
            "CSRFPreventionToken": csrf_token
        }
        data = {
            "net0": "bridge=vmbr0,name=eth0,ip=dhcp,ip6=dhcp",
            "ostemplate": "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst",
            "vmid": vmid,
            "hostname": container_name,
            "memory": int(ram),
            "password": password,
            "cores": int(cpu_cores),
            "swap": int(swap),
            "rootfs": f"local:{disk_size}"
        }

        container_response = requests.post(container_url, headers=headers, data=data, verify=False)
        print("Container Creation Response:")
        print(container_response.json())
    else:
        print("Failed to authenticate.")
else:
    print("Failed to retrieve next available VMID.")
