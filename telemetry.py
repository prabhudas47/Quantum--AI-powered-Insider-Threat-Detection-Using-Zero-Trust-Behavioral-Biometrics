import requests

from config import BACKEND_URL


def send_telemetry(
    device_id,
    user_id,
    statistics,
    failed_logins=0
):
    url = f"{BACKEND_URL}/telemetry/"

    params = {
        "device_id": device_id,
        "user_id": user_id,

        # Behavioral data
        "typing_speed": statistics["typing_speed"],
        "mouse_speed": statistics["mouse_speed"],
        "mouse_movements": statistics["mouse_movements"],
        "idle_time": statistics["idle_time"],

        # Activity information
        "activity_state": statistics["activity_state"],
        "last_activity": statistics["last_activity"],

        # Authentication information
        "failed_logins": failed_logins
    }

    try:

        response = requests.post(
            url,
            params=params,
            timeout=5
        )

        if response.status_code == 200:

            print("Telemetry sent successfully.")

            return True

        print(
            "Telemetry failed:",
            response.status_code,
            response.text
        )

    except requests.RequestException as error:

        print(
            "Backend connection failed:",
            error
        )

    return False