from tkinter import *
import tkinter
import xml_parsing


def raise_frame(frame):
    frame.tkraise()


def add_component_behavior_ok():
    selected = component_type.get()
    new_test = {}
    new_test['name'] = entry_add_test.get()
    new_test['resourceId'] = entry_add_resource.get()
    new_test['appActivity'] = entry_add_activity.get()
    new_test['type'] = component_type.get()
    new_test['expectedResult'] = expected_result.get()
    if selected == 'Button':
        new_test['actionType'] = action_type.get()
    elif selected == "Label":
        new_test['content'] = entry_content.get()
    xml_parsing.add_new_test_to_flow(entry_add_flow.get(), new_test, 'xml_file.xml')#the third parameter


def delete_component_behavior_ok():
    xml_parsing.delete_test_from_flow(entry_delete_flow.get(), entry_delete_test.get(), 'xml_file.xml')#the third parameter


def update_component_behavior_ok():
    return


def continue_component_behavior_ok():
    #continue_delete_button
    test = xml_parsing.return_test(entry_delete_flow.get(), entry_delete_test.get(), 'xml_file.xml')#the third parameter
    type_component = test['type']
    component_type_delete_label.place(x=70, y=260)
    type_entry_delete.place(x=240, y=260)
    type_entry_delete.configure(state="disabled")
    component_type_delete.set(test['type'])
    if type_component == "Button":
        action_type_delete_label.place(x=70, y=290)
        action_type_delete_entry.place(x=240, y=290)
        action_type_delete.set(test['actionType'])
    elif type_component == "Label":
        label_delete_content.place(x=70, y=290)
        entry_delete_content.place(x=240, y=290)
        entry_delete_content.delete(0, END)
        entry_delete_content.insert(0, test['content'])
    # elif selected == "Check Box":
    #     print()
    # elif selected == "List":
    #     print()
    expected_result_delete_label.place(x=70, y=320)
    expected_result_delete_entry.place(x=240, y=320)
    expected_result_delete.set(test['expectedResult'])
    update_button.place(x=170, y=400)


def component_type_change(event):
    selected = component_type.get()
    type_entry.configure(state="disabled")
    if selected == "Button":
        action_type_label.place(x=70, y=260)
        action_type_entry.place(x=240, y=260)
    elif selected == "Label":
        label_content.place(x=70, y=260)
        entry_content.place(x=240, y=260)

    # elif selected == "Check Box":
    #     print()
    # elif selected == "List":
    #     print()
    expected_result_label.place(x=70, y=290)
    expected_result_entry.place(x=240, y=290)


main_win = Tk()
main_win.geometry('500x500')
main_win.title("Registration Form")

#define frames

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

#main_frame
Label(main_frame, text="Choose the desired action", width=20, font=("bold", 20)).place(x=90, y=53)

Label(main_frame, text="run test", width=30, font=("bold", 10)).place(x=30, y=150)
Button(main_frame, text='run', width=20, bg='brown', fg='white', command=lambda: raise_frame(run_test_frame)).place(x=250, y=150)

Label(main_frame, text="add a component behavior test", width=30, font=("bold", 10)).place(x=30, y=200)
Button(main_frame, text='add', width=20, bg='brown', fg='white', command=lambda: raise_frame(add_component_behavior_frame)).place(x=250, y=200)

Label(main_frame, text="delete a component behavior test", width=30, font=("bold", 10)).place(x=30, y=250)
Button(main_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: raise_frame(delete_component_behavior_frame)).place(x=250, y=250)

Label(main_frame, text="update a component behavior test", width=30, font=("bold", 10)).place(x=30, y=300)
Button(main_frame, text='update', width=20, bg='brown', fg='white', command=lambda: raise_frame(update_component_behavior_frame)).place(x=250, y=300)

#add_component_behavior_frame

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
component_type = tkinter.StringVar() # there is the rule: variable name lowercase with _
type_entry = tkinter.OptionMenu(add_component_behavior_frame, component_type, "Button", "Label", "Check Box", "List", command=component_type_change)
type_entry.place(x=240, y=220)
component_type.set("select your component type")

