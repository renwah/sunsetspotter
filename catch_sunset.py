
# goals:
# find the approximate sunset time for the day
# turn on camera for 30min before - 30 min after the sunset
# monitor what is on the camera for colorfulness
# when it's appropriately nice out, take a picture
# send that picture somewhere (how to host?)
# OR, if the sunset is no good, take a photo before you turn off the camera? (do this if u get shitty weather)
# that app will notify someone else

import datetime
import requests
# from astral.sun import sun, SunDirection, golden_hour
# from astral.geocoder import database, lookup
import os
from crontab import CronTab

from PIL import Image
import numpy as np
#from vilib import Vilib
# city = lookup("Chicago", database())
# s = sun(city.observer, date=datetime.date(2025, 5, 8))
# golden = golden_hour(city.observer, direction = SunDirection.SETTING, date = datetime.date(2025, 5, 8))
# print((
#     f'Dawn:    {s["dawn"]}\n'
#     f'Sunrise: {s["sunrise"]}\n'
#     f'Noon:    {s["noon"]}\n'
#     f'Sunset:  {s["sunset"]}\n'
#     f'Dusk:    {s["dusk"]}\n'
#     f'Golden Hour: {golden}\n'
#     f'Golden Hour Start: {golden[0]}\n'
#     f'Golden Hour End: {golden[1]}\n'
# ))
# print(golden_hour(city.observer, direction = SunDirection.SETTING, date = datetime.date(2025, 5, 8)))
# def schedule_monitor_sunset(start_time, end_time):
#     cron = CronTab(user=True)
#     job = cron.new(command=f'python3 /Users/renwah/sunsetspotter/monitor_sunset.py')
#     job.setall(f'{start_time.minute} {start_time.hour} * * *')
#     job.set_comment('Monitor Sunset Start')
#     cron.write()

#     job_end = cron.new(command=f'pkill -f monitor_sunset.py')
#     job_end.setall(f'{end_time.minute} {end_time.hour} * * *')
#     job_end.set_comment('Monitor Sunset End')
#     cron.write()

# Calculate golden hour for the day after today
# city = lookup("Chicago", database())
# tomorrow = datetime.date.today() + datetime.timedelta(days=1)
# golden_tomorrow = golden_hour(city.observer, direction=SunDirection.SETTING, date=tomorrow)

# Schedule the monitor_sunset script
#schedule_monitor_sunset(golden_tomorrow[0], golden_tomorrow[1])
# schedule_monitor_sunset(datetime.time(19, 50), datetime.time(20, 50))  # Example times

def monitor_sunset():
    photo_path = "/Users/renwah/sunsetspotter/photos/test_sunset.png"
    timestamp = "2025-05-12T19:50:00Z"  # ISO 8601 format
    rails_url = "http://localhost:3001/sunsets"

    send_to_rails_app(photo_path, timestamp, rails_url)
    # Initialize the camera
    Vilib.camera_start()
    Vilib.display(local=True, web=True)
    Vilib.color_detect(color="red")  # red, green, blue, yellow , orange, purple


    try:
        while True:
            n = Vilib.color_obj_parameter['n']
            color = Vilib.color_obj_parameter['color']
            if n != 0:
                x = Vilib.color_obj_parameter['x']
                y = Vilib.color_obj_parameter['y']
                w = Vilib.color_obj_parameter['w']
                h = Vilib.color_obj_parameter['h']
                print(f"{n} {color} blocks found, the largest block coordinate=({x}, {y}), size={w}*{h}")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                image.save(f"/Users/renwah/sunsetspotter/photos/sunset_{timestamp}.jpg")
                print(f"Photo taken at {timestamp}")
                break
            else:
                print(f'No {color} block found')

    finally:
        # Stop the camera
        #schedule for the following day
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        schedule_monitor_sunset(tomorrow.time(20, 50), tomorrow.time(21, 50))
        Vilib.camera_close()


def send_to_rails_app(photo_path, timestamp, rails_url):
    with open(photo_path, 'rb') as photo:
        files = {'image': photo}  # Match the `image` parameter in the Rails controller
        response = requests.post(rails_url, files=files, data={})
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")


if __name__ == "__main__":
    monitor_sunset()