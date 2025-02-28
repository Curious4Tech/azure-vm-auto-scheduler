import os
import datetime
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import AzureError

# Create the function app
app = func.FunctionApp()

# Define variables
SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP = os.environ.get("RESOURCE_GROUP")
# Add tag-based filtering for selective deallocation
SHUTDOWN_TAG = os.environ.get("SHUTDOWN_TAG", "AutoShutdown")
SHUTDOWN_TAG_VALUE = os.environ.get("SHUTDOWN_TAG_VALUE", "true")
# Add exclusion list for critical VMs
EXCLUDED_VMS = os.environ.get("EXCLUDED_VMS", "").split(",")

def main(myTimer: func.TimerRequest) -> None:
    # Check if the timer is past due
    if myTimer.past_due:
        logging.warning("The timer function is running late!")
    
    start_time = datetime.datetime.utcnow()
    logging.info(f"Azure Function 'deallocate_vms_timer' executed at {start_time}")
    
    try:
        # Validate environment variables
        if not SUBSCRIPTION_ID or not RESOURCE_GROUP:
            logging.error("Missing required environment variables: AZURE_SUBSCRIPTION_ID or RESOURCE_GROUP")
            return
            
        # Authenticate using Managed Identity or Service Principal
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
        
        logging.info(f"Fetching virtual machines in resource group {RESOURCE_GROUP}...")
        # Get all VMs
        vms = list(compute_client.virtual_machines.list(RESOURCE_GROUP))
        logging.info(f"Found {len(vms)} VMs in resource group {RESOURCE_GROUP}")
        
        deallocated_count = 0
        skipped_count = 0
        error_count = 0
        
        for vm in vms:
            vm_name = vm.name
            
            # Skip excluded VMs
            if vm_name in EXCLUDED_VMS:
                logging.info(f"VM {vm_name} is in the exclusion list. Skipping.")
                skipped_count += 1
                continue
                
            # Check if VM has the required tag for auto-shutdown
            if SHUTDOWN_TAG and SHUTDOWN_TAG_VALUE:
                if not vm.tags or SHUTDOWN_TAG not in vm.tags or vm.tags[SHUTDOWN_TAG].lower() != SHUTDOWN_TAG_VALUE.lower():
                    logging.info(f"VM {vm_name} doesn't have the required tag {SHUTDOWN_TAG}={SHUTDOWN_TAG_VALUE}. Skipping.")
                    skipped_count += 1
                    continue
            
            try:
                # Check current power state
                instance_view = compute_client.virtual_machines.instance_view(RESOURCE_GROUP, vm_name)
                power_state = next((status.code for status in instance_view.statuses if status.code.startswith('PowerState/')), None)
                
                if power_state and "running" in power_state.lower():
                    logging.info(f"Deallocating VM: {vm_name} (current state: {power_state})")
                    # Use begin_deallocate instead of begin_power_off
                    deallocate_operation = compute_client.virtual_machines.begin_deallocate(RESOURCE_GROUP, vm_name)
                    logging.info(f"Deallocation command sent to VM: {vm_name}")
                    deallocate_operation.result()  # Wait for the operation to complete
                    logging.info(f"Successfully deallocated VM: {vm_name}")
                    deallocated_count += 1
                else:
                    logging.info(f"VM {vm_name} is not running (current state: {power_state}). Skipping.")
                    skipped_count += 1
            except AzureError as e:
                logging.error(f"Error processing VM {vm_name}: {str(e)}")
                error_count += 1
                continue
                
        # Log summary statistics
        end_time = datetime.datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        logging.info(f"Deallocation operation summary: Deallocated {deallocated_count} VMs, " +
                     f"Skipped {skipped_count} VMs, Errors {error_count} VMs")
        logging.info(f"Function completed in {duration:.2f} seconds")
                
    except Exception as e:
        logging.error(f"Error in deallocate_vms function: {str(e)}")
        raise