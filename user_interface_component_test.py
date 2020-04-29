from tkinter import *
from main_tester import MainTester
import xml_parsing
from main_tester import MainTester

'''Accepts screen name making a move to it'''
def raise_frame(frame):
    frame.tkraise()


'''When: The user press the button on the "run_test_frame" screen
What: send name of flow to run function to run it'''
def run_test():
    MainTester.run_specific_flow(entry_run_flow.get())


'''When: The user press the button on the "add_component_behavior_frame" screen
What: Builds a new test with all fields as the user filled out and call to function that add the test to the requested flow'''
def add_component_behavior_ok():
    new_test = {}
    new_test['name'] = entry_add_test.get()
    new_test['resourceId'] = entry_add_resource.get()
    new_test['appActivity'] = entry_add_activity.get()
    new_test['type'] = component_type.get()

    final_expected_result = expected_result.get()
    if (final_expected_result == "toastMessage") or (final_expected_result == 'labelMessage'):
        #These types of expected results should also include text
        final_expected_result = final_expected_result + ":" + entry_message_content_add.get()
    new_test['expectedResult'] = final_expected_result

    selected = component_type.get()
    if selected == 'Button':
        new_test['actionType'] = action_type.get()
    elif selected == "Entry":
        new_test['content'] = entry_content.get()
    elif selected == 'CheckBox':
        new_test['expectedResult'] = 'pass'
        new_test['actionType'] = 'click'
    xml_parsing.add_new_test_to_flow(entry_add_flow.get(), new_test, 'xml_file.xml')#the third parameter


'''When: The user press the button on the "delete_component_behavior_frame" screen
What: send the flow name and the test name to function to delete this test'''
def delete_component_behavior_ok():
    xml_parsing.delete_test_from_flow(entry_delete_flow.get(), entry_delete_test.get(), 'xml_file.xml')#the third parameter


'''When: The user press the "update_button" button on the "update_component_behavior_frame" screen
What: send the update data to function that update the requested  test'''
def update_component_behavior_ok():
    action_or_content = '' #A variable that will contain action or content depending on the component type
    final_expected_result = expected_result_delete.get()
    if (final_expected_result == "toastMessage") or (final_expected_result == 'labelMessage'):
        #These types of expected results should also include text
        final_expected_result = final_expected_result + ":" + entry_message_content.get()
    selected = component_type_delete.get()
    if selected == 'Button':
        action_or_content = action_type_delete.get()
    elif selected == "Entry":
        action_or_content = entry_delete_content.get()
    elif selected == 'CheckBox':
        action_or_content = 'click'
        final_expected_result = 'pass'
    xml_parsing.update_test_in_flow(entry_update_flow.get(), entry_update_test.get(), final_expected_result, action_or_content, 'xml_file.xml')  # the third parameter


'''When: The user press the "continue_delete_button" button on the "add_component_behavior_frame" screen
What: Displays different data on the screen depending on the type of component the user selected'''
def continue_component_behavior_ok():
    test = xml_parsing.return_test(entry_update_flow.get(), entry_update_test.get(), 'xml_file.xml')#the third parameter
    type_component = test['type'] #the type of component the user selected
    component_type_delete_label.place(x=70, y=260)
    type_entry_delete.place(x=240, y=260)
    type_entry_delete.configure(state="disabled")
    component_type_delete.set(test['type'])
    update_button.place(x=170, y=400)
    if type_component == "Button":
        action_type_delete_label.place(x=70, y=290)
        action_type_delete_entry.place(x=240, y=290)
        action_type_delete.set(test['actionType'])
    elif type_component == "Entry":
        label_delete_content.place(x=70, y=290)
        entry_delete_content.place(x=240, y=290)
        entry_delete_content.delete(0, END)
        entry_delete_content.insert(0, test['content'])
    elif type_component == "CheckBox":
        return
    expected_result_delete_label.place(x=70, y=320)
    expected_result_delete_entry.place(x=240, y=320)
    expected_result_delete.set(test['expectedResult'])


'''When: The user selects a component type from OptionMenu
What: Displays different data on the screen depending on the type of component the user selected'''
def component_type_change(event):
    selected = component_type.get()
    type_entry.configure(state="disabled")
    if selected == "Button":
        action_type_label.place(x=70, y=260)
        action_type_entry.place(x=240, y=260)
    elif selected == "Entry":
        label_content.place(x=70, y=260)
        entry_content.place(x=240, y=260)
    elif selected == "CheckBox":
        return
    expected_result_label.place(x=70, y=290)
    expected_result_entry.place(x=240, y=290)


