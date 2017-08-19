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
account_sid = "ACcfdf69a019ff986e66d238348c8f2211"
auth_token = "6e93ea45699c5369a82abe937c0a789d"
client = Client(account_sid, auth_token)