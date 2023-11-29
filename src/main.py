#main.py

from vm_manager import VMManager
from network_admin import NetworkAdmin
from server_comm import ServerCommunicator

def main():
    #Initialisation des modules 
    vm_manager = VMManager()
    network_admin = NetworkAdmin()
    server_comm = ServerCommunicator()
    
    try:
        # Création des machines virtuelles 
        vm_manager.create_vm("vm1", memory=1024, vcpu=1, disk_size=10)
        vm_manager.create_vm("vm2", memory=2048, vcpu=2, disk_size=20)
        
        # Déploiement des machines virtuelles
        vm_manager.deploy_vms()
        
        # Configuration réseau des machines virtuelles
        network_admin.configure_networks()
        
        # Communication avec le serveur
        server_comm.connect()
        server_comm.send_data("Données à envoyer au serveur")
        
        # Exemple de gestion d'accès au serveur pour une machine virtuelle spécifique
        server_comm.allow_access("vm1")
        server_comm.deny.access("vm2")
    except Exception as e:
        print(f"Erreur dans l'exécution du programme : {e}")
    
    finally: 
        # Déconnexion du serveur
        server_comm.disconnect()
if __name__ == "__name__":
    main()      