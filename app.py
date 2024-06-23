import logging
from flask import Flask, request, jsonify, session
import json

app = Flask(__name__)
app.secret_key = 'secret_key'
log_file = 'app.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

#Load data from data.json
with open('data.json', 'r') as f:
    data = json.load(f)


@app.route("/api/assets", methods=["GET"])
def get_assets():
    return jsonify(data["assets"])

@app.route("/api/assets/<string:asset_id>", methods=["GET"])
def get_asset(asset_id):
    asset = next((asset for asset in data["assets"] if asset["asset_id"] == asset_id), None)
    if asset:
        return jsonify(asset)
    return jsonify({"error": "Asset not found"}), 404

@app.route("/api/employees", methods=["GET"])
def get_employees():
    return jsonify(data["employees"])

@app.route("/api/employees/<string:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = next((employee for employee in data["employees"] if employee["employee_id"] == employee_id), None)
    if employee:
        return jsonify(employee)
    return jsonify({"error": "Employee not found"}), 404

@app.route("/api/requests", methods=["POST"])
def make_request():
    new_request = request.get_json()
    if not new_request or "asset_id" not in new_request or "employee_id" not in new_request:
        return jsonify({"error": "Invalid request data"}), 400
    new_request["status"] = "pending"
    new_request["request_id"] = len(data["asset_requests"]) + 1
    data["asset_requests"].append(new_request)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({
        "id": new_request["request_id"],
        "asset_id": new_request["asset_id"],
        "employee_id": new_request["employee_id"],
        "status": new_request["status"]
    }), 201

@app.route("/api/assets/search", methods=["GET"])
def search_assets():
    search_query = request.args.get("q")
    assets = data["assets"]
    filtered_assets = [asset for asset in assets if search_query.lower() in asset["name"].lower() or search_query.lower() in asset.get("model", "").lower()]
    return jsonify(filtered_assets)

@app.route("/api/requests/log", methods=["GET"])
def get_request_log():
    try:
        with open(log_file, 'r') as log_file_obj:
            log_data = log_file_obj.readlines()
        return jsonify(log_data)
    except Exception as e:
        app.logger.error(f"Error reading log file: {e}")
        return jsonify({"error": "Failed to read log file"}), 500

@app.route("/api/logs", methods=["POST"])
def log_requests():
    try:
        request_data = request.json
        logging.info(f"Request: {request_data}")
        return jsonify({"message": "Request logged successfully"})
    except Exception as e:
        app.logger.error(f"Error logging request: {e}")
        return jsonify({"error": "Failed to log request"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = None
    if "users" in data:
        for role, details in data["users"].items():
            if details["password"] == password and role == username:
                user = {"username": username, "role": details["role"]}
                break
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid Username or Password"}), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logout successful"}), 200

if __name__ == "__main__":
    app.run(debug=True)
