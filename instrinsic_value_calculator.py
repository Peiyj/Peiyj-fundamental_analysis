import requests

def main():
    # https://financialmodelingprep.com/developer/docs/
    tickerName = input("Enter your ticker: ") 
    five_year_growth_rate = input("Enter Cash flow growth rate (Yr 1-5): ")
    ten_year_growth_rate = input("Enter Cash flow growth rate (Yr 6-10): ")
    discounted_rate = input("Enter discounted rate: ")
    cashflow = fetchCashFlow(tickerName)
    debt = fetchDebt(tickerName)
    investment = fetchInvestment(tickerName)
    shares = fetchShares(tickerName)
    print(cashflow, debt, investment, shares)
    instrinsic_value = calculateIV(float(five_year_growth_rate), float(ten_year_growth_rate), \
                                        float(discounted_rate), cashflow, debt, investment, shares)
    print('intrinsic value', instrinsic_value)
    
def calculateIV(five_year_growth_rate, ten_year_growth_rate, discounted_rate, cashflow, debt, investment, shares):
    ten_year_cash_flow = [0.0] * 10
    for i in range(5): # year 1 - 5
        ten_year_cash_flow[i] = cashflow * ((1 + five_year_growth_rate) * (1 - discounted_rate)) ** i
    for i in range(5, 10): # year 6 - 10
        ten_year_cash_flow[i] = cashflow * ((1 + ten_year_growth_rate) * (1 - discounted_rate)) ** i
    instrinsic_value = (sum(ten_year_cash_flow) + investment - debt)/shares
    return instrinsic_value

def fetchCashFlow(tickerName):
    cash_flow_url = 'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/'
    response = requests.get(cash_flow_url + tickerName)
    assert(response.status_code == 200)
    return processCashFlowData(response.json())

def fetchDebt(tickerName):
    debt_url = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/'
    response = requests.get(debt_url + tickerName)
    assert(response.status_code == 200)
    return processDebtData(response.json())

def fetchInvestment(tickerName):
    investment_url = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/'
    response = requests.get(investment_url + tickerName)
    assert(response.status_code == 200)
    return processInvestmentData(response.json())

def fetchShares(tickerName):
    share_url = 'https://financialmodelingprep.com/api/v3/enterprise-value/'
    response = requests.get(share_url + tickerName)
    assert(response.status_code == 200)
    return processSharesData(response.json())

def processCashFlowData(json):
    for key, metrics in json.items():
        if key == 'financials':
            break
    assert(key == 'financials')
    for metric in metrics:
        assert(type(metric) == dict)
        for key, val in metric.items():
            if key == 'Free Cash Flow':
                return float(metric[key])
    return -1

def processDebtData(json):
    long_term_debt = ''
    for key, metrics in json.items():
        if key == 'financials':
            break
    assert(key == 'financials')
    for metric in metrics:
         for key, val in metric.items():
            if key == 'Long-term debt':
                return float(metric[key])
    return -1

def processInvestmentData(json):
    long_term_debt = ''
    for key, metrics in json.items():
        if key == 'financials':
            break
    assert(key == 'financials')
    for metric in metrics:
         for key, val in metric.items():
            if key == 'Cash and short-term investments':
                return float(metric[key])
    return -1

def processSharesData(json):
    long_term_debt = ''
    for key, metrics in json.items():
        if key == 'enterpriseValues':
            break
    assert(key == 'enterpriseValues')
    for metric in metrics:
         for key, val in metric.items():
            if key == 'Number of Shares':
                return float(metric[key])
    return -1
    
if __name__ == "__main__":
    main()