from tkinter import *
from utils import xml_parsing
from utils import main_tester
from threading import Thread
from utils import string_list as sl
import ast

tests = xml_parsing.tests_xml_to_dictionary(sl.COMPONENTS_FILE)
tests_names = [x[sl.TEST_NAME] for x in tests]
steps = ["choose test"]
flag_delete_update = True # delete=True, update=False


#Starts the program by displaying the first screen
def run_component_test():
    main_win.mainloop()


'''Accepts screen name making a move to it'''
def raise_frame(frame):
    frame.tkraise()

def open_delete_frame():
    delete_step_button.place(x=170, y=350)
    delete_test_button.place(x=170, y=400)
    raise_frame(delete_component_behavior_frame)

def open_update_frame():
    global flag_delete_update
    flag_delete_update = False
    continue_update_button.place(x=170, y=200)
    raise_frame(delete_component_behavior_frame)

'''When: The user press the button on the "run_test_frame" screen
What: send name of flow to run function to run it'''
def run_test():
    if run_flow_s.get() != sl.NOT_SELECTED:
        main_tester.MainTester().run_specific_behvior_flow(run_flow_s.get())


'''When: The user press the button on the "add_component_behavior_frame" screen
What: Builds a new test with all fields as the user filled out and call to function that add the test to the requested flow'''
def add_component_behavior_test_ok():
    new_test = {}
    new_test[sl.TEST_NAME] = entry_add_test.get()
    final_expected_result = expected_result_type.get()
    if (final_expected_result == sl.TOASTMESSAGE) or (final_expected_result == sl.LABELMESSAGE):
        #These types of expected results should also include text
        final_expected_result = final_expected_result + ":" + entry_message_content_add.get()
    new_test[sl.TEST_EXPECTED_RES] = final_expected_result
    new_test[sl.STEPS] = steps
    xml_parsing.add_new_item_to_xml(new_test, sl.COMPONENTS_FILE)

def add_step_to_test_ok():
    global steps
    new_step = {}
    new_step[sl.TYPE_STEP] = entry_type_step.get()
    new_step[sl.ID_STEP] = entry_id_step.get()
    new_step[sl.ACTION_STEP] = entry_action_step.get()
    new_step[sl.CONTENT_STEP] = entry_content_step.get()
    steps.append(new_step)

    entry_type_step.delete(0, END)
    entry_type_step.insert(0, "")
    entry_id_step.delete(0, END)
    entry_id_step.insert(0, "")
    entry_action_step.delete(0, END)
    entry_action_step.insert(0, "")
    entry_content_step.delete(0, END)
    entry_content_step.insert(0, "")


'''When: The user press the button on the "delete_component_behavior_frame" screen to delete all the test
What: send the flow name and the test name to function to delete this test'''
def delete_test_ok():
    xml_parsing.delete_test(delete_test_name.get(), sl.COMPONENTS_FILE)

'''When: The user press the button on the "delete_component_behavior_frame" screen to delete specific step in the test
What: send the flow name and the test name to function to delete this test'''
def delete_step_ok():
    xml_parsing.delete_step_from_test(delete_test_name.get(), delete_step_name.get(), sl.COMPONENTS_FILE)

def choose_test_to_delete(test_name):
    global steps
    for test in tests:
        if test[sl.TEST_NAME] == test_name:
            steps = test[sl.STEPS]
            entry_delete_step_name.children["menu"].delete(0, 'end')
            for step in steps:
                entry_delete_step_name.children["menu"].add_command(label=step, command=lambda value=step: delete_step_name.set(value))

def choose_step_from_test():
    if flag_delete_update == False:
        step_type_label.place(x=80, y=250)
        step_type_entry.place(x=240, y=250)
        step_id_label.place(x=80, y=280)
        step_id_entry.place(x=240, y=280)
        step_action_label.place(x=80, y=310)
        step_action_entry.place(x=240, y=310)
        step_content_label.place(x=80, y=340)
        step_content_entry.place(x=240, y=340)
        update_test_button.place(x=170, y=400)

        specific_step = delete_step_name.get()
        specific_step = ast.literal_eval(specific_step)

        step_type_entry.insert(0, str(specific_step[sl.TYPE_STEP]))
        step_id_entry.insert(0, specific_step[sl.ID_STEP])
        step_action_entry.insert(0, specific_step[sl.ACTION_STEP])
        step_content_entry.insert(0, specific_step[sl.CONTENT_STEP])

'''When: The user press the "update_button" button on the "update_component_behavior_frame" screen
What: send the update data to function that update the requested  test'''
def update_component_behavior_ok():
    old_step = ast.literal_eval(delete_step_name)
    new_step = {}
    new_step[sl.TYPE_STEP] = step_type_entry.get()
    new_step[sl.ID_STEP] = step_id_entry.get()
    new_step[sl.ACTION_STEP] = step_action_entry.get()
    new_step[sl.CONTENT_STEP] = step_content_entry.get()

    xml_parsing.update_tests(delete_test_name, old_step, new_step, sl.COMPONENTS_FILE)


'''When: The user selects a component type from OptionMenu
What: Displays different data on the screen depending on the type of component the user selected'''
def expected_result_change(event):
    selected = expected_result_type.get()
    expected_result_entry.configure(state="disabled")
    if selected == sl.TOASTMESSAGE or selected == sl.LABELMESSAGE:
        label_content.place(x=70, y=190)
        entry_message_content_add.place(x=240, y=190)


run_test_thread = Thread(target=run_test)

#Visual display of screens
main_win = Tk()
main_win.geometry('500x500')
main_win.title("Registration Form")

#define 5 frames, each represents a screen
run_test_frame = Frame(main_win)
run_test_frame.place(x=0, y=0, width=500, height=500)

