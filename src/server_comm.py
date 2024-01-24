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
            
    def receive_message(self):
        data = self.sock.recv(1024).decode()
        return data
    def close_connection(self):
        self.sock.close()            
class ServerCommunicator:
    def __init__(self):
        self.server_address = ('127.0.0.1', 8080)
        self.client_socket = None
        self.vm_roles = {} # Dictionary to store virtual machine roles
        self.access_control = AccessControl()

    def connect(self):
        # Code to establish a connection with the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("Connection established with server.")
    
    def disconnect(self):
        # Code to close the connection with the server
        if self.client_socket:
            self.client_socket.close()
            print("connection to server closed.")
        
    def send_data(self, data, vm_name):
        # Code to send data to server
        if self.client_socket:
            role = self.vm_roles.get(vm_name, "user")
            if self.access_control.has_permission(role, "write"): 
                self.client_socket.sendall(data.encode('utf-8'))
                print(f"Data sent to the server from {vm_name} with the role {role} : {data}")
            else:
                print(f"Write access is not allowed for {vm_name} with the role {role}.")
                
   # Receive data from server
    def receive_data(self):
        if self.client_socket:
            received_data = self.client_socket.recv(4096).decode('utf-8')
            if len(received_data) > 0:
                print(f"Received from the server: {received_data}")
                return received_data
            else:
                print("Communication is over.")
                self.disconnect()
                

    # Send data from server
    def send_file(self, filepath, filename=None):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"the file {filepath} does not exist.")
        else:
            with open(filepath, 'rb') as f:
                filesize = os.path.getsize(filepath)
                if filename is None:
                    filename = os.path.basename(filepath)
                    header = f"SendFile:{os.path.join(os.path.dirname(filepath), filename)}:{filesize}"
                else:
                    header = f"SendFile:{os.path.join(os.path.dirname(filepath), filename)}:{filesize}"
                
                # Send the header before transmitting the file
            self.client_socket.send(header.encode('utf-8'))
            if self.recv_confirmation():
                data = f.read(4096)
                while data:
                    self.client_socket.send(data)
                    data = f.read(4096)    
        print(f"{filename}")
    def recv_confirmation(self):
        confirmation = self.client_socket.recv(4096).decode('utf-8')
        if confirmation == "ReadyToReceive":
            return True
        else:
            raise ConnectionError("Server confirmation error.")
                    
    # Get the list of authorized virtual machines
    def get_allowed_vms(self):
        # Code to get the list of authorized virtual machines
        allowed_vms = []
        for vm in allowed_vms:
            if self.access_control.has_permission("admin", "read") or self.access_control.has_permission(self.vm_roles[vm], "read"): allowed_vms.append(vm)
            return allowed_vms
        
    def set_vm_role(self, vm_name, role):
        """Adds or modifies a name - role pair of a virtual machine"""
        self.vm_roles[vm_name] = role
        print(f"role of {vm_name} has been changed {role}.")
    
    # Obtain the list of permissions associated with a given role to a specific virtual machine
    def get_vm_role_permissions(self, role):
        try:
            vms_with_this_role = [k for k, v in self.vm_roles.items() if v == role and k in self.access_control.roles]
            return vms_with_this_role
        except KeyError as e:
            raise ValueError(f"role '{e}' unknown.")
        
    # Get old and new roles for specific virtual machine
    def update_vm_role(self, old_vm, new_vm):
        if old_vm not in self.vm_roles and new_vm not in self.vm_roles:
            raise ValueError("No changes can be made to a new or old VM.")
        elif old_vm in self.vm_roles and new_vm not in self.vm_roles:
            del self.vm_roles[old_vm]
            print(f"The role of the old VM '{old_vm}' has been removed.")
        elif old_vm not in self.vm_roles and new_vm in self.vm_roles:
            self.vm_roles[new_vm] = 'admin'
            print(f"The role of the new VM '{new_vm}' has been added.")
        else:
            print(f"The role of the new VM '{new_vm}' has been added.")
                
    # Get allowed roles for a specific virtual machine
    def get_vm_roles(self, vm_name):
        roles = self.vm_roles.get(vm_name, [])
        return roles
    # Change the role of an authorized virtual machine
    def change_vm_role(self, vm_name, new_role, old_roles):
        # Code to change the role of an authorized virtual machine
        if vm_name in self.vm_roles:
            if new_role not in old_roles:
                self.vm_roles[vm_name] = new_role
                print(f"The role of {vm_name} has been changed to {new_role}.")
            else:
                print(f"server access for {vm_name} is not allowed.")
                   
    def allow_access(self, vm_name, roles="user"):
        # Code to allow server access for a specific virtual machine
        if vm_name not in self.vm_roles:
            self.vm_roles[vm_name] = roles
            self.allowed_vms.add(vm_name)
            print(f"Access to the server has been authorized for {vm_name} with the role {roles}.")
        else:
            print(f"Access to the server for {vm_name} is already authorized with the role {self.vm_roles[vm_name]}.")
    
    def deny_access(self, vm_name):
        # Code to deny server access for a specific virtual machine
        if vm_name in self.vm_roles:
            del self.vm_roles[vm_name]
            print(f"Access to the server has been denied for {vm_name}.")
        else:
            print(f"Server access for {vm_name} is not permitted.")