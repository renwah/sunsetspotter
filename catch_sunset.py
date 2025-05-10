
# goals:
# find the approximate sunset time for the day
# turn on camera for 30min before - 30 min after the sunset
# monitor what is on the camera for colorfulness
# when it's appropriately nice out, take a picture
# send that picture somewhere (how to host?)
# OR, if the sunset is no good, take a photo before you turn off the camera? (do this if u get shitty weather)
# that app will notify someone else

import datetime
from astral.sun import sun, SunDirection, golden_hour
from astral.geocoder import database, lookup
import os
from crontab import CronTab
from vilib import Vilib
from PIL import Image
import numpy as np
city = lookup("Chicago", database())
s = sun(city.observer, date=datetime.date(2025, 5, 8))
golden = golden_hour(city.observer, direction = SunDirection.SETTING, date = datetime.date(2025, 5, 8))
print((
    f'Dawn:    {s["dawn"]}\n'
    f'Sunrise: {s["sunrise"]}\n'
    f'Noon:    {s["noon"]}\n'
    f'Sunset:  {s["sunset"]}\n'
    f'Dusk:    {s["dusk"]}\n'
    f'Golden Hour: {golden}\n'
    f'Golden Hour Start: {golden[0]}\n'
    f'Golden Hour End: {golden[1]}\n'
))
print(golden_hour(city.observer, direction = SunDirection.SETTING, date = datetime.date(2025, 5, 8)))
def schedule_monitor_sunset(start_time, end_time):
    cron = CronTab(user=True)
    job = cron.new(command=f'python3 /Users/renwah/sunsetspotter/monitor_sunset.py')
    job.setall(f'{start_time.minute} {start_time.hour} * * *')
    job.set_comment('Monitor Sunset Start')
    cron.write()

    job_end = cron.new(command=f'pkill -f monitor_sunset.py')
    job_end.setall(f'{end_time.minute} {end_time.hour} * * *')
    job_end.set_comment('Monitor Sunset End')
    cron.write()

# Calculate golden hour for the day after today
city = lookup("Chicago", database())
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
golden_tomorrow = golden_hour(city.observer, direction=SunDirection.SETTING, date=tomorrow)

# Schedule the monitor_sunset script
schedule_monitor_sunset(golden_tomorrow[0], golden_tomorrow[1])

def monitor_sunset():
    # Initialize the camera
    Vilib.camera_start()
    Vilib.display(local=True, web=False)

    try:
        while True:
            # Capture a frame from the camera
            frame = Vilib.capture_frame()
            if frame is None:
                continue

            # Convert the frame to an image
            image = Image.fromarray(frame)

            # Check for the presence of red in the image
            red_pixels = np.sum(np.array(image)[:, :, 0] > 150)  # Red channel threshold
            if red_pixels > 1000:  # Arbitrary threshold for "enough red"
                # Save the image
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                image.save(f"/Users/renwah/sunsetspotter/photos/sunset_{timestamp}.jpg")
                print(f"Photo taken at {timestamp}")
                break

    finally:
        # Stop the camera
        Vilib.camera_stop()

if __name__ == "__main__":
    monitor_sunset()