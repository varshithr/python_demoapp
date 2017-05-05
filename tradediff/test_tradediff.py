# -*- coding: utf-8 -*-

import unittest
 
from tradediff import TradeDiff
 
 
#json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_sample.json"
json_url = "http://www.suntradingllc.com/interview_exercises/sun_trades_insight.json"
#csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_sample.csv"
csv_url = "http://www.suntradingllc.com/interview_exercises/counterparty_trades_insight.csv"


class MyTestCase(unittest.TestCase):
 
    def test_trade_diff(self):
 
        t = TradeDiff(json_url, csv_url)
        self.assertRaises(Exception, t.trade_diff, json_url, csv_url)
 
    def test_negative_discr(self):
 
        self.assertEqual(True, False)

if __name__ == '__main__':
 
    unittest.main()