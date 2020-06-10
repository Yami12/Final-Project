from utils import driver
from utils import string_list as sl
import datetime

def do_action(component, action , content):
    try:
        if action == sl.ACTION_CLICK:
            print("in click")
            component.click()
        elif action == sl.ACTION_SEND_KEYS:
            if content == sl.MESSAGING_CONTENT:
                component.send_keys(driver.current_test[sl.MESSAGING_CONTENT])
                driver.sending_time = datetime.datetime.now()  # save the sending time
            elif content == sl.TEST_CONTACT:
                component.send_keys(driver.current_test[sl.CHILD_NAME][:-1])

        elif action == sl.ACTION_GET:
            component_text = component.get_attribute("text")
            return ['Passed', component_text]

        return ['Passed', "SUCCESS"]

    except Exception as e:
        return ['Failed', e]

def id_operation(resource_id, action, content):
    print(resource_id)
    try:
        component = driver.global_driver.find_element_by_id(resource_id)
        print(resource_id)
        return do_action(component, action, content)
    except Exception as e:
        return ['Failed', e]

def class_operation(resource_id, action, content):
    try:
        component = driver.global_driver.find_elements_by_class_name(resource_id)
        return do_action(component[0], action, content)

    except Exception as e:
        return ['Failed', e]

def uiautomator_operation(resource_id, action, content):
    try:
        component = driver.global_driver.find_element_by_android_uiautomator(resource_id)
        return do_action(component, action, content)
    except Exception as e:
        return ['Failed', e]


def xpath_operation(resource_id, action):
    try:
        component = driver.global_driver.find_element_by_xpath(resource_id)
        return do_action(component,action, "")
    except Exception as e:
        return ['Failed', e]


def component_operation(step):
    print(step)
    #id type
    if step[sl.TYPE_STEP] == sl.TYPE_ID:
        return id_operation(step[sl.ID_STEP], step[sl.ACTION_STEP], step[sl.CONTENT_STEP])
    #class type
    elif step[sl.TYPE_STEP] == sl.TYPE_CLASS:
        return class_operation(step[sl.ID_STEP], step[sl.ACTION_STEP], step[sl.CONTENT_STEP])
    #uiautomator type
    elif step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR:
        if step[sl.CONTENT_STEP] == sl.UIAUTOMATOR_CHAT_NAME:
            resource_id = 'new UiSelector().textContains("' + driver.current_test[sl.CHAT_NAME] + '")'
        elif step[sl.CONTENT_STEP] == 'Group info':
            resource_id = 'new UiSelector().textContains("Group info")'
        elif step[sl.CONTENT_STEP] == 'More options':
            resource_id = 'new UiSelector().descriptionContains("More options")'
        else:
            resource_id = 'new UiSelector().descriptionContains("' + step[sl.CONTENT_STEP] + '")'
        print(resource_id)
        return uiautomator_operation(resource_id, step[sl.ACTION_STEP], "")













# def button_operation(resours_id, action):
#     try:
#         component = driver.global_current_driver.find_element_by_id(resours_id)
#         if action == 'click':
#             component.click()
#             return ['Passed',"SUCCESS"]
#     except Exception as e:
#         return ['Failed', e]
#
#
# def input_operation(resours_id, content):
#     try:
#         input = driver.global_current_driver.find_element_by_id(resours_id)
#         input.send_keys(content)
#         return ['Passed','SUCCESS']
#     except Exception as e:
#         return ['Failed', e]
#
# def label_operation(resorce_id):
#     try:
#         error_message = driver.global_current_driver.find_element_by_id(resorce_id)
#         error_message_text = error_message.get_attribute("text")
#         return ['Passed', error_message_text]
#     except Exception as e:
#         return ['Failed', e]
#
# def toast_operation(resorce_id):
#     try:
#         error_message = driver.global_driver.find_element_by_xpath(resorce_id)
#         error_message_text = error_message.get_attribute("text")
#         return ['Passed', error_message_text]
#     except Exception as e:
#         return ['Failed', e]