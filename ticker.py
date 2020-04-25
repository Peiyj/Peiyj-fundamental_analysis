import requests

class ticker(object):
    def __init__(self, tickerName):
        ##
        self.api = 'https://financialmodelingprep.com/api/v3/'
        self.tickerName = tickerName 
        self.tenYearCashFlow = []
        self.growthRate = []
        self.debt = 0
        self.investment = 0 
        self.shares = 0
        self.intrinsic_value = 0
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
        long_term_growth = sum(self.growthRate) / len(self.growthRate)
        discounted_rate = 0.05
        ten_year_cash_flow = [0.0] * 10
        cashflow = self.tenYearCashFlow[0]
        investment = self.investment
        debt = self.debt
        shares = self.shares
        ##
        for i in range(5): # year 1 - 5
            ten_year_cash_flow[i] = cashflow * ((1 + short_term_growth) * (1 - discounted_rate)) ** i
        for i in range(5, 10): # year 6 - 10
            ten_year_cash_flow[i] = cashflow * ((1 + long_term_growth) * (1 - discounted_rate)) ** i
        self.intrinsic_value = (sum(ten_year_cash_flow) + investment - debt)/shares
        print('{} final intrinsic value is {}'.format(self.tickerName, self.intrinsic_value))

    def fetchCashFlow(self):
        cash_flow_url = self.api + 'financials/cash-flow-statement/' + self.tickerName
        response = requests.get(cash_flow_url)
        assert(response.status_code == 200)
        
        cashflow_json = response.json()
        for key, metrics in cashflow_json.items():
            if key == 'financials':
                break
        assert(key == 'financials')
        for metric in metrics:
            assert(type(metric) == dict)
            for key, val in metric.items():
                if key == 'Operating Cash Flow':
                    self.tenYearCashFlow.append(float(val))

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
# create new object
myTicker = ticker('AMZN')
myTicker = ticker('MSFT')
myTicker = ticker('AAPL')
myTicker = ticker('BABA')
myTicker = ticker('FB')
myTicker = ticker('MCD')
myTicker = ticker('UNH')
myTicker = ticker('V')
myTicker = ticker('LMT')
myTicker = ticker('NOC')