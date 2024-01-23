from data import Data
from util import settings
from config import helpStr, egs
from test_suite import TestSuite
from util import cli

if __name__ == '__main__':
    t, dir = settings(helpStr)
    t = cli(t, dir)
    
    if(t['help']):
        print("You can use the following options: ")
        print(helpStr)
    
    else:
        if(t['run_tc']=="all"):
            print("Running all tests!")
            ts = TestSuite()
            ts.run_tests()

        elif(t['run_tc']!="None"):
            print("Running test "+ t['run_tc'])
            ts = TestSuite()
            try:
                egs[t['run_tc']]()
                print(f"Test {t['run_tc']} passed.")
            except AssertionError as e:
                print(f"Test {t['run_tc']} failed: {e}")
        
        elif(t['run_tc']==""):
            pass

        new_data = Data(t['file'])
        print(new_data.stats())