#if button
action_type_label = Label(add_component_behavior_frame, text="What action type:", width=20, font=("bold", 10))
action_type = tkinter.StringVar()  # there is the rule: variable name lowercase with _
action_type_entry = tkinter.OptionMenu(add_component_behavior_frame, action_type, "click", "over")
action_type.set("select your action type")


#if label
label_content = Label(add_component_behavior_frame, text="content:", width=20, font=("bold", 10))
entry_content = Entry(add_component_behavior_frame)

expected_result_label = Label(add_component_behavior_frame, text="What expected result:", width=20, font=("bold", 10))
expected_result = tkinter.StringVar()  # there is the rule: variable name lowercase with _
expected_result_entry = tkinter.OptionMenu(add_component_behavior_frame, expected_result, "disabled")
expected_result.set("select your expected result")

Button(add_component_behavior_frame, text='OK', width=20, bg='brown', fg='white', command=lambda: add_component_behavior_ok()).place(x=170, y=400)

#delete_component_behavior_frame

Label(delete_component_behavior_frame, text="delete component behavior frame form", width=30, font=("bold", 16)).place(x=90, y=53)

Label(delete_component_behavior_frame, text="flow name:", width=20, font=("bold", 10)).place(x=80, y=130)
entry_delete_flow = Entry(delete_component_behavior_frame)
entry_delete_flow.place(x=240, y=130)

Label(delete_component_behavior_frame, text="test name:", width=20, font=("bold", 10)).place(x=80, y=180)
entry_delete_test = Entry(delete_component_behavior_frame)
entry_delete_test.place(x=240, y=180)

Button(delete_component_behavior_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: delete_component_behavior_ok()).place(x=170, y=400)

#update_component_behavior_frame

Label(update_component_behavior_frame, text="update component behavior frame form", width=30, font=("bold", 16)).place(x=90, y=53)

Label(update_component_behavior_frame, text="flow name:", width=20, font=("bold", 10)).place(x=80, y=130)
entry_delete_flow = Entry(update_component_behavior_frame)
entry_delete_flow.place(x=240, y=130)

Label(update_component_behavior_frame, text="test name:", width=20, font=("bold", 10)).place(x=80, y=170)
entry_delete_test = Entry(update_component_behavior_frame)
entry_delete_test.place(x=240, y=170)

continue_delete_button = Button(update_component_behavior_frame, text='continue', width=20, bg='brown', fg='white', command=lambda: continue_component_behavior_ok()).place(x=170, y=210)

component_type_delete_label = Label(update_component_behavior_frame, text="What component type:", width=20, font=("bold", 10))
component_type_delete = tkinter.StringVar() # there is the rule: variable name lowercase with _
type_entry_delete = tkinter.OptionMenu(update_component_behavior_frame, component_type_delete, "Button", "Label", "Check Box", "List", command=component_type_change)
component_type_delete.set("select your component type")

#if button
action_type_delete_label = Label(update_component_behavior_frame, text="What action type:", width=20, font=("bold", 10))
action_type_delete = tkinter.StringVar()  # there is the rule: variable name lowercase with _
action_type_delete_entry = tkinter.OptionMenu(update_component_behavior_frame, action_type_delete, "click", "over")
action_type_delete.set("select your action type")

#if label
label_delete_content = Label(update_component_behavior_frame, text="content:", width=20, font=("bold", 10))
entry_delete_content = Entry(update_component_behavior_frame)

expected_result_delete_label = Label(update_component_behavior_frame, text="What expected result:", width=20, font=("bold", 10))
expected_result_delete = tkinter.StringVar()  # there is the rule: variable name lowercase with _
expected_result_delete_entry = tkinter.OptionMenu(update_component_behavior_frame, expected_result_delete, "disabled")
expected_result_delete.set("select your expected result")

update_button = Button(update_component_behavior_frame, text='update', width=20, bg='brown', fg='white', command=lambda: update_component_behavior_ok())

main_win.mainloop()

