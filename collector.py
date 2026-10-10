import time
import threading
import math

from pynput import mouse, keyboard


class BehaviorCollector:

    def __init__(self):

        # ==============================
        # KEYBOARD
        # ==============================

        self.last_key_time = None
        self.key_intervals = []

        # ==============================
        # MOUSE
        # ==============================

        self.last_mouse_position = None
        self.last_mouse_time = None
        self.mouse_speeds = []
        self.mouse_movements = 0

        # ==============================
        # ACTIVITY
        # ==============================

        self.last_activity_time = time.time()

        # ==============================
        # THREAD SAFETY
        # ==============================

        self.lock = threading.Lock()

        # ==============================
        # LISTENERS
        # ==============================

        self.keyboard_listener = None
        self.mouse_listener = None

    # ==========================================
    # ACTIVITY UPDATE
    # ==========================================

    def update_activity(self):
        """
        Updates the last activity time.
        """

        self.last_activity_time = time.time()

    # ==========================================
    # KEYBOARD
    # ==========================================

    def on_key_press(self, key):

        current_time = time.time()

        with self.lock:

            # We DO NOT store actual keys.
            # Only timing information is collected.

            if self.last_key_time is not None:

                interval = (
                    current_time - self.last_key_time
                )

                if 0 < interval <= 5:

                    self.key_intervals.append(interval)

                    if len(self.key_intervals) > 100:
                        self.key_intervals.pop(0)

            self.last_key_time = current_time

            self.update_activity()

    # ==========================================
    # MOUSE
    # ==========================================

    def on_mouse_move(self, x, y):

        current_time = time.time()

        with self.lock:

            if self.last_mouse_position is not None:

                old_x, old_y = self.last_mouse_position

                distance = math.sqrt(
                    (x - old_x) ** 2 +
                    (y - old_y) ** 2
                )

                if self.last_mouse_time is not None:

                    time_difference = (
                        current_time -
                        self.last_mouse_time
                    )

                    if time_difference > 0:

                        speed = (
                            distance /
                            time_difference
                        )

                        if speed <= 10000:

                            self.mouse_speeds.append(
                                speed
                            )

                            if len(self.mouse_speeds) > 100:
                                self.mouse_speeds.pop(0)

                self.mouse_movements += 1

            self.last_mouse_position = (x, y)
            self.last_mouse_time = current_time

            self.update_activity()

    # ==========================================
    # ACTIVITY STATE
    # ==========================================

    def get_activity_state(self):

        current_time = time.time()

        idle_time = (
            current_time -
            self.last_activity_time
        )

        # Less than 30 seconds
        if idle_time < 30:

            return "Active"

        # 30 seconds to 5 minutes
        elif idle_time < 300:

            return "Idle"

        # More than 5 minutes
        else:

            return "Away"

    # ==========================================
    # CURRENT STATISTICS
    # ==========================================

    def get_statistics(self):

        with self.lock:

            # ==============================
            # TYPING SPEED
            # ==============================

            if self.key_intervals:

                average_interval = (
                    sum(self.key_intervals)
                    /
                    len(self.key_intervals)
                )

                if average_interval > 0:

                    typing_speed = (
                        1 /
                        average_interval
                    )

                else:

                    typing_speed = 0

            else:

                average_interval = 0
                typing_speed = 0

            # ==============================
            # MOUSE SPEED
            # ==============================

            if self.mouse_speeds:

                mouse_speed = (
                    sum(self.mouse_speeds)
                    /
                    len(self.mouse_speeds)
                )

            else:

                mouse_speed = 0

            # ==============================
            # IDLE TIME
            # ==============================

            idle_time = (
                time.time()
                -
                self.last_activity_time
            )

            # ==============================
            # ACTIVITY STATE
            # ==============================

            activity_state = self.get_activity_state()

            # ==============================
            # RETURN DATA
            # ==============================

            return {

                "typing_speed": round(
                    typing_speed,
                    2
                ),

                "average_key_interval": round(
                    average_interval,
                    3
                ),

                "mouse_speed": round(
                    mouse_speed,
                    2
                ),

                "mouse_movements":
                    self.mouse_movements,

                "idle_time": round(
                    idle_time,
                    2
                ),

                "activity_state":
                    activity_state,

                "last_activity":
                    self.last_activity_time
            }

    # ==========================================
    # START COLLECTION
    # ==========================================

    def start(self):

        self.keyboard_listener = (
            keyboard.Listener(
                on_press=self.on_key_press
            )
        )

        self.mouse_listener = (
            mouse.Listener(
                on_move=self.on_mouse_move
            )
        )

        self.keyboard_listener.start()
        self.mouse_listener.start()

        print(
            "Behavior collector started."
        )

    # ==========================================
    # STOP COLLECTION
    # ==========================================

    def stop(self):

        if self.keyboard_listener:

            self.keyboard_listener.stop()

        if self.mouse_listener:

            self.mouse_listener.stop()

        print(
            "Behavior collector stopped."
        )