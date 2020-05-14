'''
This file interacts with the user
The user is given options for various actions, he chooses the one he wants, fills in the required details and the program executes it
'''

from tkinter import *
import xml_parsing
import driver

flag_component_feature = 0#component=0, feature=1

'''Accepts screen name making a move to it'''
def raise_frame(frame):
    frame.tkraise()

'''When: The user has finished entering the phone information and press the button on the "device_frame" screen
What: Connects to the appium driver and moves to the next screen'''
def device_frame_ok():
     driver.initialize("father", entry_platform_name.get(), entry_platform_version.get(), entry_device_name.get())
     driver.initialize("child", entry_platform_name.get(), entry_platform_version.get(), entry_device_name.get())
     next_window()

def add_device():
    raise_frame(add_device_frame)

def add_device_button():
    #add device
    new_device = {}
    new_device['device_name'] = entry_device_name.get()
    new_device['platform_name'] = entry_platform_name.get()
    new_device['platform_version'] = entry_platform_version.get()
    xml_parsing.add_new_device(new_device, 'devices.xml')

    if flag_component_feature == 1:
        raise_frame(feature_device_frame)
    else:  # flag_component_feature == 0
        raise_frame(component_device_frame)

def tester_device_frame_ok():
    return

def open_features_window():
    raise_frame(feature_device_frame)
    global flag_component_feature
    flag_component_feature = 1

def open_component_window():
    raise_frame(component_device_frame)
    global flag_component_feature
    flag_component_feature = 0

def next_window():
    global flag_component_feature
    if flag_component_feature == 1:
        main_win.destroy()
        from user_interface_feature_test import run_messaging_feature_test
        run_messaging_feature_test()
    else:   #flag_component_feature == 0
        main_win.destroy()
        from user_interface_component_test import run_component_test
        run_component_test()


#Visual display of screens
main_win = Tk()
main_win.geometry('500x500')
main_win.title("Registration Form")

add_device_frame = Frame(main_win)
add_device_frame.place(x=0, y=0, width=500, height=500)

feature_device_frame = Frame(main_win)
feature_device_frame.place(x=0, y=0, width=500, height=500)

component_device_frame = Frame(main_win)
component_device_frame.place(x=0, y=0, width=500, height=500)

first_frame = Frame(main_win)
first_frame.place(x=0, y=0, width=500, height=500)


'''feature_device_frame
A screen where the user enters various details of the mobile device to which he wants to add.
This allows you to connect to the device via the driver'''
Label(add_device_frame, text="Fill in the device details", width=20, font=("bold", 20)).place(x=80, y=40)

Label(add_device_frame, text="platform name:", width=20, font=("bold", 10)).place(x=80, y=150)
entry_platform_name = Entry(add_device_frame)
entry_platform_name.place(x=240, y=150)
entry_platform_name.insert(0, 'Android')

Label(add_device_frame, text="platform version:", width=20, font=("bold", 10)).place(x=80, y=190)
entry_platform_version = Entry(add_device_frame)
entry_platform_version.place(x=240, y=190)
entry_platform_version.insert(0, '8.0')#'10.0')

Label(add_device_frame, text="device name:", width=20, font=("bold", 10)).place(x=80, y=230)
entry_device_name = Entry(add_device_frame)
entry_device_name.place(x=240, y=230)
entry_device_name.insert(0, 'My HUAWEI')#)'Child_Device'

Button(add_device_frame, text='add', width=20, bg='brown', fg='white', command=lambda: add_device_button()).place(x=170, y=300)

# devices_names = xml_parsing.devices_xml_to_dictionary('devices.xml')
devices_names = [1, 2, 3]
print(devices_names)

'''component_device_frame
A screen where the user enters various details of the mobile device to which he wants to add.
This allows you to connect to the device via the driver'''

Label(component_device_frame, text="tester device:", width=20, font=("bold", 10)).place(x=80, y=170)
tester_devices = StringVar()
tester_devices_entry = OptionMenu(component_device_frame, tester_devices, *devices_names)
tester_devices_entry.place(x=240, y=170)
tester_devices.set("select tester device")

Button(component_device_frame, text='add device', width=20, bg='brown', fg='white', command=lambda: add_device()).place(x=170, y=400)

Button(component_device_frame, text='next', width=20, bg='brown', fg='white', command=lambda: tester_device_frame_ok()).place(x=170, y=450)


'''device_frame
A screen where the user choose his devices
This allows you to connect to the device via the driver'''
Label(feature_device_frame, text="select the devices", width=18, font=("bold", 25)).place(x=80, y=80)

Label(feature_device_frame, text="father device:", width=20, font=("bold", 10)).place(x=80, y=170)
father_devices = StringVar()
father_devices_entry = OptionMenu(feature_device_frame, father_devices, *devices_names)
father_devices_entry.place(x=240, y=170)
father_devices.set("select father device")

Label(feature_device_frame, text="child device:", width=20, font=("bold", 10)).place(x=80, y=300)
child_devices = StringVar()
child_devices_entry = OptionMenu(feature_device_frame, child_devices, *devices_names)
child_devices_entry.place(x=240, y=300)
child_devices.set("select child device")

Button(feature_device_frame, text='add device', width=20, bg='brown', fg='white', command=lambda: add_device()).place(x=170, y=400)

Button(feature_device_frame, text='next', width=20, bg='brown', fg='white', command=lambda: device_frame_ok()).place(x=170, y=450)




'''first_frame
A screen where the user can choose what type of testing he wants to use'''
Label(first_frame, text="Testing Menu", width=29, font=("bold", 20)).place(x=20, y=60)
Button(first_frame, text='to component behavior tests', width=40, bg='brown', fg='white', command=open_component_window).place(x=110, y=150)
Button(first_frame, text='to features tests', width=40, bg='brown', fg='white', command=open_features_window).place(x=110, y=230)
Button(first_frame, text='exit', width=20, bg='brown', fg='white', command=main_win.destroy).place(x=180, y=350)

#Starts the program by displaying the first screen
main_win.mainloop()