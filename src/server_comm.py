# server_comm.py

import socket

class AccessControl:
    def __init__(self):
        self.role_permissions = {
            "user": ["read"],
            "admin": ["read", "write"]
        }
    
    def has_permission(self, role, action):
        return action in self.role_permissions.get(role, [])
    
class ServerCommunicator:
    def __init__(self):
        self.server_address = ('127.0.0.1', 8080)
        self.client_socket = None
        self.vm_roles = {} # Dictionnaire pour stocker les rôles des machines virtuelles
        self.access_control = AccessControl()

    def connect(self):
        # Code pour établir une connexion avec le server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("Connexion établie avec le serveur.")
    
    def disconnect(self):
        # Code pour fermer la connexion avec le serveur
        if self.client_socket:
            self.client_socket.close()
            print("connexion avec le serveur fermée.")
        
    def send_data(self, data, vm_name):
        # Code pour envoyer des données au serveur
        if self.client_socket:
            role = self.vm_roles.get(vm_name, "user")
            if self.access_control.has_permission(role, "write"):
                self.client_socket.sendall(data.encode('utf-8'))
                print(f"Données envoyées au serveur depuis {vm_name} avec le rôle {role} : {data}")
            else:
                print(f"L'accès en écriture n'est pas autorisé pour {vm_name} avec le rôle {role}.")   
    
    def allow_access(self, vm_name, roles="user"):
        # Code pour autoriser l'accès au serveur pour une machine virtuelle spécifique
        if vm_name not in self.vm_roles:
            self.vm_roles[vm_name] = roles
            self.allowed_vms.add(vm_name)
            print(f"L'accès au serveur a été autorisé pour {vm_name} avec le rôle {roles}.")
        else:
            print(f"L'accès au serveur pour {vm_name} est déjà authorisé avec le rôle {self.vm_roles[vm_name]}.")
    
    def deny_access(self, vm_name):
        # Code pour refuser l'accès au serveur pour une machine virtuelle spécifique
        if vm_name in self.vm_roles:
            del self.vm_roles[vm_name]
            print(f"L'accès au serveur a été refusé pour {vm_name}.")
        else:
            print(f"L'accès au serveur pour {vm_name} n'est pas autorisé.")