add_component_behavior_test_frame = Frame(main_win)
add_component_behavior_test_frame.place(x=0, y=0, width=500, height=500)

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
Button(main_frame, text='add', width=20, bg='brown', fg='white', command=lambda: raise_frame(add_component_behavior_test_frame)).place(x=250, y=200)

Label(main_frame, text="delete a component behavior test", width=30, font=("bold", 10)).place(x=30, y=250)
Button(main_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: open_delete_frame()).place(x=250, y=250)

Label(main_frame, text="update a component behavior test", width=30, font=("bold", 10)).place(x=30, y=300)
Button(main_frame, text='update', width=20, bg='brown', fg='white', command=lambda: open_update_frame()).place(x=250, y=300)

'''run_test_frame
A screen where the user can enter details of a specific component behavior test and run it'''
Label(run_test_frame, text="choose the test::", width=20, font=("bold", 10)).place(x=170, y=80)

run_flow_s = StringVar()
entry_run_flow = OptionMenu(run_test_frame, run_flow_s, *tests_names)
entry_run_flow.place(x=170, y=140)
run_flow_s.set(sl.NOT_SELECTED)

Button(run_test_frame, text='run', width=20, bg='brown', fg='white', command=lambda: run_test_thread.start()).place(x=170, y=300)

'''add_component_behavior_test_frame
Screen where user can add new test to existing tests'''
Label(add_component_behavior_test_frame, text="add component behavior frame form", width=20, font=("bold", 20)).place(x=90, y=30)

Label(add_component_behavior_test_frame, text="test name:", width=20, font=("bold", 10)).place(x=80, y=110)
entry_add_test = Entry(add_component_behavior_test_frame)
entry_add_test.place(x=240, y=110)

Label(add_component_behavior_test_frame, text="What expected result:", width=20, font=("bold", 10)).place(x=70, y=150)
expected_result_type = StringVar() # there is the rule: variable name lowercase with _
expected_result_entry = OptionMenu(add_component_behavior_test_frame, expected_result_type, "toastMessage", "disabled", "labelMessage‏", command=expected_result_change)
expected_result_entry.place(x=240, y=150)
expected_result_type.set(sl.NOT_SELECTED)

#add steps to test
Label(add_component_behavior_test_frame, text="type step:", width=20, font=("bold", 10)).place(x=80, y=240)
entry_type_step = Entry(add_component_behavior_test_frame)
entry_type_step.place(x=240, y=240)
Label(add_component_behavior_test_frame, text="id step:", width=20, font=("bold", 10)).place(x=80, y=260)
entry_id_step = Entry(add_component_behavior_test_frame)
entry_id_step.place(x=240, y=260)
Label(add_component_behavior_test_frame, text="action step:", width=20, font=("bold", 10)).place(x=80, y=280)
entry_action_step = Entry(add_component_behavior_test_frame)
entry_action_step.place(x=240, y=280)
Label(add_component_behavior_test_frame, text="content step:", width=20, font=("bold", 10)).place(x=80, y=300)
entry_content_step = Entry(add_component_behavior_test_frame)
entry_content_step.place(x=240, y=300)
Button(add_component_behavior_test_frame, text='Add Step To Test', width=20, bg='brown', fg='white', command=lambda: add_step_to_test_ok()).place(x=170, y=320)

Button(add_component_behavior_test_frame, text='Add Test', width=20, bg='brown', fg='white', command=lambda: add_component_behavior_test_ok()).place(x=170, y=400)

#if expected result is a "message" type, the following component will appear
label_content = Label(add_component_behavior_test_frame, text="message:", width=20, font=("bold", 10))
entry_message_content_add = Entry(add_component_behavior_test_frame)

'''delete_component_behavior_frame
Screen where user can delete existing tests'''

Label(delete_component_behavior_frame, text="choose the test:", width=20, font=("bold", 10)).place(x=70, y=80)
delete_test_name = StringVar()
entry_delete_test_name = OptionMenu(delete_component_behavior_frame, delete_test_name, *tests_names, command=choose_test_to_delete)
entry_delete_test_name.place(x=200, y=80)
delete_test_name.set(sl.NOT_SELECTED)

Label(delete_component_behavior_frame, text="choose the step:", width=20, font=("bold", 10)).place(x=70, y=150)
delete_step_name = StringVar()
entry_delete_step_name = OptionMenu(delete_component_behavior_frame, delete_step_name, *steps)
entry_delete_step_name.place(x=200, y=150)
delete_step_name.set(sl.NOT_SELECTED)

continue_update_button = Button(delete_component_behavior_frame, text='to continue', width=20, bg='brown', fg='white', command=choose_step_from_test)

#if this is delete fram
delete_step_button = Button(delete_component_behavior_frame, text='delete specific step', width=20, bg='brown', fg='white', command=lambda: delete_step_ok())
delete_test_button = Button(delete_component_behavior_frame, text='delete all the steps', width=20, bg='brown', fg='white', command=lambda: delete_test_ok())

#if this is update fram
step_type_label = Label(delete_component_behavior_frame, text="type of step:", width=20, font=("bold", 10))
step_type_entry = Entry(delete_component_behavior_frame)

step_id_label = Label(delete_component_behavior_frame, text="id of step:", width=20, font=("bold", 10))
step_id_entry = Entry(delete_component_behavior_frame)

step_action_label = Label(delete_component_behavior_frame, text="action of step:", width=20, font=("bold", 10))
step_action_entry = Entry(delete_component_behavior_frame)

step_content_label = Label(delete_component_behavior_frame, text="content of step:", width=20, font=("bold", 10))
step_content_entry = Entry(delete_component_behavior_frame)

update_test_button = Button(delete_component_behavior_frame, text='update test', width=20, bg='brown', fg='white', command=lambda: update_component_behavior_ok())
