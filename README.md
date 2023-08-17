# Proxmox_Create_lxc_API

This script automates the process of creating a Proxmox LXC container by interacting with the Proxmox API. It prompts the user for various container parameters and performs the necessary API calls to create the container on the specified Proxmox node.

## Prerequisites

- Python 3.x
- `requests` library: You can install it using `pip install requests`

## Usage

1. Clone this repository or download the script directly.

2. Install the required `requests` library if you haven't already:

   ```bash
   pip install requests

3. Update the script with your Proxmox server details and API token:

-  proxmox_server = "PROXMOX SERVER IP:8006"
-  api_token = "USERNAME@pam!TOKEN_NAME=API TOKEN"

4. Update the image based on your preference:

-  ostemplate = "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst"

5. Run the script:

   ```bash
   python create_lxc_container.py

6. Follow the prompts to provide the container parameters:

- Container name
- Desired RAM (in MB)
- Hostname
- Password
- Number of CPU cores
- Swap size (in MB)
- Disk size (in GB)
- Image name (e.g., ubuntu-22.04-standard_22.04-1_amd64.tar.zst)
- The script will interact with the Proxmox API to create the LXC container based on the provided parameters.

## Important Notes
- Ensure that your Proxmox server is reachable and accessible from the machine running this script.
- Make sure to provide accurate and valid parameters when prompted.
- The script uses the Proxmox API to create the LXC container, so make sure you have the necessary permissions and the API token is correctly configured.


## Disclaimer
This script interacts with the Proxmox API and performs administrative tasks on your Proxmox server. Use it at your own risk and ensure you understand the actions it takes.
