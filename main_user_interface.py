'''
This file interacts with the user
The user is given options for various actions, he chooses the one he wants, fills in the required details and the program executes it
'''

from tkinter import *
import driver

'''Accepts screen name making a move to it'''
def raise_frame(frame):
    frame.tkraise()

'''When: The user has finished entering the phone information and press the button on the "device_frame" screen
What: Connects to the appium driver and moves to the next screen'''
def device_frame_ok():
     driver.initialize(entry_owner_name.get(), entry_platform_name.get(), entry_platform_version.get(), entry_device_name.get(), entry_apk_file.get())

     if entry_owner_name.get() == 'father':
         entry_owner_name.configure(state="normal")
         entry_owner_name.delete(0, END)
         entry_owner_name.insert(0, 'child')
         entry_owner_name.configure(state="disabled")
         raise_frame(device_frame)
     else:
         next_window()

def open_features_window():
    raise_frame(device_frame)

def open_component_window():
    entry_owner_name.configure(state="normal")
    entry_owner_name.delete(0, END)
    entry_owner_name.insert(0, 'tester')
    entry_owner_name.configure(state="disabled")
    raise_frame(device_frame)

def next_window():
    if entry_owner_name.get() == 'child':
        main_win.destroy()
        from user_interface_feature_test import run_messaging_feature_test
        run_messaging_feature_test()
    else:   #entry_owner_name.get() == 'tester':
        main_win.destroy()
        from user_interface_component_test import run_component_test
        run_component_test()


#Visual display of screens
main_win = Tk()
main_win.geometry('500x500')
main_win.title("Registration Form")

device_frame = Frame(main_win)
device_frame.place(x=0, y=0, width=500, height=500)

first_frame = Frame(main_win)
first_frame.place(x=0, y=0, width=500, height=500)


'''device_frame
A screen where the user enters various details of the mobile device to which he wants to connect.
This allows you to connect to the device via the driver'''
Label(device_frame, text="Fill in the device details", width=20, font=("bold", 20)).place(x=80, y=40)

Label(device_frame, text="owner name:", width=20, font=("bold", 10)).place(x=80, y=110)
entry_owner_name = Entry(device_frame)
entry_owner_name.place(x=240, y=110)
entry_owner_name.insert(0, 'father')
entry_owner_name.configure(state="disabled")

Label(device_frame, text="platform name:", width=20, font=("bold", 10)).place(x=80, y=150)
entry_platform_name = Entry(device_frame)
entry_platform_name.place(x=240, y=150)
entry_platform_name.insert(0, 'Android')

Label(device_frame, text="platform version:", width=20, font=("bold", 10)).place(x=80, y=190)
entry_platform_version = Entry(device_frame)
entry_platform_version.place(x=240, y=190)
entry_platform_version.insert(0, '10.0')#'8.0.0')

Label(device_frame, text="device name:", width=20, font=("bold", 10)).place(x=80, y=230)
entry_device_name = Entry(device_frame)
entry_device_name.place(x=240, y=230)
entry_device_name.insert(0, 'Child_Device')#'My HUAWEI')


Label(device_frame, text="apk file:", width=20, font=("bold", 10)).place(x=80, y=270)
entry_apk_file = Entry(device_frame)
entry_apk_file.place(x=240, y=270)
entry_apk_file.insert(0, '')#'Keepers Child Safety.apk')

Button(device_frame, text='OK', width=20, bg='brown', fg='white', command=lambda: device_frame_ok()).place(x=170, y=360)

'''first_frame
A screen where the user can choose what type of testing he wants to use'''
Label(first_frame, text="Testing Menu", width=29, font=("bold", 20)).place(x=20, y=60)
Button(first_frame, text='to component behavior tests', width=40, bg='brown', fg='white', command=open_component_window).place(x=110, y=150)
Button(first_frame, text='to features tests', width=40, bg='brown', fg='white', command=open_features_window).place(x=110, y=230)
Button(first_frame, text='exit', width=20, bg='brown', fg='white', command=main_win.destroy).place(x=180, y=350)

#Starts the program by displaying the first screen
main_win.mainloop()