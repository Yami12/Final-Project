from tkinter import *
from threading import Thread
from utils import xml_parsing
from utils import string_list as sl

tests = xml_parsing.feature_xml_to_dictionary('messaging_feature_tests.xml')
tests_names = [x[sl.TEST_NAME] for x in tests]
social_networks = xml_parsing.tests_xml_to_dictionary("social_networks.xml")
social_networks_name = [x[sl.S_NETWORK_NAME] for x in social_networks]

def send_message():
    if feature_tests.get() != 'Not Selected':
        from utils import main_tester
        main_tester.MainTester().run_messaging_feature_test(feature_tests.get(), social_network.get())


#Starts the program by displaying the first screen
def run_messaging_feature_test():
    main_window.mainloop()

run_test_thread = Thread(target = send_message)

#Visual display of screens
main_window = Tk()
main_window.geometry('500x500')
main_window.title("Registration Form")

#define frames, each represents a screen
main_feature_test_frame = Frame(main_window)
main_feature_test_frame.place(x=0, y=0, width=500, height=500)

'main_feature_test_frame'
Label(main_feature_test_frame, text="Choose test", width=20, font=("bold", 20)).place(x=80, y=30)

feature_tests = StringVar()
feature_tests_entry = OptionMenu(main_feature_test_frame, feature_tests, *tests_names)
feature_tests_entry.place(x=140, y=140)
feature_tests.set("Not Selected")

Label(main_feature_test_frame, text="social network:", width=20, font=("bold", 10)).place(x=80, y=350)
social_network = StringVar()
social_network_entry = OptionMenu(main_feature_test_frame, social_network, *social_networks_name)
social_network_entry.place(x=240, y=350)
social_network.set("Not Selected")

Button(main_feature_test_frame, text='start test', width=20, bg='brown', fg='white', command=lambda: run_test_thread.start()).place(x=170, y=400)
