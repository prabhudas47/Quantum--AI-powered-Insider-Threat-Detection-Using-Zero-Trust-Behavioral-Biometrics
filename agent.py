import time

from config import (
    DEVICE_ID,
    USER_ID,
    TELEMETRY_INTERVAL
)

from collector import BehaviorCollector
from telemetry import send_telemetry


def main():

    print("=" * 50)
    print("ThreatGuard Client Agent")
    print("=" * 50)

    print(f"Device ID : {DEVICE_ID}")
    print(f"User ID   : {USER_ID}")
    print(
        f"Telemetry interval : "
        f"{TELEMETRY_INTERVAL} seconds"
    )

    collector = BehaviorCollector()

    collector.start()

    print("Client Agent is running...")
    print("Press CTRL+C to stop.")
    print()

    try:

        while True:

            # Wait for the configured interval
            time.sleep(TELEMETRY_INTERVAL)

            # Get current behavioral statistics
            statistics = collector.get_statistics()

            print("-" * 50)

            print("Current Behavior")
            print(
                f"Typing Speed   : "
                f"{statistics['typing_speed']} keys/sec"
            )

            print(
                f"Mouse Speed    : "
                f"{statistics['mouse_speed']} px/sec"
            )

            print(
                f"Mouse Movements: "
                f"{statistics['mouse_movements']}"
            )

            print(
                f"Idle Time      : "
                f"{statistics['idle_time']} sec"
            )

            # Send to backend
            send_telemetry(
                device_id=DEVICE_ID,
                user_id=USER_ID,
                statistics=statistics
            )

    except KeyboardInterrupt:

        print()
        print("Stopping Client Agent...")

        collector.stop()

        print("Client Agent stopped.")


if __name__ == "__main__":
    main()