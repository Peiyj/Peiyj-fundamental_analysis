import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen

class ticker(object):
    def __init__(self, tickerName):
        ##
        self.driver_path = '/Users/Patrick/.wdm/drivers/chromedriver/80.0.3987.106/mac64/chromedriver'
        self.options = Options()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.options)
        ##
        self.api = 'https://financialmodelingprep.com/api/v3/'
        self.tickerName = tickerName 
        self.tenYearCashFlow = []
        self.freeCashFlow = 0
        self.cashflowForecast = [0.0] * 21
        self.growthRate = []
        self.marketPrice = 0
        self.debt = 0
        self.investment = 0 
        self.shares = 0
        self.intrinsic_value = 0
        self.now = datetime.datetime.now()
        self.next_5_year_growth = 0
        self.past_5_year_growth = 0
        self.isConsistentGrowing = False
        ##
        self.fetchCashFlow()
        self.fetchDebt()
        self.fetchInvestment()
        self.fetchShares()
        self.fetchFreeCashFlow()
        self.fetchLongTermGrowthRate()
        self.fetchDiscountedRate()
        self.fetchMarketPrice()
        self.fetchGrowthRate()
        if self.isConsistentGrowing == True:
            self.evaluate()

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
                if key == 'Free Cash Flow':
                    pair.append(float(val))
            self.tenYearCashFlow.append(pair)

    def fetchFreeCashFlow(self):
        cash_flow_url = self.api + 'financials/cash-flow-statement/' + self.tickerName
        response = requests.get(cash_flow_url)
        cashflow_json = response.json()
        for key, metrics in cashflow_json.items():
            if key == 'financials':
                break
        for metric in metrics:
            for key, val in metric.items():
                if key == 'Free Cash Flow':
                    self.freeCashFlow = float(val)
                    return

    def fetchMarketPrice(self):
        cash_flow_url = 'https://financialmodelingprep.com/api/v3/company/profile/' + self.tickerName
        response = requests.get(cash_flow_url)
        cashflow_json = response.json()
        for key, metrics in cashflow_json.items():
            if key == 'profile':
                break
        for key, val in metrics.items():
            if key == 'price':
                self.marketPrice = float(val)
                return

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

    def fetchLongTermGrowthRate(self):
        ##
        self.driver.get('https://finance.yahoo.com/quote/{}/analysis?'.format(self.tickerName))
        next_5_year = self.driver.find_element_by_xpath("//*[@id='Col1-0-AnalystLeafPage-Proxy']/section/table[6]/tbody/tr[5]/td[2]")
        self.next_5_year_growth = float(next_5_year.text.strip('%'))/100

        past_5_year = self.driver.find_element_by_xpath("//*[@id='Col1-0-AnalystLeafPage-Proxy']/section/table[6]/tbody/tr[6]/td[2]")
        if past_5_year.text == 'N/A':
            self.past_5_year_growth = self.next_5_year_growth
        else:
            self.past_5_year_growth = float(past_5_year.text.strip('%'))/100

    def fetchDiscountedRate(self):
        self.driver.get('https://finance.yahoo.com/quote/' + self.tickerName)
        element = self.driver.find_element_by_xpath("//*[@id='quote-summary']/div[2]/table/tbody/tr[2]/td[2]/span")
        beta = element.text
        if beta == 'N/A':
            self.discountedRate = 0.065
            return
        beta = float(beta)
        if beta < 0.8:
            self.discountedRate = 0.05
        elif 0.8 <= beta < 1.0:
            self.discountedRate = 0.055
        elif 1.0 <= beta < 1.1:
            self.discountedRate = 0.06
        elif 1.1 <= beta < 1.2:
            self.discountedRate = 0.065
        elif 1.2 <= beta < 1.3:
            self.discountedRate = 0.07
        elif 1.3 <= beta < 1.4:
            self.discountedRate = 0.075
        elif 1.4 <= beta < 1.5:
            self.discountedRate = 0.08
        elif 1.5 <= beta < 1.6:
            self.discountedRate = 0.085
        else:
            self.discountedRate = 0.09
    
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
        ten_year_negative_growth_count = 0
        five_year_negative_growth_count = 0
        count = 1
        for metric in metrics:
            if count > 10:
                break
            for key, val in metric.items():
                if key == 'Free Cash Flow growth':
                    if float(val) < -0.05:
                        ten_year_negative_growth_count += 1
                        if count <= 5:
                            five_year_negative_growth_count += 1
                    self.growthRate.append(float(val))
            count += 1
        if ten_year_negative_growth_count <= 3 or five_year_negative_growth_count <= 1:
            self.isConsistentGrowing = True
            
        print("{} has {} years of 10 Yr negative growth".format(self.tickerName, ten_year_negative_growth_count))
        print("{} has {} years of 5 Yr negative growth".format(self.tickerName, five_year_negative_growth_count))

    def analyzeOperatingCashflow(self):
        cashflowGraph = self.tenYearCashFlow[::-1]
        df = pd.DataFrame(cashflowGraph, columns = ['Date', 'NetCashFlow'])
        # df.plot(x = 'Date', y = 'Net cash flow', kind='scatter', title='Net cash provided by operating activities')
        plt.scatter(df.Date, df.NetCashFlow)
        plt.show()
        print(df)
        plt.close('all')

    def analyzeCashflowForecast(self):
        df = pd.DataFrame(self.cashflowForecast, columns = ['cashflow forecast'])
        df.insert(1, 'Date', [self.now.year + i for i in range(-1, 10)], True)
        print(df)
        df.plot(x = 'Date', y = 'cashflow forecast', kind='bar', title='{} cash flow Forecast'.format(self.tickerName))
        plt.show()
        
    def analyzeGrowthRate(self):
        df = pd.DataFrame(self.growthRate, columns = ['growth rate'])
        df.insert(1, 'Date', [self.now.year - i for i in range(1, 12)], True)
        print(df)
        df.plot(x = 'Date', y = 'growth rate', kind='bar', title='{} growth rate'.format(self.tickerName))
        plt.show()      

    def evaluate(self):
        ##
        global info
        self.cashflowForecast[0] = self.freeCashFlow
        next_5_year_growth = self.next_5_year_growth
        past_5_year_growth = max(min(self.next_5_year_growth, self.past_5_year_growth)/2, self.discountedRate)
        past_10_year_growth = max(past_5_year_growth/2, self.discountedRate)
        ##
        for i in range(1, 21): # year 1 - 5
            if i == 1: # year 1
                self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + next_5_year_growth) 
            elif 2 <= i <= 5: # year 2 to year 5
                self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + next_5_year_growth) * (1 - self.discountedRate)
            elif 6 <= i <= 10: # year 6 to year 10
                self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + past_5_year_growth) * (1 - self.discountedRate)
            else: # year 10 to year 15
                self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + past_10_year_growth) * (1 - self.discountedRate)
        self.intrinsic_value = (sum(self.cashflowForecast) - self.cashflowForecast[0]  + self.investment - self.debt)/self.shares
        info.append((self.tickerName, int(self.intrinsic_value), self.marketPrice/self.intrinsic_value))
        
        

