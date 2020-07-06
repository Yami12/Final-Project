"""
this file contains utils functions
"""

import datetime
import sys
import subprocess
import re

from utils import string_list as sl
from utils import driver

'''
    function: time_in_range
    description: A function that checks if the given time is in the requested range of the sending_time
'''
def time_in_range(time, range):
    difference = datetime.datetime.fromtimestamp(time // 1000) - driver.sending_time
    seconds_in_day = 24 * 60 * 60
    datetime.timedelta(0, 8, 562000)
    difference = divmod(difference.days * seconds_in_day + difference.seconds, 60)[0]
    if difference <= range and difference >= -range: # the time is in the range
        return True
    return False


'''
        function: get_coordinates_by_resource_id
        description: A function that returns a device component coordinates by its resource id
'''
def get_coordinates_by_resource_id(step, parent_name):
    print_log("\cf1 searching for coordinates \line")
    process = subprocess.Popen(['adb','-s', driver.child_device ,'exec-out', 'uiautomator', 'dump', '/dev/tty'],stdout=subprocess.PIPE)  # dump the uiautomator file
    content = str(process.stdout.read())
    splitted_content = re.split("<node", content)

    for node in splitted_content:
        if step[sl.TYPE_STEP] == sl.TYPE_ID and step[sl.ID_STEP] in node: # id
            process.kill()
            break
        elif step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR and 'class="android.widget.ImageView"' not in node: # uiautomator
            if step[sl.CONTENT_STEP] == sl.CHAT_NAME:
                if parent_name in node:
                    process.kill()
                    break
            elif 'content-desc="' + step[sl.CONTENT_STEP] in node:
                process.kill()
                break
        elif step[sl.TYPE_STEP] == sl.TYPE_CLASS and 'class="' + step[sl.ID_STEP] in node: # class
            process.kill()
            break

    bounds = re.search('bounds="\[([0-9]+),([0-9]+)\]', node)
    if not bounds:
        print_log("\cf2 bounds not fond. \line")
    else:
        print_log("\cf1 \\b bounds fond:\\b0 " + str(bounds)[0] + str(bounds)[1] + "\line")
    return bounds


'''
    function: print_log
    description: A function that prints the string in utf format
'''
def print_log(log):
    print(log)
    sys.stdout.flush()
