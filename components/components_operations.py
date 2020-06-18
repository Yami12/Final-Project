from utils import driver
from utils import string_list as sl
import datetime

def do_action(component, action , content):
    try:
        if action == sl.ACTION_CLICK:
            component.click()
        elif action == sl.ACTION_SEND_KEYS:
            if content == sl.MESSAGING_CONTENT:
                component.send_keys(driver.current_test[sl.MESSAGING_CONTENT])
                driver.sending_time = datetime.datetime.now()  # save the sending time
            elif content == sl.TEST_CONTACT:
                component.send_keys(driver.current_test[sl.CHAT_NAME][:-1])
            elif content == sl.CHILD_NAME:
                component.send_keys(driver.current_test[sl.CHILD_NAME][:-1])
            elif content == sl.WEBSITE:
                print(driver.current_test[sl.WEBSITE_ADDRESS])
                component.send_keys(driver.current_test[sl.WEBSITE_ADDRESS])
            else:
                component.send_keys(content)

        elif action == sl.ACTION_GET:
            component_text = component.get_attribute("text")
            return ['Passed', component_text]

        return ['Passed', "SUCCESS"]

    except Exception as e:
        return ['Failed', e]

def id_operation(resource_id, action, content):
    try:
        component = driver.global_driver.find_element_by_id(resource_id)
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



def component_operation(step):
    #id type
    if step[sl.TYPE_STEP] == sl.TYPE_ID:
        return id_operation(step[sl.ID_STEP], step[sl.ACTION_STEP], step[sl.CONTENT_STEP])
    #class type
    elif step[sl.TYPE_STEP] == sl.TYPE_CLASS:
        return class_operation(step[sl.ID_STEP], step[sl.ACTION_STEP], step[sl.CONTENT_STEP])
    #uiautomator type
    elif step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR:
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
