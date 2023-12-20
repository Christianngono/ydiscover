# server_comm.py

import socket
import os

class AccessControl:
    def __init__(self):
        self.role_permissions = {"user": ["read"], "admin": ["read", "write"]}
            
    def has_permission(self, role, action):
        return action in self.role_permissions.get(role, [])
class UserInterface:
    def __init__(self, host='localhost', port=12345):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self.sock
    def connect(self):
        try:
            self.sock.connect(host='localhost', port=12345)
            print("Connected to the server.")
        except Exception as e:
            # handle connection errors
            print(f"Failed to connect to the server. Error: {e}")
    def send_message(self, message):
        if not isinstance(message, str):
            raise TypeError('Message must be a string')
        else:
            self.sock.sendall(message.encode())
            
    def receive_message(self, message):
        data = self.sock.recv(1024).decode()
        return data
    def close_connection(self):
        self.sock.close()            
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
                
    # Recevoir des données du serveur
    def receive_data(self):
        if self.client_socket:
            received_data = self.client_socket.recv(4096).decode('utf-8')
            if len(received_data) > 0:
                print(f"Reçu de la part du serveur : {received_data}")
                return received_data
            else:
                print("La communication est terminée.")
                self.disconnect()
                

    # Envoyer les données du serveur
    def send_file(self, filepath, filename=None):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Le fichier {filepath} n'existe pas.")
        elif not os.path.isfile(filepath):
            raise IsADirectoryError(f"{filepath} n'est pas un fichier.")
        else:
            with open(filepath, 'rb') as f:
                filesize = os.path.getsize(filepath)
                if filename is None:
                    filename = os.path.basename(filepath)
                    header = f"SendFile:{os.path.join(os.path.dirname(filepath), filename)}:{filesize}"
                else:
                    header = f"SendFile:{os.path.join(os.path.dirname(filepath), filename)}:{filesize}"
                
                # Envoyer le header avant de transmettre le fichier
            self.client_socket.send(header.encode('utf-8'))
            if self.recv_confirmation():
                data = f.read(4096)
                while data:
                    self.client_socket.send(data)
                    data = f.read(4096)    
        print(f"Fichier {filename} envoyé.")
    def recv_confirmation(self):
        confirmation = self.client_socket.recv(4096).decode('utf-8')
        if confirmation == "ReadyToReceive":
            return True
        else:
            raise ConnectionError("Erreur de confirmation du serveur.")
            return False
                    
    # Obtenir la liste des machines virtuelles autorisées
    def get_allowed_vms(self):
        # Code pour obtenir la liste des machines virtuelles autorisées
        allowed_vms = list(self.vm_roles.keys())
        allowed_vms = []
        for vm in allowed_vms:
            if self.access_control.has_permission("admin", "read") or self.access_control.has_permission(self.vm_roles[vm], "read"): allowed_vms.append(vm)
            return allowed_vms
        
    def set_vm_role(self, vm_name, role):
        """Ajoute ou modifie un couple nom - rôle d'une machine virtuelle"""
        self.vm_roles[vm_name] = role
        print(f"Le rôle de {vm_name} a été défini sur {role}.")
    
    # Obtenir la liste des permissions associées à un rôle donné à une machine virtuelle spécifique   
    def get_vm_role_permissions(self, role):
        try:
            vms_with_this_role = [k for k, v in self.vm_roles.items() if v == role and k in self.access_control.roles]
            return vms_with_this_role
        except KeyError as e:
            raise ValueError(f"Rôle '{e}' inconnu.")
        
    # Obtenir les anciens et nouveaux rôles pour machine virtuelle spécifique
    def update_vm_role(self, old_vm, new_vm):
        if old_vm not in self.vm_roles and new_vm not in self.vm_roles:
            raise ValueError("Aucune modification ne peut être apportée à un nouveau ou ancien VM.")
        elif old_vm in self.vm_roles and new_vm not in self.vm_roles:
            del self.vm_roles[old_vm]
            print(f"Le rôle de l'ancienne VM '{old_vm}' a été supprimé.")
        elif old_vm not in self.vm_roles and new_vm in self.vm_roles:
            self.vm_roles[new_vm] = 'admin'
            print(f"Le rôle de la nouvelle VM '{new_vm}' a été ajouté.")
        else:
            print(f"Le rôle de la nouvelle VM '{new_vm}' a été ajouté.")
                
    # Obtenir les rôles autorisés pour une machine virtuelle spécifique
    def get_vm_roles(self, vm_name):
        roles = self.vm_roles.get(vm_name, [])
        return roles
    
    # Changer le rôle d'une machine virtuelle autorisée
    def change_vm_role(self, vm_name, new_role, old_roles):
        # Code pour changer le rôle d'une machine virtuelle autorisée
        if vm_name in self.vm_roles:
            if new_role not in old_roles:
                self.vm_roles[vm_name] = new_role
                print(f"Le rôle de {vm_name} a été modifié à {new_role}.")
            else:
                print(f"l'accès au serveur pour {vm_name} n'est pas autorisé.")
                   
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