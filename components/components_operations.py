"""
This file performs actions on requested components
"""
import datetime

from utils import driver
from utils import string_list as sl
from utils import utils_funcs as uf


'''
accepts: component, action, content
do: executing the action on the component
if the action is send key, do the action by her content
return: if the action succeeded or not
'''
def do_action(component, action , content):
    uf.print_log("\cf1 " + action)
    try:
        if action == sl.ACTION_CLICK: # click on the component
            component.click()
            return [sl.TEST_PASSED, "Click" ]
        elif action == sl.ACTION_SEND_KEYS: # send keys to the components
            if content == sl.MESSAGING_CONTENT: #send message content
                component.send_keys(driver.current_test[sl.MESSAGING_CONTENT])
                driver.sending_time = datetime.datetime.now()
                return [sl.TEST_PASSED, "Send keys: " + driver.current_test[sl.MESSAGING_CONTENT]]
            elif content == sl.TEST_CONTACT: # sent chat name
                component.send_keys(driver.current_test[sl.CHAT_NAME][:-1])
                return [sl.TEST_PASSED, "Send keys: " + driver.current_test[sl.CHAT_NAME][:-1]]
            elif content == sl.CHILD_NAME: # send child name
                component.send_keys(driver.current_test[sl.CHILD_NAME][:-1])
                return [sl.TEST_PASSED, "Send keys: " + driver.current_test[sl.CHILD_NAME][:-1]]
            else: # send content
                component.send_keys(content)
                return [sl.TEST_PASSED, "Send keys: " + content]

        elif action == sl.ACTION_GET: # get component content
            #get the component text
            component_text = component.get_attribute("text")
            uf.print_log("\cf1  SUCCESS \line")
            return [sl.TEST_PASSED, component_text]

        uf.print_log("\cf1  success \line")

    except Exception as e:
        uf.print_log("\cf2  failed \line")
        return [sl.TEST_FAILED, e]

'''
get the component by resource id
send to do_action function
return: if succeeded to find the component or not
'''
def id_operation(resource_id, action, content):
    uf.print_log("\cf1 " + resource_id + "  ")
    try:
        component = driver.global_driver.find_element_by_id(resource_id)
        return do_action(component, action, content)
    except Exception as e:
        return [sl.TEST_FAILED, e]

'''
get the component by class
send to do_action function
return: if succeeded to find the component or not
'''
def class_operation(resource_id, action, content):
    uf.print_log("\cf1 " + resource_id + "  ")
    try:
        component = driver.global_driver.find_elements_by_class_name(resource_id)
        return do_action(component[0], action, content)
    except Exception as e:
        return [sl.TEST_FAILED, e]


'''
get the component by uiautomator
send to do_action function
return: if succeeded to find the component or not
'''
def uiautomator_operation(resource_id, action, content):
    uf.print_log("\cf1 " + resource_id + "  ")
    try:
        component = driver.global_driver.find_element_by_android_uiautomator(resource_id)
        return do_action(component, action, content)
    except Exception as e:
        return [sl.TEST_FAILED, e]


'''
accept step and send his components to the appropriate function with the appropriate id
return if the called function succeeded or not
'''
def component_operation(step):
    #id type
    if step[sl.TYPE_STEP] == sl.TYPE_ID:
        return id_operation(step[sl.ID_STEP], step[sl.ACTION_STEP], step[sl.CONTENT_STEP])
    #class type
    elif step[sl.TYPE_STEP] == sl.TYPE_CLASS:
        return class_operation(step[sl.ID_STEP], step[sl.ACTION_STEP], step[sl.CONTENT_STEP])
    #uiautomator type
    elif step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR:
        #find the text that identify the component by the steps content
        if step[sl.CONTENT_STEP] == sl.CHAT_NAME:
            resource_id = 'new UiSelector().textContains("' + driver.current_test[sl.CHAT_NAME] + '")'
        elif step[sl.CONTENT_STEP] == sl.CHILD_NAME:
            resource_id = 'new UiSelector().textContains("' + driver.current_test[sl.CHILD_NAME] + '")'
        elif "text:" in step[sl.CONTENT_STEP]:
            resource_id = 'new UiSelector().textContains("' + str(step[sl.CONTENT_STEP]).split("text:")[1] + '")'
        elif "desc:" in step[sl.CONTENT_STEP]:
            resource_id = 'new UiSelector().descriptionContains("' + str(step[sl.CONTENT_STEP]).split("desc:")[1] + '")'
        elif "resourceid-" in step[sl.CONTENT_STEP]:
            resource_id = 'new UiSelector().resourceId("' + str(step[sl.CONTENT_STEP]).split("-")[2] + '")'
        else:
            resource_id = 'new UiSelector().descriptionContains("' + step[sl.CONTENT_STEP] + '")'
        return uiautomator_operation(resource_id, step[sl.ACTION_STEP], "")
