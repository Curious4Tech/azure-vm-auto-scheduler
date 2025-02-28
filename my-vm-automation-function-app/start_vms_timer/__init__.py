import os
import datetime
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import AzureError

def main(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.warning("The start_vms timer function is running late!")
    
    logging.info(f"Azure Function 'start_vms_timer' executed at {datetime.datetime.utcnow()}")
    
    # Get environment variables
    SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")
    RESOURCE_GROUP = os.environ.get("RESOURCE_GROUP")
    START_TAG = os.environ.get("START_TAG", "AutoStart")
    START_TAG_VALUE = os.environ.get("START_TAG_VALUE", "true")
    
    # Validate environment variables
    if not SUBSCRIPTION_ID or not RESOURCE_GROUP:
        logging.error("Missing environment variables: AZURE_SUBSCRIPTION_ID or RESOURCE_GROUP")
        return
    
    try:
        # Authenticate and create client
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
        
        logging.info(f"Fetching virtual machines in resource group {RESOURCE_GROUP}...")
        vms = list(compute_client.virtual_machines.list(RESOURCE_GROUP))
        logging.info(f"Found {len(vms)} VMs in resource group {RESOURCE_GROUP}")
        
        started_count = 0
        skipped_count = 0
        
        for vm in vms:
            vm_name = vm.name
            
            # Check if VM has the required tag for auto-starting
            if START_TAG and START_TAG_VALUE:
                if not vm.tags or START_TAG not in vm.tags or vm.tags[START_TAG].lower() != START_TAG_VALUE.lower():
                    logging.info(f"VM {vm_name} doesn't have the required tag {START_TAG}={START_TAG_VALUE}. Skipping.")
                    skipped_count += 1
                    continue
            
            try:
                # Check current power state
                instance_view = compute_client.virtual_machines.instance_view(RESOURCE_GROUP, vm_name)
                power_state = next(
                    (status.code for status in instance_view.statuses if status.code.startswith("PowerState/")),
                    None
                )
                
                if power_state and "running" in power_state.lower():
                    logging.info(f"VM {vm_name} is already running (current state: {power_state}). Skipping.")
                    skipped_count += 1
                else:
                    # Start the VM and wait for operation to complete
                    logging.info(f"Starting VM: {vm_name} (current state: {power_state})")
                    start_operation = compute_client.virtual_machines.begin_start(RESOURCE_GROUP, vm_name)
                    start_operation.result()  # Wait for operation to complete
                    logging.info(f"Successfully started VM: {vm_name}")
                    started_count += 1
                    
            except AzureError as e:
                logging.error(f"Error processing VM {vm_name}: {str(e)}")
                continue
        
        logging.info(f"Start VMs operation summary: Started {started_count} VMs, Skipped {skipped_count} VMs")
        
    except Exception as e:
        logging.error(f"Unexpected error in start_vms: {str(e)}")
        raise