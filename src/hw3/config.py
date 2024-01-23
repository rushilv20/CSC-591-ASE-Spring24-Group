from test_suite import TestSuite

helpStr = __doc__

the = {}
test_suite = TestSuite()

egs = {
    "coerce":test_suite.test_coerce,
    "cells":test_suite.test_cells,
    "settings":test_suite.test_settings,
    "round":test_suite.test_rounded,
    "add_num":test_suite.test_add_num,
    "mid_num":test_suite.test_mid_num,
    "div_num":test_suite.test_div_num,
    "add_sym":test_suite.test_add_sym,
    "mid_sym":test_suite.test_mid_sym,
    "div_sym":test_suite.test_div_sym,
    "small_sym":test_suite.test_small_sym
}