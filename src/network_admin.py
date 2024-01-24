#network_admin.py
import json
import paramiko
import time 
import logging

class NetworkAdmin:
    # Initialization of NetworkAdmin object
    def __init__(self, net_config_file="net_config.json"):
        self.net_config_file = net_config_file
        self.result = {"status": False, "message": ""}
    # Read network configuration from file    
    def read_network_configuration(self):
        try:
            with open(self.net_config_file, "r") as file:
                return json.load(file) # Load JSON data
        except FileNotFoundError as e:
            print(f"Error reading network configuration file: {e}")
            return []
        except Exception as e:
            print(f"Error reading network configuration file : {e}")
            return[]                 
    # Connect to switch using Paramiko SSH client
    def connect_to_switch(self, ip_address, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=username, password=password)
            return ssh
        except Exception as e:
            print(f"Error connecting to switch {ip_address}: {e}")
            return None
    
    # Execute command on switch        
    def execute_command_on_switch(self, ssh, command):
        try:
            stdout = ssh.exec_command(command)
            return stdout.read().decode("utf-8") # Read output
        except Exception as e:
            print(f"Error executing command {command}: {e}")
           
    def close_connection(self, ssh):
        # Code to close the SSH connection
        try:
            if ssh is not None:
                ssh.close()
        except Exception as e:
            print(f"Error closing SSH connection: {e}")
    
    def execute_command_on_vm(self, cmd):
       # Runs a command on the virtual machine and returns the output
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode("utf-8").strip()
            error = stderr.read().decode("utf-8").strip()
            if error:
                    print(f"Error executing command '{cmd}': {error}")
            return output
        finally:
            client.close()

    
    
    # Code to configure the SSH virtual machine network (Paramiko)
    
    class SSH: 
        def __init__(self, ip_address, username, password):
            self.ip_address = ip_address
            self.username = username
            self.password = password
         
        def configure_network(self):
            try: 
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(self.ip_address, username=self.username, password=self.password) 
                cmd1 = "ifconfig eth0 down; ifconfig eth0 up;"
                cmd2 = "sudo dh_client -r eth0; sudo dh_client eth0-cf /etc/dhcp3/dh_client.conf; echo 'Network configured successfully.'"
                try:
                    _, stdout, stderr = client.exec_command(cmd1 + cmd2)
                    output = stdout.read().decode("utf-8").strip()
                    error = stderr.read().decode("utf-8").strip()
                    if error:
                        print("error")
                        logging.error(f"error: {error}")
                    else:
                        print(output)
                except Exception as e:
                        print(f"Exception: {e}")
                        logging.exception(e)               
                finally:
                    client.close()        
            except Exception as e:
                print(f"Exception: {e}")
                logging.exception(e)
    logging.basicConfig(filename='ssh_conn.log', level=logging.DEBUG)                   
                