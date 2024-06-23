import json
from datetime import datetime


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


import json
from datetime import datetime
from collections import Counter


class LogManager:
    def __init__(self, filename):
        self.filename = filename

    def add_log(self, level, component, message, user_id):
        log_entry = {
            "id": f"L{self._get_next_log_id():03d}",
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "component": component,
            "message": message,
            "user_id": user_id
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

    def _get_next_log_id(self):
        try:
            with open(self.filename, 'r') as file:
                logs = json.load(file)
                return int(logs[-1]['id'][1:]) + 1 if logs else 1
        except FileNotFoundError:
            return 1

    def get_logs(self, start_date=None, end_date=None):
        with open(self.filename, 'r') as file:
            logs = json.load(file)

        if start_date and end_date:
            return [log for log in logs if start_date <= log['timestamp'] <= end_date]
        return logs

    def analyze_logs(self, start_date=None, end_date=None):
        logs = self.get_logs(start_date, end_date)

        return {
            "total_logs": len(logs),
            "log_levels": self._count_log_levels(logs),
            "component_usage": self._count_component_usage(logs),
            "user_activity": self._count_user_activity(logs),
            "error_summary": self._summarize_errors(logs)
        }

    def _count_log_levels(self, logs):
        return dict(Counter(log['level'] for log in logs))

    def _count_component_usage(self, logs):
        return dict(Counter(log['component'] for log in logs))

    def _count_user_activity(self, logs):
        return dict(Counter(log['user_id'] for log in logs))

    def _summarize_errors(self, logs):
        error_logs = [log for log in logs if log['level'] == 'ERROR']
        return {
            "total_errors": len(error_logs),
            "error_components": dict(Counter(log['component'] for log in error_logs))
        }