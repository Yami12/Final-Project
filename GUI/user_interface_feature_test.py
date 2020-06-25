from tkinter import *
from threading import Thread
from utils import xml_parsing
from utils import string_list as sl
from utils import driver

tests = xml_parsing.feature_xml_to_dictionary(sl.MESSAGING_FEATURE_FILE)
tests_names = [x[sl.TEST_NAME] for x in tests]
social_networks = xml_parsing.tests_xml_to_dictionary("applications.xml")
social_networks_name = [x[sl.APP_NAME] for x in social_networks]
steps = []
steps_group = []

#Starts the program by displaying the first screen
def run_messaging_feature_test():
    main_window.mainloop()

def send_message():
    if feature_tests.get() != sl.NOT_SELECTED:
        from utils import main_tester
        main_tester.MainTester().run_messaging_feature_test(feature_tests.get(), social_network.get())
        button_run_message.configure(background="brown")
        button_run_message["state"] = "active"


'''Accepts screen name making a move to it'''
def raise_frame(frame):
    frame.tkraise()


def add_social_network():
    new_social_network = {}
    new_social_network[sl.S_NETWORK_NAME] = entry_name_social_network.get()
    new_social_network[sl.APP_PACKAGE] = entry_app_package_social_network.get()
    new_social_network[sl.APP_ACTIVITY] = entry_app_activity_social_network.get()
    new_social_network[sl.PARENT_NAME] = entry_parent_name_social_network.get()
    new_social_network[sl.CHILD_NAME] = entry_child_name_social_network.get()
    new_social_network[sl.STEPS] = steps
    xml_parsing.add_new_item_to_xml(new_social_network, sl.NETWORKS_FILE)

    new_social_network_remove_group = {}
    new_social_network_remove_group[sl.S_NETWORK_NAME] = entry_name_social_network.get()
    new_social_network_remove_group[sl.GROUP_NAME] = entry_group_name_remove.get()
    new_social_network_remove_group[sl.STEPS] = steps_group
    xml_parsing.add_new_item_to_xml(new_social_network_remove_group, sl.REMOVE_GROUP_FILE)

def add_step(type, id, action, content):
    new_step = {}
    new_step[sl.TYPE_STEP] = type.get()
    new_step[sl.ID_STEP] = id.get()
    new_step[sl.ACTION_STEP] = action.get()
    new_step[sl.CONTENT_STEP] = content.get()

    type.delete(0, END)
    type.insert(0, "")
    id.delete(0, END)
    id.insert(0, "")
    action.delete(0, END)
    action.insert(0, "")
    content.delete(0, END)
    content.insert(0, "")

    return new_step

def add_step_to_social_network():
    global steps
    steps.append(add_step(entry_type_step, entry_id_step, entry_action_step, entry_content_step))


def add_step_to_removal_from_group():
    global steps_group
    steps_group.append(add_step(entry_type_step_remove, entry_id_step_remove, entry_action_step_remove, entry_content_step_remove))


def run_all_messaging_tests():
    from utils import main_tester
    main_tester.MainTester().run_messaging_feature_test(sl.ALL, sl.ALL)


def removal_from_group():
    return


def thread_send_messaging():
    button_run_message.configure(background="gray")
    button_run_message["state"] = "disabled"
    send_message_thread = Thread(target=send_message)
    send_message_thread.start()


#Visual display of screens
main_window = Tk()
main_window.geometry('500x500')
main_window.title("Keepers")

#define frames, each represents a screen
run_messaging_test_frame = Frame(main_window)
run_messaging_test_frame.place(x=0, y=0, width=500, height=500)

main_messaging_test_frame = Frame(main_window)
main_messaging_test_frame.place(x=0, y=0, width=500, height=500)

add_social_network_frame = Frame(main_window)
add_social_network_frame.place(x=0, y=0, width=500, height=500)

main_feature_test_frame = Frame(main_window)
main_feature_test_frame.place(x=0, y=0, width=500, height=500)

'''run_messaging_test_frame'''
Label(run_messaging_test_frame, text="Choose test", width=20, font=("bold", 20)).place(x=80, y=30)

feature_tests = StringVar()
feature_tests_entry = OptionMenu(run_messaging_test_frame, feature_tests, *tests_names)
feature_tests_entry.place(x=180, y=140)
feature_tests.set(sl.NOT_SELECTED)

Label(run_messaging_test_frame, text="social network:", width=20, font=("bold", 10)).place(x=80, y=350)
social_network = StringVar()
social_network_entry = OptionMenu(run_messaging_test_frame, social_network, *social_networks_name)
social_network_entry.place(x=240, y=350)
social_network.set(sl.NOT_SELECTED)

