##################################    TWILIO PYTHON   ###########################################

#from twilio import *
from openerp import models, fields, api
#from twilio.rest import TwilioRestClient
from openerp.exceptions import Warning
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
#from twilio import TwilioRestException
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
auth_token = "your_auth_token"
client = Client(account_sid, auth_token)