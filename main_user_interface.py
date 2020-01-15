from tkinter import *


def raise_frame(frame):
    frame.tkraise()


main_win = Tk()
main_win.geometry('500x500')
main_win.title("Registration Form")

#define frames

main_frame = Frame(main_win)
main_frame.place(x=0, y=0, width=500, height=500)

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
label_00 = Label(main_frame, text="Choose the desired action", width=20, font=("bold", 20))
label_00.place(x=90, y=53)

label_11 = Label(main_frame, text="run test", width=30, font=("bold", 10))
label_11.place(x=30, y=150)
Button(main_frame, text='run', width=20, bg='brown', fg='white', command=lambda: raise_frame(run_test_frame)).place(x=250, y=150)

label_22 = Label(main_frame, text="add a component behavior test", width=30, font=("bold", 10))
label_22.place(x=30, y=200)
Button(main_frame, text='add', width=20, bg='brown', fg='white', command=lambda: raise_frame(add_component_behavior_frame)).place(x=250, y=200)

label_33 = Label(main_frame, text="delete a component behavior test", width=30, font=("bold", 10))
label_33.place(x=30, y=250)
Button(main_frame, text='delete', width=20, bg='brown', fg='white', command=lambda: raise_frame(delete_component_behavior_frame)).place(x=250, y=250)

label_44 = Label(main_frame, text="update a component behavior test", width=30, font=("bold", 10))
label_44.place(x=30, y=300)
Button(main_frame, text='update', width=20, bg='brown', fg='white', command=lambda: raise_frame(update_component_behavior_frame)).place(x=250, y=300)

#add_component_behavior_frame

label_0 = Label(add_component_behavior_frame, text="add component behavior frame form", width=20, font=("bold", 20))
label_0.place(x=90, y=53)

label_1 = Label(add_component_behavior_frame, text="resource id:", width=20, font=("bold", 10))
label_1.place(x=80, y=130)

entry_1 = Entry(add_component_behavior_frame)
entry_1.place(x=240, y=130)

label_2 = Label(add_component_behavior_frame, text="app activity:", width=20, font=("bold", 10))
label_2.place(x=80, y=180)

entry_2 = Entry(add_component_behavior_frame)
entry_2.place(x=240, y=180)

label_4 = Label(add_component_behavior_frame, text="What component type:", width=20, font=("bold", 10))
label_4.place(x=70, y=280)

list1 = ['Button', 'Label', 'Check Box', 'List'];
c = StringVar()
droplist = OptionMenu(add_component_behavior_frame, c, *list1)
droplist.config(width=27)
c.set('select your component type')
droplist.place(x=240, y=280)

Button(add_component_behavior_frame, text='OK', width=20, bg='brown', fg='white').place(x=170, y=400)


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