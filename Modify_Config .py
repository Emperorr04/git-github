import os
from getpass4 import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

#ensure input files are in correct directory
os.chdir("D:\PP\Python")

#accept credentials
username = input("Enter your SSH username: ")
password = getpass("input password: ")


#set of configs and device IPs
with open("commands_file_cisco") as f:
    commands_file_cisco = f.read().splitlines()

with open("commands_file_junos") as f:
    commands_file_junos = f.read().splitlines()

with open("devices_file") as f:
    devices_list = f.read().splitlines()

for devices in devices_list:
    print ("connecting to device" + devices )
    device_ip_type = devices.split(',')
    ip_address_of_device = device_ip_type[0]
    device_type  = device_ip_type[1]
    #router_or_switch = device_ip_type[2]
    ios_device = {"device_type": device_type,
                  "ip": ip_address_of_device,
                  "username": username,
                  "password": password
                  }
    #check for errors
    with open('log.txt', 'a') as f:   ###double check here for append and write
        try:
            net_connect = ConnectHandler(**ios_device)
        except (AuthenticationException):
            print (f"Authentication failure:  + {ip_address_of_device}")
            f.write(f"Authentication failure:  + {ip_address_of_device}\n")
            continue
        except (NetmikoTimeoutException):
            print (f"Timeout to device:  + {ip_address_of_device}")
            f.write(f"Timeout to device:  + {ip_address_of_device}\n")
            continue
        except (EOFError): #check what EOF error mean
            print (f"End of file while attempting device  + {ip_address_of_device}")
            f.write(f"End of file while attempting device:  + {ip_address_of_device}\n")
            continue
        except (SSHException):
            print(f"SSH Issue. Are you sure SSH is enabled?  + {ip_address_of_device}")
            f.write(f"SSH Issue. Are you sure SSH is enabled?  + {ip_address_of_device}\n")
            continue
        except Exception as unknown_error:
            print(f"Some other error:  + {unknown_error}")
            f.write(f"SSH Issue. Are you sure SSH is enabled?  + {unknown_error}\n")
            continue


    #check for the version to know which command set to input
    list_versions = ["vios_l2-ADVENTERPRISEK9-M",
                     "C1900-UNIVERSALK9-M",
                     "13.3R1.4",
                     "15.3R1.4"]

    for software_ver in list_versions:
        print (f"checking for + {software_ver}")
        output_version = net_connect.send_command("show version")
        int_version = 0  # Reset integer value
        int_version = output_version.find(software_ver)
        if int_version > 0:
            print (f"Software version found:  + {software_ver}")
            break
        else:
            print (f"Did not find + {software_ver}")


    if software_ver == "vios_l2-ADVENTERPRISEK9-M":
        print (f"Running + {software_ver} + commands")
        output = net_connect.send_config_set(commands_file_cisco)
    elif software_ver == "VIOS-ADVENTERPRISEK9-M":
        print(f"Running + {software_ver} + commands")
        output = net_connect.send_config_set(commands_file_cisco)
    elif software_ver == "13.3R1.4":
        print(f"Running + {software_ver} + commands")
        output = net_connect.send_config_set(commands_file_junos)
    elif software_ver == "15.3R1.4":
        print(f"Running + {software_ver} + commands")
        output = net_connect.send_config_set(commands_file_junos)

    print(output)





