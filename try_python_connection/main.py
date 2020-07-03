import sys
import os
conf_path = os.getcwd()
sys.path.append(conf_path)

import main_tester

if __name__ == '__main__':
    print(conf_path)
    if sys.argv[1] == 0:
       main_tester.MainTester.run_messaging_feature_test()
    if sys.argv[1] == 1:
       main_tester.MainTester.run_web_filtering_test()


    # print(str(sys.argv[1])+str(sys.argv[2])+str(sys.argv[3]))