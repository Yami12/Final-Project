from tkinter import *
from threading import Thread

#Starts the program by displaying the first screen
def run_messaging_feature_test():
    main_window.mainloop()

def send_message():
    from main_tester import MainTester
    MainTester.run_messaging_feature_test("Recive an offensive message via Whatsapp")
    return

run_test_thread = Thread(target = send_message)

def choose_sender_name(event):
    selected = sender_name.get()
    entry_receiver_name.configure(state="normal")
    entry_receiver_name.delete(0, END)
    if selected == 'tester':
        entry_receiver_name.insert(0, 'child')
    else:
        entry_receiver_name.insert(0, 'tester')
    entry_receiver_name.configure(state="disabled")


#Visual display of screens
main_window = Tk()
main_window.geometry('500x500')
main_window.title("Registration Form")

#define frames, each represents a screen
main_feature_test_frame = Frame(main_window)
main_feature_test_frame.place(x=0, y=0, width=500, height=500)

'main_feature_test_frame'
Label(main_feature_test_frame, text="Fill in the details", width=20, font=("bold", 20)).place(x=80, y=30)

Label(main_feature_test_frame, text="social network name:", width=20, font=("bold", 10)).place(x=80, y=110)
social_network_name = StringVar()  # there is the rule: variable name lowercase with _
social_network_name_entry = OptionMenu(main_feature_test_frame, social_network_name, "Whatsapp")
social_network_name_entry.place(x=240, y=110)
social_network_name.set("select social network")

Label(main_feature_test_frame, text="sender:", width=20, font=("bold", 10)).place(x=80, y=170)
sender_name = StringVar()  # there is the rule: variable name lowercase with _
sender_name_entry = OptionMenu(main_feature_test_frame, sender_name, "child", "tester", command=choose_sender_name)
sender_name_entry.place(x=240, y=170)
sender_name.set("select sender")

Label(main_feature_test_frame, text="receiver:", width=20, font=("bold", 10)).place(x=80, y=230)
entry_receiver_name = Entry(main_feature_test_frame)
entry_receiver_name.place(x=240, y=230)

Label(main_feature_test_frame, text="content of the message:", width=20, font=("bold", 10)).place(x=80, y=290)
entry_content_message = Entry(main_feature_test_frame)
entry_content_message.place(x=240, y=290)

Button(main_feature_test_frame, text='send message', width=20, bg='brown', fg='white', command=lambda: run_test_thread.start()).place(x=170, y=400)

