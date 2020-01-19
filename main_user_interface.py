from tkinter import *
import tkinter
import xml_parsing


def raise_frame(frame):
    frame.tkraise()


def add_component_behavior_ok():
    new_test = {}
    new_test['name'] = entry_add_test.get()
    new_test['resourceId'] = entry_add_resource.get()
    new_test['appActivity'] = entry_add_activity.get()
    new_test['type'] = component_type.get()

    # if type == 'Button':
    #
    # elif type == "Label"
    # new_test['expectedResult'] =
    # xml_parsing.add_new_test_to_flow(entry_add_flow.get(), new_test)


def delete_component_behavior_ok():
    return


def update_component_behavior_ok():
    return


def component_type_change(event):
    selected = component_type.get()
    if selected == "Button":
        Label(add_component_behavior_frame, text="What action type:", width=20, font=("bold", 10)).place(x=70, y=260)
        action_type = tkinter.StringVar()  # there is the rule: variable name lowercase with _
        action_type_entry = tkinter.OptionMenu(add_component_behavior_frame, action_type, "click", "over")
        action_type_entry.place(x=240, y=260)
        action_type.set("select your action type")

        Label(add_component_behavior_frame, text="What expected result:", width=20, font=("bold", 10)).place(x=70, y=290)
        expected_result = tkinter.StringVar()  # there is the rule: variable name lowercase with _
        expected_result_entry = tkinter.OptionMenu(add_component_behavior_frame, expected_result, "disabled")
        expected_result_entry.place(x=240, y=290)
        expected_result.set("select your expected result")
    elif selected == "Label":
        Label(add_component_behavior_frame, text="content:", width=20, font=("bold", 10)).place(x=70, y=260)
        entry_content = Entry(add_component_behavior_frame)
        entry_content.place(x=240, y=260)

        Label(add_component_behavior_frame, text="What expected result:", width=20, font=("bold", 10)).place(x=70, y=290)
        expected_result = tkinter.StringVar()  # there is the rule: variable name lowercase with _
        expected_result_entry = tkinter.OptionMenu(add_component_behavior_frame, expected_result, "disabled")
        expected_result_entry.place(x=240, y=290)
        expected_result.set("select your expected result")
    # elif selected == "Check Box":
    #     print()
    # elif selected == "List":
    #     print()


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

Button(add_component_behavior_frame, text='OK', width=20, bg='brown', fg='white', command=lambda: add_component_behavior_ok()).place(x=170, y=400)

#delete_component_behavior_frame

Label(delete_component_behavior_frame, text="delete component behavior frame form", width=30, font=("bold", 16)).place(x=90, y=53)

Label(delete_component_behavior_frame, text="flow name:", width=20, font=("bold", 10)).place(x=80, y=130)
entry_1 = Entry(delete_component_behavior_frame)
entry_1.place(x=240, y=130)

Label(delete_component_behavior_frame, text="test name:", width=20, font=("bold", 10)).place(x=80, y=180)
entry_2 = Entry(delete_component_behavior_frame)
entry_2.place(x=240, y=180)

Button(delete_component_behavior_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: delete_component_behavior_ok()).place(x=170, y=400)

#update_component_behavior_frame

Label(update_component_behavior_frame, text="update component behavior frame form", width=30, font=("bold", 16)).place(x=90, y=53)

Button(update_component_behavior_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: update_component_behavior_ok()).place(x=170, y=400)


# label_3 = Label(add_component_behavior_frame, text="Gender", width=20, font=("bold", 10))
# label_3.place(x=70, y=230)
# var = IntVar()
# Radiobutton(add_component_behavior_frame, text="Male", padx=5, variable=var, value=1).place(x=235, y=230)
# Radiobutton(add_component_behavior_frame, text="Female", padx=20, variable=var, value=2).place(x=290, y=230)

# label_4 = Label(add_component_behavior_frame, text="Programming", width=20, font=("bold", 10))
# label_4.place(x=85, y=330)
# var1 = IntVar()
# Checkbutton(add_component_behavior_frame, text="java", variable=var1).place(x=235, y=330)
# var2 = IntVar()
# Checkbutton(add_component_behavior_frame, text="python", variable=var2).place(x=290, y=330)

# Button(add_component_behavior_frame, text='Submit', width=20, bg='brown', fg='white', command=lambda: raise_frame(second_frame)).place(
#     x=180, y=380)
#
# label_8 = Label(second_frame, text="Welcome to page 2", width=20, font=("bold", 10))
# label_8.place(x=70, y=230)
#
# Button(second_frame, text="Switch back to page 1", width=20, bg='brown', fg='white',
#        command=lambda: raise_frame(add_component_behavior_frame)).place(x=180, y=380)

main_win.mainloop()