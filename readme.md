# IOT-SDK Project

## Overview
This project leverages IoT sensors to collect data, write it to the blockchain, and send the data to an Azure Service Bus queue. Data pulled from the Azure queue is stored in a local database, serving as a data faucet for further use. 

## Features
- Collects real-time data from IoT sensors.
- Writes data to the blockchain for immutability and traceability.
- Integrates with Azure Service Bus for push and pull operations.
- Stores pulled data in a local database for secure and reliable storage.

---

## Prerequisites
Before you start, ensure you have the following installed:
- Python 3.8 or higher
- Azure Service Bus credentials (Namespace and Queue Name)
- Growthaxl SDK

---

## Installation
1. Install the **Growthaxl SDK** by running the following command:

   ```bash
   pip install Growthaxl-sdk
   ```

---

## Steps to Run the Project

### 1. Start the Flask Server
Run the main application file to start the Flask server:

```bash
python app.py
```

### 2. Connect IoT Devices to the Server

Use the `/write_data` API to connect IoT devices to the server and send data.

- **API Endpoint:**
  ```
  POST /write_data
  ```

- **Sample Request Body:**
  ```json
  {
    "uuid": "12345",
    "IOT_DATA": "YOUR_DATA",
  }
  ```

### 3. Configure Azure Service Bus

If Azure Service Bus is implemented, you need to provide the following details:

- **Namespace**
- **Queue Name**

Once configured, data written to the blockchain will also be pushed to the Azure Service Bus queue for further processing.

### 4. Local Database
Pulled data from the Azure queue will be stored in the local database for future access and analysis. Ensure the database is properly configured in the project settings.

---

## Project Workflow

1. IoT sensors send data to the server via the `/write_data` API.
2. The server writes the data to the blockchain.
3. If configured, the data is pushed to the Azure Service Bus queue.
4. Data is pulled from the Azure queue and stored in the local database.

---

## Requirements
- Flask
- Growthaxl SDK
- Azure Service Bus SDK
- Blockchain connection library
- Local database (e.g., SQLite, PostgreSQL)

---

## Contributions
Feel free to raise issues, suggest improvements, or contribute to the project by submitting pull requests.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
