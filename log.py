# log.py
import datetime

def make_logger(logname):
    def log_to_file(session_id, action_type, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(logname, "a", encoding="utf-8") as f:
            f.write(f'{timestamp} | {session_id} | {action_type} | {message}\n')

    return log_to_file