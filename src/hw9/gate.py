#!/usr/bin/env python3
"""
gate: guess, assess, try, expand
(c) 2023, Tim Menzies, BSD-2, GROUP 4
Learn a little, guess a lot, try the strangest guess, repeat

USAGE:
  python3 gate.py [OPTIONS] 

OPTIONS:
  -c --cohen  small effect size               = .35
  -f --file   csv data file name              = '../data/diabetes.csv'
  -h --help   show help                       = False
  -k --k      low class frequency kludge      = 1
  -m --m      low attribute frequency kludge  = 2
  -s --seed   random number seed              = 31210
  -t --todo   start up action                 = 'help' """


from data import Data
from test_suite import TestSuite
import argparse
from util import Utility

def main():
    parser = argparse.ArgumentParser(description="Statistics on a CSV file: ")
    
    parser.add_argument('-c', '--cohen', help="small effect size               = .35")
    parser.add_argument("-f", "--file", help="csv data file name              = '../data/diabetes.csv'")
    parser.add_argument("-k", "--k", type=int, help="low class frequency kludge      = 1")
    parser.add_argument('-m', '--m', type=int,help="low attribute frequency kludge  = 2")
    parser.add_argument('-s', '--seed', help="random number seed              = 31210")
    parser.add_argument("-t", "--task", help="start up action                 = 'help' ")
    args = parser.parse_args()

    #loading data and sending it to Data class
    data = Data(args, src=args.file)

    tests = TestSuite(args)

    if args.task == "stats":
        res = data.stats()
        print (res)

    elif args.task == "sym":
        tests.run_sym_tests()

    elif args.task == "num":
        tests.run_num_tests()

    elif args.task == "bayes":
        tests.test_eg_bayes()
    elif args.task == "km":
        tests.test_km()
    elif args.task == "gate":
        tests.test_gate()
    elif args.task == "gate20":
        tests.test_gate20()

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