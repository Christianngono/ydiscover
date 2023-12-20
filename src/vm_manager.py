# vm_manager.py

import libvirt


class VMManager:
    def __init__(self):
        self.conn = libvirt.open('qemu:///system')
        
        if self.conn is None:
            raise Exception("Echec de la connexion")
    
    def create_vm(self, vm_name, memory=1024, vcpu=1, disk_size=10):
        # Code pour créer la machine virtuelle avec libvirt(QEMU/KVM)
        xml_disc = f"""
            <domain type='kvm'>
                <name>{vm_name}</name>
                <memory unit='KiB'>{memory * 1024}<memory>
                <vcpu placement='static'>{vcpu}</vcpu>
                <!-- Ajouter d'autres configurations selon nos besoins -->
            </domain>
        """
        
        try:
            dom = self.conn.createXML(xml_disc, 0)
            print(f"La machine virtuelle {vm_name} a été créée avec succès.")
            return dom
        except libvirt.libvirtError as e:
            print(f"Erreur lors de la création de la machine virtuelle {vm_name}: {e}")
            raise
    def deploy_vms(self):
        # Code pour démarrer les machines virtuelles
        domains = self.conn.listDomainsID()
        for dom_id in domains:
            dom = self.conn.lookupByID(dom_id)
            dom.create()
            
    def list_vms(self):
        # Code pour afficher une liste des machines virtuelles
        domains = self.conn.listAllDomains()
        for dom_id in domains:
            dom = self.conn.lookupByID(dom_id)
            print(f"Machine virtuelle: {dom.name()}")    
        print(f"Statut: {dom.state()[0]}")
            
    def start_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.create()
            print(f"La machine virtuelle {vm_name} a été démarrée avec succès.")
        except libvirt.libvirtError as e:
            print(f"Impossible de trouver ou de démarrer la machine virtuelle {vm_name}.\nDétails : \n{e}")
            raise
    def stop_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.destroy()
            print(f"La machine virtuelle {vm_name} a bien été arrêtée.")
        except libvirt.libvirtError as e:
            print(f"Impossible d'arrêter la machine virtuelle {vm_name}.\nDétails : \n{ e}")
            raise
    def undefine_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.undefine()
            print(f"La machine virtuelle {vm_name} a été définie avec succès.")
        except libvirt.libvirtError as e:
            print(f"Erreur lors de la suppression de la machine virtuelle {vm_name}: {e}")
            raise 
    # fermer la connexion avec l'hyperviseur
    def close_connection(self):
        # Fermeture de la connexion à l'hyperviseur
        if self.conn != None:
            self.conn.close()
            print("La connexion avec l'hyperviseur a été fermée.")
    # Obtenir l'état actuel de la machine virtuelle        
    def get_vm_state(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            state, reason = dom.state()
            print(f"Machine virtuelle {vm_name} - État: {libvirt.VIR_DOMAIN_STATE[state]} ({reason})")
            return state
        except libvirt.libvirtError as e:
            print(f"Impossible d'obtenir l'état de la machine virtuelle {vm_name}.\nDétails : \n{e}")
            raise
    # Ajouter des disques supplémentaires à une machine virtuelle existante
    def add_disk(self, vm_name, disk_path, disk_dev, bus='ide'):
        try:
            # Récupérer la machine virtuelle
            dom = self.conn.lookupByName(vm_name)
            # Créer le nouvel élément de disque
            xml_desc = f"""
                <!-- Ajoutez ici la configuration du disque supplémentaire selon vos besoins -->
            """
            dom.attachDevice(xml_desc)
            print(f"Disque ajouté avec succès à la machine virtuelle {vm_name}.")
        except libvirt.libvirtError as e:
            print(f"Une erreur est survenue pendant l'ajout du disque à la machine virtuelle {vm_name}: {e}")
            raise
    # Créer les snapshots des machines virtuelles
    def create_snapshot(self, vm_name, snapshots_name):
        try:
            # Récupérer la machine virtuelle
            dom = self.conn.lookupByName(vm_name)
            for snapshot in snapshots_name:
                # Création d'un snapshot
                dom.snapshotCreateXML(f"""<domainsnapshot><name>{snapshot}</name></domainsnapshot>""", 0)
            print(f"Snapshot '{snapshots_name}' créé pour la machine virtuelle {vm_name}.")
            return snapshot
        except libvirt.libvirtError as e:
            print(f"Impossible de créer le/les snapshot(s) pour la machine virtuelle {vm_name}\nDétails : \n{e}")
            raise
    # lister les snapshots
    def list_snapshots(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            snapshots = dom.listSnapshots()
            print(f"Liste des snapshots pour la machine virtuelle {vm_name}: {snapshots}")
            return snapshots
        except libvirt.libvirtError as e:
            print(f"Erreur lors de la récupération des snapshots pour la machine virtuelle {vm_name}: {e}")
            raise
    # restaurer les snapshots de machines virtuelles
    def restore_from_snapshot(self, vm_name, snapshot_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            snapshot = dom.snapshotLookupByName(snapshot_name, 0)
            snapshot.revertToSnapshot(0)
            print(f"Snapshot {snapshot_name} restauré avec succès pour la machine virtuelle {vm_name}.")
        except libvirt.libvirtError as e:
            print(f"Erreur lors de la restauration du snapshot pour la machine virtuelle {vm_name}: {e}")
        raise
            