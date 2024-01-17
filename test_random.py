import datetime
import pytz

def convert_utc_to_est():
    utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    est = pytz.timezone('US/Eastern')
    est_time = utc_time.astimezone(est)
    return est_time





x = convert_utc_to_est().strftime('%I:%M %p %Z').lstrip('0')
print(x)



