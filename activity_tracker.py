import time
import win32gui
from plyer import notification

from detection.activity_classifier import classify_activity
from detection.database.activity_database import save_activity


# ============================================================
# SETTINGS
# ============================================================

# Seconds of continuous distraction before notification
DISTRACTION_LIMIT = 30

# Seconds before another notification can appear
NOTIFICATION_COOLDOWN = 60


# ============================================================
# GET ACTIVE WINDOW
# ============================================================

def get_active_window():
    """
    Returns the title of the currently active Windows window.
    """

    try:
        window = win32gui.GetForegroundWindow()

        if window == 0:
            return "Unknown"

        title = win32gui.GetWindowText(window)

        if not title:
            return "Unknown"

        return title

    except Exception:
        return "Unknown"


# ============================================================
# SHOW DISTRACTION NOTIFICATION
# ============================================================

def show_distraction_notification(window_title, duration):
    """
    Shows a Windows desktop notification when
    a distraction continues for too long.
    """

    try:
        notification.notify(
            title="⚠️ Procrastination Alert",
            message=(
                f"You have been using {window_title} "
                f"for {duration} seconds.\n"
                "Consider returning to your productive task!"
            ),
            app_name="Digital Procrastination Detector",
            timeout=5
        )

    except Exception as error:
        print(f"Notification error: {error}")


# ============================================================
# START PROGRAM
# ============================================================

print("========================================")
print("   DIGITAL PROCRASTINATION DETECTOR")
print("========================================")
print("       REAL-TIME ACTIVITY TRACKER")
print("========================================")
print()
print("Tracking your computer activity...")
print("Distraction alert after 30 seconds.")
print("Press CTRL + C to stop.")
print()


# ============================================================
# VARIABLES
# ============================================================

last_window = ""
last_category = ""

start_time = time.time()

last_notification_time = 0


# ============================================================
# MAIN TRACKING LOOP
# ============================================================

try:

    while True:

        # Get currently active window
        current_window = get_active_window()

        # Get current time
        current_time = time.time()


        # ====================================================
        # WINDOW CHANGED
        # ====================================================

        if current_window != last_window:

            # -----------------------------------------------
            # Save previous activity
            # -----------------------------------------------

            if last_window != "":

                duration = int(current_time - start_time)

                save_activity(
                    last_window,
                    last_category,
                    duration
                )

                print(
                    f"Saved: "
                    f"{last_category:<12} | "
                    f"{last_window} | "
                    f"{duration} seconds"
                )


            # -----------------------------------------------
            # Classify new window
            # -----------------------------------------------

            current_category = classify_activity(
                current_window
            )

            print(
                f"Now tracking: "
                f"{current_category:<12} | "
                f"{current_window}"
            )


            # -----------------------------------------------
            # Start timing new activity
            # -----------------------------------------------

            last_window = current_window

            last_category = current_category

            start_time = current_time

            # Reset notification timer
            last_notification_time = 0


        # ====================================================
        # SAME WINDOW
        # ====================================================

        else:

            # Calculate how long current window has been active
            current_duration = int(
                current_time - start_time
            )


            # =================================================
            # CHECK FOR DISTRACTION
            # =================================================

            if (
                last_category == "DISTRACTION"
                and current_duration >= DISTRACTION_LIMIT
            ):

                # Calculate time since last notification
                time_since_notification = (
                    current_time - last_notification_time
                )


                # ---------------------------------------------
                # Show notification
                # ---------------------------------------------

                if (
                    last_notification_time == 0
                    or time_since_notification >= NOTIFICATION_COOLDOWN
                ):

                    show_distraction_notification(
                        last_window,
                        current_duration
                    )

                    last_notification_time = current_time

                    print()
                    print("⚠️ PROCRASTINATION ALERT!")
                    print(
                        f"Distraction: {last_window}"
                    )
                    print(
                        f"Duration: {current_duration} seconds"
                    )
                    print()


        # Wait one second before checking again
        time.sleep(1)


# ============================================================
# STOP PROGRAM WITH CTRL + C
# ============================================================

except KeyboardInterrupt:

    print()
    print("Stopping activity tracker...")


    # Save the final activity
    if last_window != "":

        duration = int(
            time.time() - start_time
        )

        save_activity(
            last_window,
            last_category,
            duration
        )

        print(
            f"Saved final activity: "
            f"{last_window} | "
            f"{duration} seconds"
        )


    print()
    print("Activity tracking stopped.")