'''When: The user selects a expected result type from OptionMenu
What: Displays different data on the screen depending on the type of expected result the user selected'''
def expected_result_add(event):
    selected = expected_result.get()
    expected_result_entry.configure(state="disabled")
    if (selected == "toastMessage") or (selected == 'labelMessage'):
        label_message_content_add.place(x=70, y=330)
        entry_message_content_add.place(x=240, y=330)


'''When: The user selects a expected result type from OptionMenu
What: Displays different data on the screen depending on the type of expected result the user selected'''
def expected_result_update(event):
    selected = expected_result_delete.get()
    expected_result_delete_entry.configure(state="disabled")
    if (selected == "toastMessage") or (selected == 'labelMessage'):
        label_message_content.place(x=70, y=360)
        entry_message_content.place(x=240, y=360)


#Visual display of screens
main_win = Tk()
main_win.geometry('500x500')
main_win.title("Registration Form")

#define 5 frames, each represents a screen
run_test_frame = Frame(main_win)
run_test_frame.place(x=0, y=0, width=500, height=500)

add_component_behavior_frame = Frame(main_win)
add_component_behavior_frame.place(x=0, y=0, width=500, height=500)

delete_component_behavior_frame = Frame(main_win)
delete_component_behavior_frame.place(x=0, y=0, width=500, height=500)

update_component_behavior_frame = Frame(main_win)
update_component_behavior_frame.place(x=0, y=0, width=500, height=500)

main_frame = Frame(main_win)
main_frame.place(x=0, y=0, width=500, height=500)

'''main_frame
The main screen of component behavior tests
The user can choose action on tests'''
Label(main_frame, text="Choose the desired action", width=20, font=("bold", 20)).place(x=90, y=53)

Label(main_frame, text="run test", width=30, font=("bold", 10)).place(x=30, y=150)
Button(main_frame, text='run', width=20, bg='brown', fg='white', command=lambda: raise_frame(run_test_frame)).place(x=250, y=150)

Label(main_frame, text="add a component behavior test", width=30, font=("bold", 10)).place(x=30, y=200)
Button(main_frame, text='add', width=20, bg='brown', fg='white', command=lambda: raise_frame(add_component_behavior_frame)).place(x=250, y=200)

Label(main_frame, text="delete a component behavior test", width=30, font=("bold", 10)).place(x=30, y=250)
Button(main_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: raise_frame(delete_component_behavior_frame)).place(x=250, y=250)

Label(main_frame, text="update a component behavior test", width=30, font=("bold", 10)).place(x=30, y=300)
Button(main_frame, text='update', width=20, bg='brown', fg='white', command=lambda: raise_frame(update_component_behavior_frame)).place(x=250, y=300)

'''run_test_frame
A screen where the user can enter details of a specific component behavior test and run it'''
Label(run_test_frame, text="flow name:", width=20, font=("bold", 10)).place(x=80, y=80)
entry_run_flow = Entry(run_test_frame)
entry_run_flow.place(x=240, y=80)

Button(run_test_frame, text='run', width=20, bg='brown', fg='white', command=lambda: run_test()).place(x=170, y=300)

'''add_component_behavior_frame
Screen where user can add new test to existing tests'''
Label(add_component_behavior_frame, text="add component behavior frame form", width=20, font=("bold", 20)).place(x=90, y=30)

Label(add_component_behavior_frame, text="flow name:", width=20, font=("bold", 10)).place(x=80, y=80)
entry_add_flow = Entry(add_component_behavior_frame)
entry_add_flow.place(x=240, y=80)

Label(add_component_behavior_frame, text="test name:", width=20, font=("bold", 10)).place(x=80, y=110)
entry_add_test = Entry(add_component_behavior_frame)
entry_add_test.place(x=240, y=110)

Label(add_component_behavior_frame, text="resource id:", width=20, font=("bold", 10)).place(x=80, y=150)
entry_add_resource = Entry(add_component_behavior_frame)
entry_add_resource.place(x=240, y=150)

Label(add_component_behavior_frame, text="app activity:", width=20, font=("bold", 10)).place(x=80, y=180)
entry_add_activity = Entry(add_component_behavior_frame)
entry_add_activity.place(x=240, y=180)

Label(add_component_behavior_frame, text="What component type:", width=20, font=("bold", 10)).place(x=70, y=220)
component_type = StringVar() # there is the rule: variable name lowercase with _
type_entry = OptionMenu(add_component_behavior_frame, component_type, "Button", "Label", "CheckBox", command=component_type_change)
type_entry.place(x=240, y=220)
component_type.set("select your component type")

