import requests,os
from dotenv import load_dotenv

load_dotenv()


def send_email(email,text):
	return requests.post(
		os.getenv('MAILGUN_URL'),
		auth=("api", os.getenv('MAILGUN_API_KEY')),
		data={"from": f"Mailgun Sandbox <{os.getenv('MAILGUN_FROM')}>",
			"to": f"<{email}>",
			"subject": "code status",
			"text": text})





