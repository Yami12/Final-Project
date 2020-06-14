'''
This file interacts with the user
The user is given options for various actions, he chooses the one he wants, fills in the required details and the program executes it
'''
from tkinter import *
from utils import xml_parsing
from utils import driver
from utils import string_list as sl

flag_component_feature = 0#component=0, feature=1
devices = driver.identify_connected_device()
# if not devices == False:
devices_names = [x[sl.DEVICE_UDID] for x in devices]


'''Accepts screen name making a move to it'''
def raise_frame(frame):
    frame.tkraise()

'''When: The user has finished entering the phone information and press the button on the "device_frame" screen
What: Connects to the appium driver and moves to the next screen'''
def device_frame_ok():
     if father_devices.get() != 'Not Selected' and child_devices.get() != 'Not Selected':
         father_device = next(i for i in devices if i[sl.DEVICE_UDID] == father_devices.get())
         child_device = next(i for i in devices if i[sl.DEVICE_UDID] == child_devices.get())
         driver.initialize(father_device[sl.DEVICE_VERSION], father_devices.get())
         driver.child_device = child_devices.get()
         driver.father_device = father_devices.get()
         print(driver.child_device)
         next_window()


def tester_device_frame_ok():
    if tester_devices.get() != 'Not Selected':
        tester_device = next(i for i in devices if i[sl.DEVICE_UDID] == tester_devices.get())
        driver.initialize(tester_device[sl.DEVICE_VERSION], tester_devices.get())
        driver.tester_device = tester_devices.get()
        print(driver.tester_device)
        next_window()

def open_features_window():
    raise_frame(feature_device_frame)
    global flag_component_feature
    flag_component_feature = 1
    # print("len",len(devices_names))
    # if  devices_names == []:
    #     feature_num_of_devices.place(x=180,y=240)


def open_component_window():
    raise_frame(component_device_frame)
    global flag_component_feature
    flag_component_feature = 0

def next_window():
    global flag_component_feature
    if flag_component_feature == 1:
        main_win.destroy()
        from GUI import user_interface_feature_test
        user_interface_feature_test.run_messaging_feature_test()
    else:   #flag_component_feature == 0
        main_win.destroy()
        from GUI import user_interface_component_test
        user_interface_component_test.run_component_test()


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


'''component_device_frame
A screen where the user enters various details of the mobile device to which he wants to add.
This allows you to connect to the device via the driver'''

Label(component_device_frame, text="tester device:", width=20, font=("bold", 10)).place(x=80, y=170)
tester_devices = StringVar()
tester_devices_entry = OptionMenu(component_device_frame, tester_devices, *devices_names)
tester_devices_entry.place(x=240, y=170)
tester_devices.set("Not Selected")

Button(component_device_frame, text='next', width=20, bg='brown', fg='white', command=lambda: tester_device_frame_ok()).place(x=170, y=450)


'''device_frame
A screen where the user choose his devices
This allows you to connect to the device via the driver'''
Label(feature_device_frame, text="select the devices", width=18, font=("bold", 25)).place(x=80, y=80)

Label(feature_device_frame, text="father device:", width=20, font=("bold", 10)).place(x=80, y=170)
father_devices = StringVar()
father_devices_entry = OptionMenu(feature_device_frame, father_devices, *devices_names)
father_devices_entry.place(x=240, y=170)
father_devices.set("Not Selected")

Label(feature_device_frame, text="child device:", width=20, font=("bold", 10)).place(x=80, y=300)
child_devices = StringVar()
child_devices_entry = OptionMenu(feature_device_frame, child_devices, *devices_names)
child_devices_entry.place(x=240, y=300)
child_devices.set("Not Selected")

Button(feature_device_frame, text='next', width=20, bg='brown', fg='white', command=lambda: device_frame_ok()).place(x=170, y=450)

'''first_frame
A screen where the user can choose what type of testing he wants to use'''
Label(first_frame, text="Testing Menu", width=29, font=("bold", 20)).place(x=20, y=60)
Button(first_frame, text='to component behavior tests', width=40, bg='brown', fg='white', command=open_component_window).place(x=110, y=150)
Button(first_frame, text='to features tests', width=40, bg='brown', fg='white', command=open_features_window).place(x=110, y=230)
Button(first_frame, text='exit', width=20, bg='brown', fg='white', command=main_win.destroy).place(x=180, y=350)


#Starts the program by displaying the first screen
main_win.mainloop()