expected_result_label = Label(add_component_behavior_frame, text="What expected result:", width=20, font=("bold", 10))
expected_result = StringVar()  # there is the rule: variable name lowercase with _
expected_result_entry = OptionMenu(add_component_behavior_frame, expected_result, "disabled", 'toastMessage', 'labelMessage‏'
                                   , command=expected_result_add)
expected_result.set("select your expected result")

Button(add_component_behavior_frame, text='OK', width=20, bg='brown', fg='white', command=lambda: add_component_behavior_ok()).place(x=170, y=400)

#if button this is the type of component the user has selected, these component will appear
action_type_label = Label(add_component_behavior_frame, text="What action type:", width=20, font=("bold", 10))
action_type = StringVar()  # there is the rule: variable name lowercase with _
action_type_entry = OptionMenu(add_component_behavior_frame, action_type, "click", "over")
action_type.set("select your action type")

#if label this is the type of component the user has selected, these component will appear
label_content = Label(add_component_behavior_frame, text="content:", width=20, font=("bold", 10))
entry_content = Entry(add_component_behavior_frame)

#if expected result is a "message" type, the following component will appear
label_message_content_add = Label(add_component_behavior_frame, text="message:", width=20, font=("bold", 10))
entry_message_content_add = Entry(add_component_behavior_frame)


'''delete_component_behavior_frame
Screen where user can delete existing tests'''
Label(delete_component_behavior_frame, text="delete component behavior frame form", width=30, font=("bold", 16)).place(x=90, y=53)

Label(delete_component_behavior_frame, text="flow name:", width=20, font=("bold", 10)).place(x=80, y=130)
entry_delete_flow = Entry(delete_component_behavior_frame)
entry_delete_flow.place(x=240, y=130)

Label(delete_component_behavior_frame, text="test name:", width=20, font=("bold", 10)).place(x=80, y=180)
entry_delete_test = Entry(delete_component_behavior_frame)
entry_delete_test.place(x=240, y=180)

Button(delete_component_behavior_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: delete_component_behavior_ok()).place(x=170, y=400)

'''update_component_behavior_frame
Screen where user can update existing tests'''
Label(update_component_behavior_frame, text="update component behavior frame form", width=30, font=("bold", 16)).place(x=90, y=53)

Label(update_component_behavior_frame, text="flow name:", width=20, font=("bold", 10)).place(x=80, y=130)
entry_update_flow = Entry(update_component_behavior_frame)
entry_update_flow.place(x=240, y=130)

Label(update_component_behavior_frame, text="test name:", width=20, font=("bold", 10)).place(x=80, y=170)
entry_update_test = Entry(update_component_behavior_frame)
entry_update_test.place(x=240, y=170)

continue_delete_button = Button(update_component_behavior_frame, text='continue', width=20, bg='brown', fg='white', command=lambda: continue_component_behavior_ok()).place(x=170, y=210)

component_type_delete_label = Label(update_component_behavior_frame, text="What component type:", width=20, font=("bold", 10))
component_type_delete = StringVar() # there is the rule: variable name lowercase with _
type_entry_delete = OptionMenu(update_component_behavior_frame, component_type_delete, "Button", "Entry", "CheckBox", command=component_type_change)
component_type_delete.set("select your component type")

expected_result_delete_label = Label(update_component_behavior_frame, text="What expected result:", width=20, font=("bold", 10))
expected_result_delete = StringVar()  # there is the rule: variable name lowercase with _
expected_result_delete_entry = OptionMenu(update_component_behavior_frame, expected_result_delete, "disabled",
                                          'toastMessage', 'labelMessage‏', command=expected_result_update)
expected_result_delete.set("select your expected result")

update_button = Button(update_component_behavior_frame, text='update', width=20, bg='brown', fg='white', command=lambda: update_component_behavior_ok())

#if button this is the type of component the user has selected, these component will appear
action_type_delete_label = Label(update_component_behavior_frame, text="What action type:", width=20, font=("bold", 10))
action_type_delete = StringVar()  # there is the rule: variable name lowercase with _
action_type_delete_entry = OptionMenu(update_component_behavior_frame, action_type_delete, "click", "over")
action_type_delete.set("select your action type")

#if entry this is the type of component the user has selected, these component will appear
label_delete_content = Label(update_component_behavior_frame, text="content:", width=20, font=("bold", 10))
entry_delete_content = Entry(update_component_behavior_frame)

#if expected result is a "message" type, the following component will appear
label_message_content = Label(update_component_behavior_frame, text="message:", width=20, font=("bold", 10))
entry_message_content = Entry(update_component_behavior_frame)

#Starts the program by displaying the first screen
def run_component_test():
    main_win.mainloop()
