# Final-Project

Automation Enviroment for testing Keepers application


code's files:


components:

*components_operations.py: This file performs actions on requested components

*components_tests.py: This file handles the components tests


features:

*device_locked.py: This file handles the child device locked test

*messaging.py: The file handles messaging and removal from group tests

*web_filtering.py: This file handles the web filtering test blocked requested websites in the child device


utils:

*drive.py : contains the appium's driver implementation

*xml_parsing.py : contains the implementation of the functions that hundle the xml files

*html_page.py : create html file with the test result and send all the files by mail

*read_messaginf_logs.py : This file create an asynchronous File reader class this class is used for reading logs

*string_list.py : This file contains consts for all the other files

*keepers automation: contains the exe files of our project - Keepers Automation.exe

*utils_funcs.py : this file contains utils functions


xml_files:

*applications.xml: contains all the apps details

*components_behavior_tests.xml: contains all the componenets tests

*features_tests.xml: contains all the features tests


keepers_automation.py: the main file that run all the tests
