# azure-vm-auto-scheduler
Azure VM Auto-Scheduler is a serverless automation solution using Azure Functions to optimize cloud costs by automatically shutting down and starting VMs based on tagging. It ensures non-critical VMs are deallocated when idle and restarted when needed, using a timer trigger and managed identity authentication. 


# Azure VM Auto-Scheduler

An Azure Functions–based solution that automates the **deallocation and startup** of **non-critical VMs** based on tagging, optimizing cloud costs and resource availability.

## Features

- **Automated VM Shutdown:** Deallocates VMs tagged `AutoShutdown=true` to reduce costs.  
- **Automated VM Startup:** Starts VMs tagged `AutoStart=true` when needed.  
- **Tag-Based Filtering & Exclusions:** Ensures only relevant VMs are managed while excluding critical ones.

## Prerequisites

- **Azure Subscription** – [Sign up](https://azure.microsoft.com/free/) if needed.  
- **Azure Functions Core Tools** – [Install guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local).  
- **Python 3.9+** – [Download](https://www.python.org/downloads/).  
- **Azure SDK Libraries** – Install via `pip install -r requirements.txt`.  
- **Managed Identity** – Used for secure authentication.

## Setup

1. **Clone the Repository:**  
   ```bash
   git clone <repository-url> && cd <repository-directory>
   ```

2. **Install Dependencies:**  
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Use .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**  
   Update `local.settings.json` for local testing:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AZURE_SUBSCRIPTION_ID": "<your-subscription-id>",
       "RESOURCE_GROUP": "<your-resource-group>",
       "SHUTDOWN_TAG": "AutoShutdown",
       "START_TAG": "AutoStart",
       "EXCLUDED_VMS": "critical-vm1,critical-vm2"
     }
   }
   ```

## Deployment

1. **Deploy to Azure:**  
   ```bash
   func azure functionapp publish <YourFunctionAppName>
   ```

2. **Monitor Logs:**  
   Use the **Azure Portal** or **Azure Functions Core Tools** to track execution.

## How It Works

| Function | Purpose | Trigger |
|----------|---------|---------|
| **Deallocate VMs** | Shuts down VMs with `AutoShutdown=true` | Timer (`deallocate_vms/function.json`) |
| **Start VMs** | Starts VMs with `AutoStart=true` | Timer (`start_vms/function.json`) |

### VM Tagging Rules

- VMs **must** have:
  - `AutoShutdown=true` to be deallocated.
  - `AutoStart=true` to be restarted.

## Troubleshooting

- **Check Environment Variables:** Ensure correct values in **Azure Function App settings**.  
- **Verify Managed Identity:** Assign proper VM management permissions.  
- **Inspect Logs:** Use `logging.exception` for deeper insights.

## Contributing

Fork, improve, and submit a pull request. For major changes, open an issue first.

