from flask import Flask, request, jsonify
import json
import threading
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
log_file = 'app.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class JSONDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.lock = threading.Lock()

    def load_data(self):
        with self.lock:
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                return {"users": [], "assets": [], "requests": [], "logs": []}

    def save_data(self, data):
        with self.lock:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)


db = JSONDatabase('db.json')

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username]['password'] == password and users[username]['role'] == 'admin':
        return jsonify({"message": "Admin logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/employee/login', methods=['POST'])
def employee_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username]['password'] == password and users[username]['role'] == 'employee':
        return jsonify({"message": "Employee logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/request_asset', methods=['POST']))
def request_asset():
    data = request.json
    employee_id = data.get('employee_id')
    asset_id = data.get('asset_id')

    all_data = db.load_data()
    new_request = {
        "id": f"R{len(all_data['requests']) + 1:03d}",
        "employee_id": employee_id,
        "asset_id": asset_id,
        "status": "pending",
        "request_date": datetime.now().isoformat()
    }
    all_data['requests'].append(new_request)
    db.save_data(all_data)

    return jsonify({"status": "success", "message": "Asset request submitted"})


@app.route('/release_asset', methods=['POST'])
def release_asset():
    data = request.json
    employee_id = data.get('employee_id')
    asset_id = data.get('asset_id')

    all_data = db.load_data()
    assets = all_data['assets']

    for asset in assets:
        if asset['id'] == asset_id and asset['assigned_to'] == employee_id:
            asset['assigned_to'] = None
            asset['status'] = 'available'
            db.save_data(all_data)
            return jsonify({"status": "success", "message": "Asset released"})

    return jsonify({"status": "failure", "message": "Asset not found or not assigned to this employee"}), 404


@app.route('/view_tagged_assets', methods=['GET'])
def view_tagged_assets():
    employee_id = request.args.get('employee_id')

    all_data = db.load_data()
    assets = all_data['assets']

    tagged_assets = [asset for asset in assets if asset['assigned_to'] == employee_id]
    return jsonify(tagged_assets)


@app.route('/api/admin/add_asset', methods=['POST'])
def add_asset():
    data = request.get_json()
    asset_name = data.get('asset_name')
    asset_id = data.get('asset_id')

    if asset_name and asset_id:
        assets.append({"asset_name": asset_name, "asset_id": asset_id})
        return jsonify({"message": f"Asset {asset_name} added successfully"}), 200
    else:
        return jsonify({"message": "Invalid asset details"}), 400

@app.route('/api/admin/remove_asset', methods=['POST'])
def remove_asset():
    data = request.get_json()
    asset_name = data.get('asset_name')
    asset_id = data.get('asset_id')

    for asset in assets:
        if asset['asset_name'] == asset_name and asset['asset_id'] == asset_id:
            assets.remove(asset)
            return jsonify({"message": f"Asset {asset_name} removed successfully"}), 200

    return jsonify({"message": "Asset not found"}), 404

@app.route('/api/admin/add_employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    employee_name = data.get('employee_name')
    employee_id = data.get('employee_id')

    if employee_name and employee_id:
        employees.append({"employee_name": employee_name, "employee_id": employee_id})
        return jsonify({"message": f"Employee {employee_name} added successfully"}), 200
    else:
        return jsonify({"message": "Invalid employee details"}), 400

@app.route('/api/admin/remove_employee', methods=['POST'])
def remove_employee():
    data = request.get_json()
    employee_name = data.get('employee_name')
    employee_id = data.get('employee_id')

    for employee in employees:
        if employee['employee_name'] == employee_name and employee['employee_id'] == employee_id:
            employees.remove(employee)
            return jsonify({"message": f"Employee {employee_name} removed successfully"}), 200

    return jsonify({"message": "Employee not found"}), 404
################################################################
@app.route('/approve_request', methods=['POST'])
def approve_request():
    request_id = request.json.get('request_id')
    all_data = db.load_data()
    for req in all_data['requests']:
        if req['id'] == request_id:
            req['status'] = 'approved'
            for asset in all_data['assets']:
                if asset['id'] == req['asset_id']:
                    asset['assigned_to'] = req['employee_id']
                    asset['status'] = 'assigned'
            db.save_data(all_data)
            return jsonify({"status": "success", "message": "Request approved"})
    return jsonify({"status": "failure", "message": "Request not found"}), 404


@app.route('/get_logs', methods=['GET'])
def get_logs():
    log_type = request.args.get('type')  # 'frontend' or 'backend'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    all_data = db.load_data()
    logs = all_data['logs']

    filtered_logs = [log for log in logs if log['type'] == log_type]

    if start_date and end_date:
        filtered_logs = [log for log in filtered_logs if start_date <= log['timestamp'] <= end_date]

    return jsonify(filtered_logs)


class LogManager:
    def __init__(self, filename):
        self.filename = filename

    def add_log(self, message, user_id, log_type):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "user_id": user_id,
            "type": log_type
        }

        try:
            with open(self.filename, 'r+') as file:
                logs = json.load(file)
                logs.append(log_entry)
                file.seek(0)
                json.dump(logs, file, indent=2)
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                json.dump([log_entry], file, indent=2)

    def get_logs(self, start_date=None, end_date=None):
        with open(self.filename, 'r') as file:
            logs = json.load(file)

        if start_date and end_date:
            return [log for log in logs if start_date <= log['timestamp'] <= end_date]
        return logs

    def analyze_logs(self, analysis_type, start_date=None, end_date=None):
        logs = self.get_logs(start_date, end_date)

        if analysis_type == 'user_activity':
            user_activity = {}
            for log in logs:
                user_id = log['user_id']
                user_activity[user_id] = user_activity.get(user_id, 0) + 1
            return {"user_activity": user_activity}

        elif analysis_type == 'log_types':
            log_types = {}
            for log in logs:
                log_type = log['type']
                log_types[log_type] = log_types.get(log_type, 0) + 1
            return {"log_types": log_types}

        else:  # general analysis
            return {
                "total_logs": len(logs),
                "date_range": {
                    "start": logs[0]['timestamp'] if logs else None,
                    "end": logs[-1]['timestamp'] if logs else None
                }
            }

log_manager = LogManager('logs.json')

@app.route('/get_logs', methods=['GET'])
def get_logs():
    log_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    logs = log_manager.get_logs(start_date, end_date)

    if log_type:
        logs = [log for log in logs if log['type'] == log_type]

    return jsonify(logs)

@app.route('/analyze_logs', methods=['GET'])
def analyze_logs():
    analysis_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    analysis_result = log_manager.analyze_logs(analysis_type, start_date, end_date)

    return jsonify(analysis_result)
if __name__ == '__main__':
    app.run(debug=True)