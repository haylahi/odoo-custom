##################################    TWILIO PYTHON   ###########################################

#from twilio import *
from odoo import models, fields, api
#from twilio.rest import TwilioRestClient
from odoo.exceptions import Warning
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
#from twilio import TwilioRestException

from twilio.rest import Client

# Get these credentials from http://twilio.com/user/account
account_sid = "ACXXXXXXXXXXXXXXXXX"
auth_token = "YYYYYYYYYYYYYYYYYY"
client = Client(account_sid, auth_token)