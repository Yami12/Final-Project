import datetime
from utils import driver

def time_in_range(time, range):
    difference = datetime.datetime.fromtimestamp(time // 1000) - driver.sending_time
    seconds_in_day = 24 * 60 * 60
    datetime.timedelta(0, 8, 562000)
    difference = divmod(difference.days * seconds_in_day + difference.seconds, 60)[0]
    if difference <= range and difference >= -range:
        print("True")
        return True
    return False



