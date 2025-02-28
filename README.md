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
   git clone https://github.com/Curious4Tech/azure-vm-auto-scheduler.git && cd azure-vm-auto-scheduler/my-vm-automation-function-app
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
       "SHUTDOWN_TAG_VALUE": "true",
       "START_TAG": "AutoStart",
       "START_TAG_VALUE": "true"
       "EXCLUDED_VMS": "critical-vm1,critical-vm2"
     }
   }
   ```

## Deployment

1. **Deploy to Azure:**  
   ```bash
   func azure functionapp publish <YourFunctionAppName>
   ```
You can also use VS code to deploy it easily.

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



### **Quick Steps to Test in Azure Portal** 🚀  

1️⃣ **Deploy the Function App**  
   - Navigate to **Azure Portal** → **Function Apps**  
   - Click **Create** and configure your **Function App** (Python runtime).  
   - Deploy the project using:  
     ```bash
     func azure functionapp publish <YourFunctionAppName>
     ```
![image](https://github.com/user-attachments/assets/6781257b-6720-4e04-984c-2af24390971c)

2️⃣ **Set Environment Variables**  
   - In **Azure Portal**, go to your **Function App** → **Configuration**.  
   - Add the required **Application Settings**:  
     - `AZURE_SUBSCRIPTION_ID`
     - `RESOURCE_GROUP`
     -  `SHUTDOWN_TAG_VALUE=true`
     - `SHUTDOWN_TAG=AutoShutdown`
     - `START_TAG=AutoStart`
     - `START_TAG_VALUE=true`
     - `EXCLUDED_VMS=critical-vm1,critical-vm2`  
   - Click **Apply**.

![image](https://github.com/user-attachments/assets/0f2e76d1-5375-498a-9c99-65a61a61ef0d)


3️⃣ **Assign Managed Identity Permissions**  
   - In **Function App** → **Identity**, enable **System Assigned Identity**.  
   - Grant **Virtual Machine Contributor** role to the Function App for your resource group.

![image](https://github.com/user-attachments/assets/7e0ee63f-62b2-40d4-bf0e-e7e7123bcb4e)


4️⃣ **Run the Function Manually**  
   - In **Azure Portal**, open **Function App** → **Functions**.  
   - Select **deallocate_vms** or **start_vms**.  
   - Click **Run** to execute the function.

![image](https://github.com/user-attachments/assets/f8d5173e-be9a-4926-96eb-55a95c046294)


5️⃣ **Check Logs & Results**  
   - Open **Monitor** → **Logs** to verify VM actions.

![image](https://github.com/user-attachments/assets/d3600cbb-8aa8-4e87-8a0d-10a7e4039b20)

   - You should see in your vms all the deallocated vms.

![image](https://github.com/user-attachments/assets/fc12e735-1bb6-466f-8529-1a32d15e284a)

   - Same process for testing the startup function

![image](https://github.com/user-attachments/assets/e511fedb-6581-44c9-8eef-70dbccad6827)

   - Now all your vms will be runing again

![image](https://github.com/user-attachments/assets/fa8f5fec-1f6d-4fd7-81d5-dbab3bd7dc03)


   - Ensure VMs tagged with `AutoShutdown=true` are stopped and `AutoStart=true` are started.
   

✅ **Done!** Your Azure Function is now managing VMs automatically! 🚀
## Troubleshooting

- **Check Environment Variables:** Ensure correct values in **Azure Function App settings**.  
- **Verify Managed Identity:** Assign proper VM management permissions.  
- **Inspect Logs:** Use `logging.exception` for deeper insights.

## Contributing

Fork, improve, and submit a pull request. For major changes, open an issue first.

