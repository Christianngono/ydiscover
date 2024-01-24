# vm_manager.py

import libvirt


class VMManager:
    def __init__(self):
        self.conn = libvirt.open('qemu:///system')
        
        if self.conn is None:
            raise Exception("Login failed")
    
    def create_vm(self, vm_name, memory=1024, vcpu=1,):
        # Code to create the virtual machine with libvirt(QEMU/KVM)
        xml_disc = f"""
        <domain type='kvm'>
                <name>{vm_name}</name>
                <memory unit='KiB'>{memory * 1024}</memory>
                <vcpu placement='static'>{vcpu}</vcpu>
                <!-- Add other configurations according to our needs -->
            </domain>
        """
        
        try:
            dom = self.conn.createXML(xml_disc, 0)
            print(f"Virtual machine {vm_name} was created successfully.")
            return dom
        except libvirt.libvirtError as e:
            print(f"Error creating virtual machine {vm_name}: {e}")
            raise
    def deploy_vms(self):
        # Code to start virtual machines
        domains = self.conn.listDomainsID()
        for dom_id in domains:
            dom = self.conn.lookupByID(dom_id)
            dom.create()
            
    def list_vms(self):
        # Code to display a list of virtual machines
        domains = self.conn.listAllDomains()
        for dom in domains:
            print(f"Virtual machine: {dom.name()}")    
            print(f"Status: {dom.state()[0]}")
            
    def start_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.create()
            print(f"Virtual machine {vm_name} was started successfully.")
        except libvirt.libvirtError as e:
            print(f"Unable to find or start virtual machine {vm_name}.\nDetails: \n{e}")
            raise
    def stop_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.destroy()
            print(f"Virtual machine {vm_name} has been successfully shut down.")
        except libvirt.libvirtError as e:
            print(f"Failed to shut down virtual machine {vm_name}.\nDetails: \n{ e}")
            raise
    def undefine_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            dom.undefine()
            print(f"Virtual machine {vm_name} was successfully defined.")
        except libvirt.libvirtError as e:
            print(f"Error deleting virtual machine {vm_name}: {e}")
            raise 
   # close the connection with the hypervisor
    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("The connection with the hypervisor has been closed.")
    # Get the current state of the virtual machine       
    def get_vm_state(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            state, reason = dom.state()
            print(f"Virtual machine {vm_name} - State: {libvirt.VIR_DOMAIN_STATE[state]} ({reason})")
            return state
        except libvirt.libvirtError as e:
            print(f"Failed to get the status of virtual machine {vm_name}.\nDetails: \n{e}")
            raise
    # Add additional disks to an existing virtual machine
    def add_disk(self, vm_name):
        try:
            # Recover the virtual machine
            dom = self.conn.lookupByName(vm_name)
            # Create the new disk item
            xml_desc = ""    
            dom.attachDevice(xml_desc)
            print(f"Disk successfully added to virtual machine {vm_name}.")
        except libvirt.libvirtError as e:
            print(f"An error occurred while adding the disk to virtual machine {vm_name}: {e}")
            raise
    # Create virtual machine snapshots
    def create_snapshot(self, vm_name, snapshots_name):
        try:
            # Recover the virtual machine
            dom = self.conn.lookupByName(vm_name)
            for snapshot in snapshots_name:
                # Creating a snapshot
                dom.snapshotCreateXML(f"""<domainsnapshot><name>{snapshot}</name></domainsnapshot>""", 0)
            print(f"Snapshot '{snapshots_name}' created for virtual machine {vm_name}.")
            return snapshot
        except libvirt.libvirtError as e:
            print(f"Failed to create snapshot(s) for virtual machine {vm_name}\nDetails: \n{e}")
            raise
    # lister les snapshots
    def list_snapshots(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            snapshots = dom.listSnapshots()
            print(f"List of snapshots for virtual machine {vm_name}: {snapshots}")
            return snapshots
        except libvirt.libvirtError as e:
            print(f"Error retrieving snapshots for virtual machine {vm_name}: {e}")
            raise
    # restore virtual machine snapshots
    def restore_from_snapshot(self, vm_name, snapshot_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            snapshot = dom.snapshotLookupByName(snapshot_name, 0)
            snapshot.revertToSnapshot(0)
            print(f"Snapshot {snapshot_name} successfully restored for virtual machine {vm_name}.")
        except libvirt.libvirtError as e:
            print(f"Error restoring snapshot for virtual machine {vm_name}: {e}")
            raise
            