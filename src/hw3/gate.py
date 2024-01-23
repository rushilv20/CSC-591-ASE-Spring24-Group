from utils import settings, cli
from config import help_str, egs
from test_suite import TestSuite
from learner import print_stats, bayes




if __name__ == '__main__':
    the, opt_dir = settings(help_str)
    the = cli(the, opt_dir)

    if(the['help'] == 'True'):
        print("You can use the following help: ")
        print(help_str)
        exit(1)
    
    if(the['run_tc']=="all"):
        print("running all tests!")
        ts = TestSuite()
        ts.run_tests()
    elif(the['run_tc']==""):
        pass
    elif(the['run_tc']!="None"):
        print("running test "+ the['run_tc'])
        ts = TestSuite()
        try:
            egs[the['run_tc']]()
            print(f"Test {the['run_tc']} passed.")
        except AssertionError as e:
            print(f"Test {the['run_tc']} failed: {e}")
    
    data_new = print_stats(the['file'], the)
    acc = bayes(data_new, the)
    print(f"Accuracy for {the['file'].split('/')[3]}: {acc}"),