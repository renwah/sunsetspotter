import os
import datetime
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from astral.sun import sun, SunDirection, golden_hour
from astral.geocoder import database, lookup

def email_sunset():
    message = Mail(
    from_email='rwah@uic.edu',
    to_emails='renwah41@gmail.com',
    subject='Look outside!',
    html_content='<strong>A good sunset is happening!</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

    send_to_rails_app()


def send_to_rails_app():
    # ex: 
    # photo_path = "/Users/renwah/sunsetspotter/photos/test_sunset.png"
    # timestamp = "2025-05-12T19:50:00Z"  # ISO 8601 format
    rails_url = os.environ.get('RAILS_APP_URL')
    todays_date = datetime.datetime.now().strftime("%Y%m%d")
    photo_path = f"./photos/{todays_date}.jpg"
    with open(photo_path, 'rb') as photo:
        files = {'image': photo}  # Match the `image` parameter in the Rails controller
        response = requests.post(rails_url, files=files, data={})
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

if __name__ == "__main__":
    email_sunset()