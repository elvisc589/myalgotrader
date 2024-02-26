import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RedditCredentials:
    def __init__(self):
        self.user = os.getenv("REDDIT_USER")
        self.password = os.getenv("REDDIT_PASS")
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        
    @property
    def empty_credentials(self):
        """Returns True if any credential is empty; False otherwise"""

        return not (bool(self.user) and bool(self.password) and bool(self.client_id) and bool(self.client_secret))


class RobinhoodCredentials:
    def __init__(self):
        self.user = os.getenv("ROBINHOOD_USER")
        self.password = os.getenv("ROBINHOOD_PASS")
        self.mfa_code = os.getenv("ROBINHOOD_MFA_CODE")

    @property
    def empty_credentials(self):
        """Returns True if any credential is empty; False otherwise"""

        return not (bool(self.user) and bool(self.password) and bool(self.mfa_code))
    
class TwilioCredentials:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.your_phone_number = os.getenv("YOUR_PHONE_NUMBER")  # Add the variable for the 'to' phone number
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")  # Add the variable for the 'from' phone number


    @property
    def empty_credentials(self):
        """Returns True if any credential is empty; False otherwise"""

        return not (bool(self.account_sid) and bool(self.auth_token))
    