# generate report
file_ = open("intrinsic value report.txt", "w")
info = []
file_.write(str(datetime.datetime.now()))
file_.write('\n\n')

## technology
myTicker = ticker('BABA') 
myTicker = ticker('FB') 
myTicker = ticker('UNH') 
myTicker = ticker('LMT') 
myTicker = ticker('NOC') 
myTicker = ticker('AAPL') 
myTicker = ticker('JNJ')  
myTicker = ticker('GOOG')  
myTicker = ticker('INTC')  
myTicker = ticker('CSCO') 
myTicker = ticker('ORCL') 
myTicker = ticker('CRM') 
myTicker = ticker('EA') 


## financial service
myTicker = ticker('BAC') 
myTicker = ticker('WFC') 
myTicker = ticker('AXP') 
myTicker = ticker('V')  

## Consumer
myTicker = ticker('KO') 
myTicker = ticker('ROST')
myTicker = ticker('AMZN')
myTicker = ticker('WMT')

## Health care
myTicker = ticker('GILD')
myTicker = ticker('IDXX')
myTicker = ticker('VRTX')
myTicker = ticker('BIIB')
myTicker = ticker('ISRG')
myTicker = ticker('REGN')
myTicker = ticker('ILMN')

info.sort(key=lambda x:x[2])
for ticker, iv, discount in info:
    file_.write('{} : {} : {} \n'.format(ticker, iv, discount))
file_.close()
