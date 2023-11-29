#network_admin.py

import paramiko

class NetworkAdmin:
    def __init__(self):
        pass
    
    def configure_networks(self):
        # Code pour configurer le réseau des machines virtuelles SSH (Paramiko)
        vm_configurations = [
            {"name": "vm1", "ip_address": "192.168.1.101", "username": "user", "password": "password"},
            {"name":"vm2", "ip_address": "192.168.1.102", "username": "user", "password": "password"},
            # Ajouter d'autres configurations réseau selon nos besoins
        ]
        
        for config in vm_configurations:
            self.configure_network(config["name"], config["ip_address"], config["username"], config["password"])
    
    def configure_network(self, vm_name, ip_address, username, password):
        # Configure l'adresse IP de la machine virtuelle via SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            client.connect(ip_address, username=username, password=password)
            command = f"echo -e 'auto ens3\niface ens3 inet dhcp' | sudo tee ./network/interfaces.d/ens3.cfg"
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode('utf-8'))
        
        except paramiko.AuthentificationException as e:
            print(f"Erreur d'authentification pour {vm_name}: {e}")
        except Exception as e:
            print(f"Erreur lors de la configuration réseau de {vm_name}: {e}")
        
        finally:
            client.close()
        