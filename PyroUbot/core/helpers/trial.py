import json
import os
import time

TRIAL_FILE = "trial_users.json"
TRIAL_DURATION = 86400  # 1 hari dalam detik

def load_trials():
    if not os.path.exists(TRIAL_FILE):
        return {}
    with open(TRIAL_FILE, "r") as f:
        return json.load(f)

def save_trials(data):
    with open(TRIAL_FILE, "w") as f:
        json.dump(data, f, indent=2)

def start_trial(user_id: int) -> bool:
    user_id = str(user_id)
    trials = load_trials()

    # Jika sudah pernah trial
    if user_id in trials:
        start_time = trials[user_id]
        if time.time() - start_time < TRIAL_DURATION:
            return False  # masih aktif
        else:
            return False  # expired, tapi tetap tidak boleh ulangi

    # Simpan waktu mulai trial
    trials[user_id] = time.time()
    save_trials(trials)
    return True

def is_trial_active(user_id: int) -> bool:
    user_id = str(user_id)
    trials = load_trials()

    if user_id not in trials:
        return False

    start_time = trials[user_id]
    return (time.time() - start_time) < TRIAL_DURATION
