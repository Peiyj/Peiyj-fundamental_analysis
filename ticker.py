import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
class ticker(object):
    def __init__(self, tickerName):
        ##
        self.api = 'https://financialmodelingprep.com/api/v3/'
        self.tickerName = tickerName 
        self.tenYearCashFlow = []
        self.cashflowForecast = [0.0] * 11
        self.growthRate = []
        self.debt = 0
        self.investment = 0 
        self.shares = 0
        self.intrinsic_value = 0
        self.now = datetime.datetime.now()
        ##
        self.fetchCashFlow()
        self.fetchDebt()
        self.fetchInvestment()
        self.fetchShares()
        self.fetchGrowthRate()
        self.calculateIV()
        
    def calculateIV(self):
        ## 
        short_term_growth = self.growthRate[0]
        long_term_growth = (sum(self.growthRate) + self.growthRate[0] * 5) / (len(self.growthRate) + 5)
        print("{}'s growth rate".format(self.tickerName))
        discounted_rate = 0.05
        self.cashflowForecast[0] = self.tenYearCashFlow[0][1]
        investment = self.investment
        debt = self.debt
        shares = self.shares
        ##
        for i in range(1, 6): # year 1 - 5
            self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + short_term_growth) * (1 - discounted_rate)
        for i in range(6, 11): # year 6 - 10
            self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + long_term_growth) * (1 - discounted_rate)
        self.intrinsic_value = (sum(self.cashflowForecast) - self.cashflowForecast[0]  + investment - debt)/shares
        print('{} final intrinsic value is {}'.format(self.tickerName, int(self.intrinsic_value)))

    def fetchCashFlow(self):
        cash_flow_url = self.api + 'financials/cash-flow-statement/' + self.tickerName
        response = requests.get(cash_flow_url)
        cashflow_json = response.json()
        for key, metrics in cashflow_json.items():
            if key == 'financials':
                break
        for metric in metrics:
            pair = []
            for key, val in metric.items():
                if key == 'date':
                    pair.append(val[:7])
                if key == 'Operating Cash Flow':
                    pair.append(float(val))
            self.tenYearCashFlow.append(pair)

    def fetchDebt(self):
        debt_url = self.api + 'financials/balance-sheet-statement/' + self.tickerName
        response = requests.get(debt_url)
        assert(response.status_code == 200)
        debt_json = response.json()
        for key, metrics in debt_json.items():
            if key == 'financials':
                break
        assert(key == 'financials')
        for metric in metrics:
            for key, val in metric.items():
                if key == 'Long-term debt':
                    self.debt = float(metric[key])
                    return

    def fetchInvestment(self):
        investment_url = self.api + 'financials/balance-sheet-statement/' + self.tickerName
        response = requests.get(investment_url)
        assert(response.status_code == 200)
        investment_json = response.json()
        for key, metrics in investment_json.items():
            if key == 'financials':
                break
        assert(key == 'financials')
        for metric in metrics:
            for key, val in metric.items():
                if key == 'Cash and short-term investments':
                    self.investment = float(metric[key])
                    return

    def fetchShares(self):
        share_url = self.api + 'enterprise-value/' + self.tickerName
        response = requests.get(share_url)
        shares_json = response.json()
        for key, metrics in shares_json.items():
            if key == 'enterpriseValues':
                break
        assert(key == 'enterpriseValues')
        for metric in metrics:
            for key, val in metric.items():
                if key == 'Number of Shares':
                    self.shares = float(metric[key])
                    return

    def fetchGrowthRate(self):
        growth_url = self.api + 'financial-statement-growth/' + self.tickerName
        response = requests.get(growth_url)
        growth_json = response.json()
        for key, metrics in growth_json.items():
            if key == 'growth':
                break
        assert(key == 'growth')
        for metric in metrics:
            for key, val in metric.items():
                if key == 'Operating Cash Flow growth':
                    self.growthRate.append(float(val))
    
    def analyzeOperatingCashflow(self):
        cashflowGraph = self.tenYearCashFlow[::-1]
        df = pd.DataFrame(cashflowGraph, columns = ['Date', 'Net cash flow'])
        df.plot(x = 'Date', y = 'Net cash flow', kind='bar', title='Net cash provided by operating activities')
        plt.show()
        print(df)

    def analyzeCashflowForecast(self):
        df = pd.DataFrame(self.cashflowForecast, columns = ['cashflow forecast'])
        df.insert(1, 'Date', [self.now.year + i for i in range(-1, 10)], True)
        print(df)
        df.plot(x = 'Date', y = 'cashflow forecast', kind='bar', title='{} cash flow Forecast'.format(self.tickerName))
        plt.show()
# create new object
# myTicker = ticker('AMZN')
# myTicker.analyzeOperatingCashflow()
myTicker = ticker('msft')
myTicker.analyzeCashflowForecast()
# myTicker = ticker('MSFT')
# myTicker = ticker('AAPL')
# myTicker = ticker('BABA')
# myTicker = ticker('FB')
# myTicker = ticker('MCD')
# myTicker = ticker('UNH')
# myTicker = ticker('V')
# myTicker = ticker('LMT')
# myTicker = ticker('NOC')