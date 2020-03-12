from datetime import datetime
from .constants import DATE_FORMAT
# import datetime

####################### func of converting date atring into datetime object ############################

def convert_date(date):
    d = datetime.strptime(date, DATE_FORMAT).date()
    print(d, type(d))
    return d
