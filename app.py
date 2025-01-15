from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from deploy_file import deploy_data
import random

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/getTemperatureFromFrontEnd", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def getTemperature():
    try:
        # all_app_ids = [708128476, 709404721][random.randint(0,1)]

        # Added two more parameters humidity and moisture
        selected_app_id = 722841168
        received_temperature_data = request.get_json()
        uuid = random.randint(1000 , 5000)
        received_temperature_data['uuid'] = uuid
        received_temperature_data['moisture'] = random.randint(0,100)
        received_temperature_data['humidity'] = random.randint(0,100)
        print("Raspberry data received on server !!!")
        
        deploy_data(json_data=received_temperature_data ,filter_application_ID=selected_app_id)
        return jsonify({"Success" : "Data Sent !!!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False)
