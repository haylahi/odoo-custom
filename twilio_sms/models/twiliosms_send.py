##################################    TWILIO PYTHON   ###########################################

from twilio import *
from odoo import models, fields, api
from twilio.rest import TwilioRestClient
from odoo.exceptions import Warning
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from twilio import TwilioRestException