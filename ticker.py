import requests
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen

class ticker(object):
    def __init__(self, tickerNames):
        ##
        self.options = Options()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.file_ = open("intrinsic value report.txt", "w")
        self.file_.write(str(datetime.datetime.now()))
        self.file_.write('\n\n')
        ##
        self.cashflowForecast = [0] * 11
        self.marketprice = 0
        self.debt = 0
        self.investment = 0 
        self.shares = 0
        self.intrinsic_value = 0
        self.next_5_year_growth = 0
        self.discountedRate = 0
        self.past_5_year_growth = 0
        for tickerName in tickerNames:
            self.tickerName = tickerName
            ##
            self.fetchFreeCashFlow()
            self.fetchMarketPrice()
            self.fetchShares()
            self.fetchDiscountedRate()
            self.fetchLongTermGrowthRate()
            self.evaluate()

    def fetchFreeCashFlow(self):
        self.driver.get('http://financials.morningstar.com/cash-flow/cf.html?t={}&region=usa&culture=en-US'.format(self.tickerName))
        cash = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[3]/div[3]/div/div/div/div/div[19]/div[6]").text
        if ',' in cash: self.cashflow = float(cash.replace(',', '')) * 1000000
        else: self.cashflow = float(cash) * 1000000   
        self.file_.write("{}'s free cashflow {}\n".format(self.tickerName, self.cashflow))
        print('free cashflow ', self.cashflow)

    def fetchMarketPrice(self):
        self.driver.get('https://finance.yahoo.com/quote/{}'.format(self.tickerName))
        marketprice = self.driver.find_element_by_xpath("//*[@id='quote-header-info']/div[3]/div/div/span[1]").text
        if ',' in marketprice: self.marketprice = float(marketprice.replace(',', '')) * 1000000
        else: self.marketprice = float(marketprice) * 1000000
        self.file_.write("{}'s marketprice {}\n".format(self.tickerName, self.marketprice))
        print('marketprice ', self.marketprice)

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
        print(self.next_5_year_growth, self.past_5_year_growth )

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
        self.driver.get('http://financials.morningstar.com/ratios/r.html?t={}&region=usa&culture=en-US&ownerCountry=USA'.format(self.tickerName))
        shares = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/div/div/table/tbody/tr[18]/td[10]").text
        if ',' in shares:
            shares = shares.replace(',','')
        self.shares = float(shares) * 1000000
        self.file_.write("{}'s shares {}\n".format(self.tickerName, self.shares))
        print('shares ', self.shares) 

    def evaluate(self):
        ##
        # global info
        self.cashflowForecast[0] = self.cashflow
        next_5_year_growth = self.next_5_year_growth
        past_5_year_growth = min(0.15, self.past_5_year_growth)
        print(next_5_year_growth, past_5_year_growth)
        ##
        for i in range(1, 11): # year 1 - 5
            if i <= 5: # year 1 - 5
                self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + next_5_year_growth) * (1 - self.discountedRate)
            elif 6 <= i <= 9: # year 6 to year 9
                self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + past_5_year_growth) * (1 - self.discountedRate)
            else: # year 10: multiply the 10th year with 12 to get the sell off value
                self.cashflowForecast[i] = self.cashflowForecast[i-1] * (1 + past_5_year_growth) * (1 - self.discountedRate) * 12
        self.intrinsic_value = sum(self.cashflowForecast)/self.shares
        # info.append((self.tickerName, int(self.intrinsic_value), self.marketPrice/self.intrinsic_value))
        self.file_.write("{}'s instrinsic value is {}\n\n".format(self.tickerName, self.intrinsic_value))
        print("{}'s iv is : {}".format(self.tickerName, self.intrinsic_value))
        
        
# generate report
myTicker = ticker(['FB', 'GOOG', 'MSFT', 'CRM']) 