button_run_message = Button(run_messaging_test_frame, text='start test', width=20, bg='brown', fg='white', command=lambda: thread_send_messaging())
button_run_message.place(x=170, y=400)

'''main_messaging_test_frame'''
Button(main_messaging_test_frame, text='run all send messaging tests', width=20, bg='brown', fg='white', command=run_all_messaging_tests).place(x=180, y=220)
Button(main_messaging_test_frame, text='run specific messaging test', width=20, bg='brown', fg='white', command=lambda: raise_frame(run_messaging_test_frame)).place(x=180, y=290)

'''add_social_network_frame'''
Label(add_social_network_frame, text="social network name:", width=20, font=("bold", 10)).place(x=80, y=20)
entry_name_social_network = Entry(add_social_network_frame)
entry_name_social_network.place(x=250, y=20)
Label(add_social_network_frame, text="social network app package:", width=20, font=("bold", 10)).place(x=80, y=40)
entry_app_package_social_network = Entry(add_social_network_frame)
entry_app_package_social_network.place(x=250, y=40)
Label(add_social_network_frame, text="social network app activity:", width=20, font=("bold", 10)).place(x=80, y=60)
entry_app_activity_social_network = Entry(add_social_network_frame)
entry_app_activity_social_network.place(x=250, y=60)
Label(add_social_network_frame, text="social network parent name:", width=20, font=("bold", 10)).place(x=80, y=80)
entry_parent_name_social_network = Entry(add_social_network_frame)
entry_parent_name_social_network.place(x=250, y=80)
Label(add_social_network_frame, text="social network child name:", width=20, font=("bold", 10)).place(x=80, y=100)
entry_child_name_social_network = Entry(add_social_network_frame)
entry_child_name_social_network.place(x=250, y=100)

#add steps to social network
Label(add_social_network_frame, text="type step:", width=20, font=("bold", 10)).place(x=80, y=150)
entry_type_step = Entry(add_social_network_frame)
entry_type_step.place(x=250, y=150)
Label(add_social_network_frame, text="id step:", width=20, font=("bold", 10)).place(x=80, y=170)
entry_id_step = Entry(add_social_network_frame)
entry_id_step.place(x=250, y=170)
Label(add_social_network_frame, text="action step:", width=20, font=("bold", 10)).place(x=80, y=190)
entry_action_step = Entry(add_social_network_frame)
entry_action_step.place(x=250, y=190)
Label(add_social_network_frame, text="content step:", width=20, font=("bold", 10)).place(x=80, y=210)
entry_content_step = Entry(add_social_network_frame)
entry_content_step.place(x=250, y=210)
Button(add_social_network_frame, text='add step to social network', width=20, bg='brown', fg='white', command=lambda: add_step_to_social_network()).place(x=170, y=230)

#add steps to removal from group
Label(add_social_network_frame, text="group name:", width=20, font=("bold", 10)).place(x=80, y=280)
entry_group_name_remove = Entry(add_social_network_frame)
entry_group_name_remove.place(x=250, y=280)
Label(add_social_network_frame, text="type step:", width=20, font=("bold", 10)).place(x=80, y=320)
entry_type_step_remove = Entry(add_social_network_frame)
entry_type_step_remove.place(x=250, y=320)
Label(add_social_network_frame, text="id step:", width=20, font=("bold", 10)).place(x=80, y=340)
entry_id_step_remove = Entry(add_social_network_frame)
entry_id_step_remove.place(x=250, y=340)
Label(add_social_network_frame, text="action step:", width=20, font=("bold", 10)).place(x=80, y=360)
entry_action_step_remove = Entry(add_social_network_frame)
entry_action_step_remove.place(x=250, y=360)
Label(add_social_network_frame, text="content step:", width=20, font=("bold", 10)).place(x=80, y=380)
entry_content_step_remove = Entry(add_social_network_frame)
entry_content_step_remove.place(x=250, y=380)
Button(add_social_network_frame, text='add step to removal from group', width=20, bg='brown', fg='white', command=lambda: add_step_to_removal_from_group()).place(x=170, y=400)

Button(add_social_network_frame, text='Add social network', width=20, bg='brown', fg='white', command=lambda: add_social_network()).place(x=170, y=460)

'''main_feature_test_frame'''
Button(main_feature_test_frame, text='messaging tests', width=20, bg='brown', fg='white', command=lambda: raise_frame(main_messaging_test_frame)).place(x=180, y=100)
Button(main_feature_test_frame, text='removal from group test', width=20, bg='brown', fg='white', command=removal_from_group).place(x=180, y=180)
Button(main_feature_test_frame, text='add social network', width=20, bg='brown', fg='white', command=lambda: raise_frame(add_social_network_frame)).place(x=180, y=260)


run_messaging_feature_test()