from netmiko import ConnectHandler
import re

device_backup_commands = {
    "aruba_os": "show running-config",
    "brocade_icx": "show config",
    "cisco_ios": "show run",
    "dell_force10": "show running-config",
    "fortinet": "show full-configuration",
    "huawei": "display current-configuration",
    "juniper": "show configuration",
    "paloalto_panos": "show running-config",
    "ruijie": "display current-configuration",
}

device_hostname_commands = {
    "aruba_os": { "cmd": "show running-config | include hostname", "index": 1 },
    "brocade_icx": { "cmd": "show hostname", "index": 1 },
    "cisco_ios": { "cmd": "show run | include hostname", "index": 1 },
    "dell_force10": { "cmd": "show running-config | grep hostname", "index": 1 },
    "fortinet": { "cmd": "get system global | grep -f hostname", "index": 5 },
    "huawei": { "cmd": "display current-configuration | include sysname", "index": 1 },
    "juniper": { "cmd": "show configuration system host-name", "index": 1 },
    "paloalto_panos": { "cmd": "show system info | match hostname", "index": 1 },
    "ruijie": { "cmd": "display run | include hostname", "index": 1 },
}

# ---- Get Device Backup ----
def get_netmiko_connection(device):
    inner_device = {
        "ip": device["ip_address"],
        "username": device["username"],
        "password": device["password"],
        "secret": device["enable_password"],
        "device_type": device["device_type"]
    }

    return ConnectHandler(**inner_device)

def get_device_backup(connection, device_type):
    try:
        connection.enable()
        config = connection.send_command_timing(device_backup_commands[device_type])
        if "Do you want to show sensitive information" in config:
            config = connection.send_command_timing("y")
        return config
    except Exception as e:
        return f"Error: {e}"

# ---- Get Device Hostname ----
def get_device_hostname(connection, device_type):
    # Commen out first if block if not needed
    if device_type == "aruba_os":
        command = "show running-config"
        out = connection.send_command_timing(command)
        if "Do you want to show sensitive information" in out:
            out = connection.send_command_timing("y")
        host = re.search(r'^hostname\s+(\S+)', out, re.MULTILINE)
        if host:
            hostname = host.group(1)
            return hostname
    if device_type in device_hostname_commands.keys():
        command = device_hostname_commands[device_type]['cmd']
        index = device_hostname_commands[device_type]['index']
    else:
        raise ValueError("Invalid device type")
    output = connection.send_command(command)
    device_hostname = output.split()[index]
    return device_hostname
