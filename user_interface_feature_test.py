from tkinter import *
from threading import Thread
import xml_parsing

tests = xml_parsing.feature_xml_to_dictionary('messaging_feature_tests.xml')
tests_names = [x['name'] for x in tests]

def send_message():
    from main_tester import MainTester
    MainTester.run_messaging_feature_test(feature_tests.get())


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


Button(main_feature_test_frame, text='start test', width=20, bg='brown', fg='white', command=lambda: run_test_thread.start()).place(x=170, y=400)

