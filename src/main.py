#main.py

from vm_manager import VMManager
from network_admin import NetworkAdmin
from server_comm import ServerCommunicator

def main():
    # Module initialization 
    vm_manager = VMManager()
    network_admin = NetworkAdmin()
    server_comm = ServerCommunicator()
    
    try:
        # Creation of virtual machines 
        vm_manager.create_vm("vm1", memory=1024, vcpu=1,)
        vm_manager.create_vm("vm2", memory=2048, vcpu=2,)
        # Deployment of virtual machines
        vm_manager.deploy_vms()
        
        # Network configuration of virtual machines
        network_admin.configure_network()
        
        # Communication with the server
        server_comm.connect()
        server_comm.send_data("Data to send to server")
        
        # Example of server access management for a specific virtual machine
        server_comm.allow_access("vm1")
        server_comm.deny_access("vm2")
    except Exception as e:
        print(f"Error executing program: {e}")
    
    finally: 
        # # Disconnect from server
        server_comm.disconnect()
if __name__ == "__main__": # Correction here
    main()      