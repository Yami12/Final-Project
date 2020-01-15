import driver


def button_click(resours_id):
    component = driver.global_driver.find_element_by_id(resours_id)
    component.click()


def input_send_keys(resours_id, content):
    input = driver.global_driver.find_element_by_id(resours_id)
    input.send_keys(content)
     