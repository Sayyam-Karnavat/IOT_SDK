import json
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
import algokit_utils
from Temperature_anomaly_model import predict_temperature_anomaly
import random
# from filter_response import filter_response
from growthaxl_SDK import BlockchainClient

import database as db
from artifact_new import HelloWorldClient
import hashlib
from Send_data_to_bus import send_data_to_bus
from Receive_data_from_bus import receive_data_from_bus


# What if User wants to check has value of few records out of entire combined data hash ?

def service_bus_message_to_json(service_bus_message):
    try:
        # Decode the JSON payload
        message_json = json.loads(next(service_bus_message.body).decode('utf-8'))
        return message_json
    except (json.JSONDecodeError, StopIteration) as e:
        print(f"Error decoding JSON: {e}")
        return {}


def deploy_data(json_data, filter_application_ID):

    client = BlockchainClient(network="testnet")
    
    NAMESPACE_CONNECTION_STR = "YOUR_AZURE_NAMSPACE_STRING"
    QUEUE_NAME = "YOUR_QUEUE_NAME"
    
    # Send the transaction data to azure bus
    send_data_to_bus(json_data=json_data,namespace_string=NAMESPACE_CONNECTION_STR , queue_name=QUEUE_NAME)

    # Receive the data from bus 
    received_data_from_queue = receive_data_from_bus(namespace_connection_string= NAMESPACE_CONNECTION_STR , queue_name= QUEUE_NAME)
    decoded_json_bus_data = service_bus_message_to_json(received_data_from_queue)

    # Create the client
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = "a" * 64
    indexer_add = "https://testnet-idx.algonode.cloud"
    


    algod_client = AlgodClient(algod_token, algod_address)
    indexer_client = IndexerClient("", indexer_add)

    # Get the details from json data received from the front end and flask
    temperature = int(decoded_json_bus_data["temperature"]) # First converting it to integer since AI model will need it for prediction
    moisture = decoded_json_bus_data['moisture']
    humidity = decoded_json_bus_data['humidity']
    uuid = decoded_json_bus_data['uuid']
    # wallet_address = json_data["walletAddress"]
    # mnemonic = decoded_json_bus_data["mnemonic"]

    json_data_string = json.dumps(decoded_json_bus_data)

    ### The MD5 encoded hash it irreversible we CANNOT DECODE IT BACK !!!! WE can just compare it

    # Third party API for generating and comparing Hash(MD5 checksum)
    json_hash_data = hashlib.md5(json_data_string.encode()).hexdigest()

    

    # Run the AI model for anomaly detection 
    prediction_result = predict_temperature_anomaly(temperature=temperature) # Return 1 for anomaly and 0 for normal temperature
    prediction = "Anomaly" if prediction_result == 1 else "Normal"

    
    # Create a deployer
    deployer = algokit_utils.get_account_from_mnemonic(mnemonic="toss transfer sure frozen real jungle mouse inch smoke derive floor alter ten eagle narrow perfect soap weapon payment chaos amateur height estate absent cabbage")

    # Create app client to use the app we have deployed
    app_client = HelloWorldClient(algod_client, creator=deployer, indexer_client=indexer_client)
    app_client.app_id = filter_application_ID
    # Get the details from response from blockchain of the data that we have written on blockchain
    response_from_blockchain = app_client.raspberry_data(hash=f"{json_hash_data}", UUID=f"{uuid}" , temperature=f"{temperature}" , moisture=f"{moisture}" , humidity=f"{humidity}")
    print(f"Data written to blockchain App ID :-{response_from_blockchain.tx_info["txn"]["txn"]["apid"]}")
    print(f"https://lora.algokit.io/testnet/transaction/{response_from_blockchain.tx_id}")


    # This function will fiter out paramters
    # Contains blockchain data like gas fees , block timestamp,app id etc. 
    blockchain_filtered_data = client.filter_response_only(response=response_from_blockchain)

    latest_transaction_data = client.fetch_latest_transaction_string(app_id=app_client.app_id)

    server_data = {}
    # Device status
    devices_list = ["Device_A", "Device_B" ,"Device_C"]
    status = ["active", "stopped"]
    # Region
    regions = ["Mumbai" , "Pune" , "Bangalore" , "Delhi" , "Goa"]

    server_data["model_prediction"] = f"{prediction}"
    server_data["device_status"] = status[random.randint(0,1)]
    server_data["device_id"] = devices_list[random.randint(0, len(devices_list)-1)]
    server_data["region"]=regions[random.randint(0,len(regions)-1)]


    # Update the blockchain filtered data with latest transaction and also with server data
    blockchain_filtered_data.update(server_data)
    blockchain_filtered_data.update(latest_transaction_data)

    
    # Printing the prediction of AI model after data is written to blockchain and pulled from azure bus service
    print("AI model prediction for temperature :-" , prediction)

    ## Check if table exists or not and insert the data into local database
    db.create_table(json_data=blockchain_filtered_data) # This query creates table only if table does not exists
    db.insert(blockchain_filtered_data)