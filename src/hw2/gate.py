from data import Data
from test_suite import TestSuite
import argparse

def main():
    parser = argparse.ArgumentParser(description="Statistics on a CSV file: ")
    
    parser.add_argument('-c', '--cohen', help="small effect size               = .35")
    parser.add_argument("-f", "--file", required=True, help="path to src file")
    parser.add_argument("-t", "--task", choices=["num", "sym", "stats", "all"], 
                        required=True, help="Task to perform")
    args = parser.parse_args()

    #loading data and sending it to Data class
    data = Data(args, src=args.file)

    tests = TestSuite()

    if args.task == "stats":
        res = data.stats()
        print (res)

    elif args.task == "sym":
        tests.run_sym_tests()

    elif args.task == "num":
        tests.run_num_tests()

    elif args.task == "all":
        tests.run_all_tests()
    
    else: 
        print (f"Unsupported Task: {args.task}")

if __name__ == "__main__":
    main()



#OLD CODE
# if __name__ == '__main__':
#     t, dir = settings(helpStr)
#     t = cli(t, dir)
    
#     if(t['help']):
#         print("You can use the following options: ")
#         print(helpStr)
    
#     else:
#         if(t['run_tc']=="all"):
#             print("Running all tests!")
#             ts = TestSuite()
#             ts.run_tests()

#         elif(t['run_tc']!="None"):
#             print("Running test "+ t['run_tc'])
#             ts = TestSuite()
#             try:
#                 egs[t['run_tc']]()
#                 print(f"Test {t['run_tc']} passed.")
#             except AssertionError as e:
#                 print(f"Test {t['run_tc']} failed: {e}")
        
#         elif(t['run_tc']==""):
#             pass

#         new_data = Data(t['file'])
#         print(new_data.stats())