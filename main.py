import json
import requests as r
from datetime import datetime
from config import FMP_KEY
from lists import SP, NYSE_NASDAQ
from industry_lists import electronic_gaming_and_multimedia
from ai_categories import chip_manufacturers, cloud_providers, ai_indstry_leaders, ai_services


def grossProfitRatio(income_statements, gross_profit_ratio_weight):
    print('Gross Profit Ratio')
    print('Formula: Gross Profit / Revenue * 100')
    print('Good: >40%')
    print('Neutral: 20%-40%')
    print('Bad: <20%')
    print(f'Weight: {gross_profit_ratio_weight}')
    increment = gross_profit_ratio_weight * 5
    gross_profit_score = 0
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        gross_profit_ratio = income_statements[i]['grossProfitRatio']
        if gross_profit_ratio >= 0.4:
            gross_profit_score += increment
            print(f'{year} Gross Profit Ratio: {round((gross_profit_ratio * 100), 1)}%; Good: +{increment} points')
        elif gross_profit_ratio <= 0.2:
            gross_profit_score -= increment
            print(f'{year} Gross Profit Ratio: {round((gross_profit_ratio * 100), 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} Gross Profit Ratio: {round((gross_profit_ratio * 100), 1)}%; Neutral: +0 points')
        increment -= gross_profit_ratio_weight
    print(f'Total Gross Profit Score: {gross_profit_score}')
    print()
    return gross_profit_score


def expensesSGA(income_statements, sga_ratio_weight):
    print('Selling, General, & Administrative Expenses')
    print('Formula: SGA Expenses / Gross Profit * 100')
    print('Good: <30%')
    print('Neutral: 30%-80%')
    print('Bad: >80%')
    print(f'Weight: {sga_ratio_weight}')
    sga_score = 0
    increment = sga_ratio_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        sga_expenses = income_statements[i]['sellingGeneralAndAdministrativeExpenses']
        gross_profit = income_statements[i]['grossProfit']
        sga_ratio = sga_expenses / gross_profit
        if sga_ratio < 0.3:
            sga_score += increment
            print(f'{year} SGA Ratio: {round(sga_ratio * 100, 1)}%; Good: +{increment} points')
        elif sga_ratio > 0.8:
            sga_score -= increment
            print(f'{year} SGA Ratio: {round(sga_ratio * 100, 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} SGA Ratio: {round(sga_ratio * 100, 1)}%; Neutral: +0 points')
        increment -= sga_ratio_weight
    print(f'Total SGA Ratio Score: {sga_score}')
    print()
    return sga_score


def expensesRD(income_statements, rd_ratio_weight):
    print('Research & Development Expenses')
    print('Formula: R&D Expenses / Gross Profit * 100')
    print('Good/Neutral: <25%')
    print('Bad: >=25%')
    print(f'Weight: {rd_ratio_weight}')
    rd_score = 0
    increment = rd_ratio_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        rd_expenses = income_statements[i]['researchAndDevelopmentExpenses']
        gross_profit = income_statements[i]['grossProfit']
        rd_ratio = rd_expenses / gross_profit
        if rd_ratio >= 0.25:
            rd_score -= increment
            print(f'{year} R&D Ratio: {round(rd_ratio * 100, 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} R&D Ratio: {round(rd_ratio * 100, 1)}%; Good/Neutral: +0 points')
        increment -= rd_ratio_weight
    print(f'Total R&D Ratio Score: {rd_score}')
    print()
    return rd_score


def depreciationRatio(income_statements, depreciation_ratio_weight):
    print('Depreciation & Amortization')
    print('Formula: Depreciation / Gross Profit * 100')
    print('Good: <10%')
    print('Neutral: 10%-20%')
    print('Bad: >20%')
    print(f'Weight: {depreciation_ratio_weight}')
    depreciation_score = 0
    increment = depreciation_ratio_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        depreciation = income_statements[i]['depreciationAndAmortization']
        gross_profit = income_statements[i]['grossProfit']
        depreciation_ratio = depreciation / gross_profit
        if depreciation_ratio < 0.1:
            depreciation_score += increment
            print(f'{year} Depreciation Ratio: {round(depreciation_ratio * 100, 1)}%; Good: +{increment} points')
        elif depreciation_ratio > 0.2:
            depreciation_score -= increment
            print(f'{year} Depreciation Ratio: {round(depreciation_ratio * 100, 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} Depreciation Ratio: {round(depreciation_ratio * 100, 1)}%; Neutral: +0 points')
        increment -= depreciation_ratio_weight
    print(f'Total Depreciation Ratio Score: {depreciation_score}')
    print()
    return depreciation_score


def interestExpense(income_statements, interest_expense_ratio_weight):
    print('Interest Expense')
    print('Formula: Interest Expense / Operating Income * 100')
    print('IMPORTANT: THIS IS A STANDARDIZED SPECIFICATION AND')
    print('GOOD/BAD INTERET RATIOS CAN VARY WIDELY BY INDUSTRY')
    print('Good: <15%')
    print('Neutral: 15%-30%')
    print('Bad: >30%')
    print(f'Weight: {interest_expense_ratio_weight}')
    interest_expense_score = 0
    increment = interest_expense_ratio_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        interest_expense = income_statements[i]['interestExpense']
        operating_income = income_statements[i]['operatingIncome']
        interest_expense_ratio = interest_expense / operating_income
        if interest_expense_ratio < 0.15:
            interest_expense_score += increment
            print(f'{year} Interest Expense Ratio: {round(interest_expense_ratio * 100, 1)}%; Good: +{increment} points')
        elif interest_expense_ratio > 0.3:
            interest_expense_score -= increment
            print(f'{year} Interest Expense Ratio: {round(interest_expense_ratio * 100, 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} Interest Expense Ratio: {round(interest_expense_ratio * 100, 1)}%; Neutral: +0 points')
        increment -= interest_expense_ratio_weight
    print(f'Total Interest Expense Ratio Score: {interest_expense_score}')
    print()
    return interest_expense_score


def netEarningsTrend(income_statements, net_earnings_trend_weight):
    print('Net Earnings Trend')
    print("Criteria: Is current year's net earnings higher than the previous year?")
    print('Good: current > previous')
    print('Neutral: current = previous')
    print('Bad: current < previous')
    print(f'Weight: {net_earnings_trend_weight}')
    net_earnings_trend_score = 0
    increment = net_earnings_trend_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        current_earnings =  income_statements[i]['netIncome']
        previous_earnings = income_statements[i+1]['netIncome']
        if current_earnings > previous_earnings:
            print(f'{year} Net Earnings: {current_earnings}; Good: +{increment} points')
            net_earnings_trend_score += increment
        elif current_earnings < previous_earnings:
            print(f'{year} Net Earnings: {current_earnings}; Bad: -{increment} points')
            net_earnings_trend_score -= increment
        else:
            print(f'{year} Net Earnings: {current_earnings}; Neutral: +0 points')
        increment -= net_earnings_trend_weight
    print(f"{int(income_statements[5]['calendarYear'])-1} Net Earnings: {income_statements[5]['netIncome']} (shown for comparison)")
    print(f'Total Net Earnings Trend Score: {net_earnings_trend_score}')
    print()
    return net_earnings_trend_score


def netEarningsRatio(income_statements, net_earnings_ratio_weight):
    print('Net Earnings to Revenue Ratio')
    print('Formula: Net Earnings / Revenue * 100')
    print('IMPORTANT: IF BANKS OR FINANCIAL COMPANIES HAVE A HIGH')
    print('RATIO, IT CAN MEAN THEY ARE INVOLVED IN RISKY LENDING')
    print('Good: >20%')
    print('Neutral: 11%-20%')
    print('Bad: <10%')
    print(f'Weight: {net_earnings_ratio_weight}')
    net_earnings_ratio_score = 0
    increment = net_earnings_ratio_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        net_earnings = income_statements[i]['netIncome']
        revenue = income_statements[i]['revenue']
        net_earnings_ratio = net_earnings / revenue
        if net_earnings_ratio > 0.2:
            net_earnings_ratio_score += increment
            print(f'{year} Net Earnings to Revenue Ratio: {round(net_earnings_ratio * 100, 1)}%; Good: +{increment} points')
        elif net_earnings_ratio < 0.1:
            net_earnings_ratio_score -= increment
            print(f'{year} Net Earnings to Revenue Ratio: {round(net_earnings_ratio * 100, 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} Net Earnings to Revenue Ratio: {round(net_earnings_ratio * 100, 1)}%; Neutral: +0 points')
        increment -= net_earnings_ratio_weight
    print(f'Total Net Earnings to Revenue Ratio Score: {net_earnings_ratio_score}')
    print()
    return net_earnings_ratio_score


def epsTrend(income_statements, eps_trend_weight):
    print('Earnings Per Share Trend')
    print("Criteria: Is current year's EPS higher than the previous year?")
    print('Good: current > previous')
    print('Neutral: current = previous')
    print('Bad: current < previous')
    print(f'Weight: {eps_trend_weight}')
    eps_trend_score = 0
    increment = eps_trend_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        current_eps =  income_statements[i]['eps']
        previous_eps = income_statements[i+1]['eps']
        if current_eps > previous_eps:
            print(f'{year} Earnings Per Share: {round(current_eps, 2)}; Good: +{increment} points')
            eps_trend_score += increment
        elif current_eps < previous_eps:
            print(f'{year} Earnings Per Share: {round(current_eps, 2)}; Bad: -{increment} points')
            eps_trend_score -= increment
        else:
            print(f'{year} Earnings Per Share: {round(current_eps, 2)}; Neutral: +0 points')
        increment -= eps_trend_weight
    print(f"{int(income_statements[5]['calendarYear'])-1} Earnings Per Share: {income_statements[5]['eps']} (shown for comparison)")
    print(f'Total Earnings Per Share Trend Score: {eps_trend_score}')
    print()
    return eps_trend_score


def debtToEquityRatio(ratios, debt_to_equity_weight):
    print("Debt to Equity Ratio")
    print("Formula: Total Liabilities / Shareholders' Equity * 100")
    print('Good: <80%')
    print('Neutral: 80%-100%')
    print('Bad: >100%')
    print(f'Weight: {debt_to_equity_weight}')
    increment = debt_to_equity_weight * 5
    debt_to_equity_score = 0
    for i in range(5):
        year = int(ratios[i]['date'][:4])
        debt_to_equity_ratio = ratios[i]['debtEquityRatio']
        if debt_to_equity_ratio < 0.8:
            debt_to_equity_score += increment
            print(f'{year} Debt to Equity Ratio: {round((debt_to_equity_ratio * 100), 1)}%; Good: +{increment} points')
        elif debt_to_equity_ratio > 1:
            debt_to_equity_score -= increment
            print(f'{year} Debt to Equity Ratio: {round((debt_to_equity_ratio * 100), 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} Debt to Equity Ratio: {round((debt_to_equity_ratio * 100), 1)}%; Neutral: +0 points')
        increment -= debt_to_equity_weight
    print(f'Total Debt to Equity Ratio Score: {debt_to_equity_score}')
    print()
    return debt_to_equity_score


def retainedEarningsGrowth(balance_sheets, retained_earnings_growth_weight):
    print('Retained Earnings Growth')
    print('Formula: (Current Retained Earnings - Previous Retained Earnings) /')
    print('Previous Retained Earnings * 100')
    print('Good: >5%')
    print('Neutral: 0%-5%')
    print('Bad: <0%')
    print(f'Weight: {retained_earnings_growth_weight}')
    retained_earnings_growth_score = 0
    increment = retained_earnings_growth_weight * 5
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        current_retained_earnings = balance_sheets[i]['retainedEarnings']
        previous_retained_earnings = balance_sheets[i+1]['retainedEarnings']
        retained_earnings_growth_rate = (current_retained_earnings - previous_retained_earnings) / previous_retained_earnings * 100
        if retained_earnings_growth_rate > 5:
            print(f'{year} Retained Earings Growth: {round(retained_earnings_growth_rate, 2)}%; Good: +{increment} points')
            retained_earnings_growth_score += increment
        elif retained_earnings_growth_rate < 0:
            print(f'{year} Retained Earings Growth: {round(retained_earnings_growth_rate, 2)}%; Bad: -{increment} points')
            retained_earnings_growth_score -= increment
        else:
            print(f'{year} Retained Earings Growth: {round(retained_earnings_growth_rate, 2)}%; Neutral: +0 points')
        increment -= retained_earnings_growth_weight
    # print(f"{int(income_statements[5]['calendarYear'])-1} Retained Earings Growth: {balance_sheets[5]['retainedEarnings']} (shown for comparison)")
    print(f'Total Retained Earings Growth Score: {retained_earnings_growth_score}')
    print()
    return retained_earnings_growth_score


def returnOnEquity(ratios, return_on_equity_weight):
    print("Return On Equity")
    print("Formula: Net Earnings / Shareholders' Equity * 100")
    print('Good: >20%')
    print('Neutral: 15%-20%')
    print('Bad: <15%')
    print(f'Weight: {return_on_equity_weight}')
    increment = return_on_equity_weight * 5
    return_on_equity_score = 0
    for i in range(5):
        year = int(ratios[i]['date'][:4])
        return_on_equity = ratios[i]['returnOnEquity']
        if return_on_equity > 0.2:
            return_on_equity_score += increment
            print(f'{year} Return on Equity: {round((return_on_equity * 100), 1)}%; Good: +{increment} points')
        elif return_on_equity < 0.15:
            return_on_equity_score -= increment
            print(f'{year} Return on Equity: {round((return_on_equity * 100), 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} Return on Equity: {round((return_on_equity * 100), 1)}%; Neutral: +0 points')
        increment -= return_on_equity_weight
    print(f'Total Return On Equity Score: {return_on_equity_score}')
    print()
    return return_on_equity_score


def capitalExpenditureRatio(cash_flow_statements, capital_expenditure_ratio_weight):
    print('Capital Expenditure Ratio')
    print('Formula: Capital Expenditure / Net Earnings * 100')
    print('Good: <50%')
    print('Neutral: 50%-100%')
    print('Bad: >100%')
    print(f'Weight: {capital_expenditure_ratio_weight}')
    increment = capital_expenditure_ratio_weight * 5
    capital_expenditure_ratio_score = 0
    for i in range(5):
        year = int(cash_flow_statements[i]['date'][:4])
        capital_expenditure = cash_flow_statements[i]['capitalExpenditure']
        net_earnings = cash_flow_statements[i]['netIncome']
        # print(net_earnings)
        capital_expenditure_ratio = (capital_expenditure * -1) / net_earnings
        if capital_expenditure_ratio < 0.5:
            if capital_expenditure_ratio > 0:
                print(f'{year} Capital Expenditure Ratio: {round((capital_expenditure_ratio * 100), 1)}%; Good: +{increment} points')
                capital_expenditure_ratio_score += increment
            else:
                print(f"{year} Capital Expenditure Ratio: CAN'T CALCULATE: NEGATIVE NET EARNINGS; Bad: -{increment} points")
                capital_expenditure_ratio_score -= increment
        elif capital_expenditure_ratio > 1:
            capital_expenditure_ratio_score -= increment
            print(f'{year} Capital Expenditure Ratio: {round((capital_expenditure_ratio * 100), 1)}%; Bad: -{increment} points')
        else:
            print(f'{year} Capital Expenditure Ratio: {round((capital_expenditure_ratio * 100), 1)}%; Neutral: +0 points')
        increment -= capital_expenditure_ratio_weight
    print(f'Total Capital Expenditure Ratio Score: {capital_expenditure_ratio_score}')
    print()
    return capital_expenditure_ratio_score


def interestRate(quote, interest_rate_weight):
    print('Equity Bond: Interest Rate')
    print('Formula: EPS / Price * 100')
    print('Good: >10%')
    print('Neutral: 3%-10%')
    print('Bad: <3%')
    print(f'Weight: {interest_rate_weight}')
    increment = interest_rate_weight * 15
    interest_rate_score = 0
    price = quote[0]['price']
    print(f'Price: ${price}')
    eps = quote[0]['eps']
    print(f'EPS: ${eps}')
    interest_rate = eps / price
    # print(f"Interest Rate: {round(interest_rate, 2)}%")
    if interest_rate > 0.1:
        print(f"Interest Rate: {round(interest_rate * 100, 1)}%; Good: +{increment} points")
        interest_rate_score += increment
    elif interest_rate < 0.03:
        print(f"Interest Rate: {round(interest_rate * 100, 1)}%; Bad: -{increment} points")
        interest_rate_score -= increment
    else:
        print(f"Interest Rate: {round(interest_rate * 100, 1)}%; Neutral: +0 points")
    print(f'Interest Rate Score: {interest_rate_score}')
    print()
    return interest_rate_score


def pretaxEpsGrowth(income_statements, pretax_eps_weight):
    print('Equity Bond: Pretax EPS Growth')
    print('Formula: ((Current Pretax EPS - Previous Pretax EPS) /')
    print('  Previous Pretax EPS) * 100')
    print('Good: >10%')
    print('Neutral: 0%-10%')
    print('Bad: <0%')
    print(f'Weight: {pretax_eps_weight}')
    increment = pretax_eps_weight * 5
    pretax_eps_score = 0
    for i in range(5):
        year = int(income_statements[i]['calendarYear'])
        current_pretax_earnings = income_statements[i]['incomeBeforeTax']
        current_shares_outstanding = income_statements[i]['weightedAverageShsOut']
        current_pretax_eps = current_pretax_earnings / current_shares_outstanding
        previous_pretax_earnings = income_statements[i+1]['incomeBeforeTax']
        previous_shares_outstanding = income_statements[i+1]['weightedAverageShsOut']
        previous_pretax_eps = previous_pretax_earnings / previous_shares_outstanding
        pretax_eps_growth = ((current_pretax_eps - previous_pretax_eps) / previous_pretax_eps)
        # print(f'Current Pretax EPS: {current_pretax_eps}; Previous Pretax EPS: {previous_pretax_eps}')
        if pretax_eps_growth > 0.1:
            print(f'{year} Pretax EPS Growth: {round(pretax_eps_growth * 100, 1)}%; Good: +{increment} points')
            pretax_eps_score += increment
        elif pretax_eps_growth < 0:
            print(f'{year} Pretax EPS Growth: {round(pretax_eps_growth * 100, 1)}%; Bad: -{increment} points')
            pretax_eps_score -= increment
        else:
            print(f'{year} Pretax EPS Growth: {round(pretax_eps_growth * 100, 1)}%; Neutral: +0 points')
        increment -= pretax_eps_growth_weight
        # print(f'Current Pretax EPS: {current_pretax_eps}; Previous Pretax EPS: {previous_pretax_eps}')
    print(f'Total Pretax EPS Growth Score: {pretax_eps_score}')
    print()
    return pretax_eps_score


def trailingToForwardPE(quote, estimates, trailing_to_forward_pe_weight):
    print('Forward P/E Ratio')
    print('Good: Forward < Trailing')
    print('Neutral: Forward = Trailing')
    print('Bad: Forward > Trailing')
    print(f'Weight: {trailing_to_forward_pe_weight}')
    trailing_pe = quote[0]['pe']
    print(f'Trailing P/E: {trailing_pe}')
    price = quote[0]['price']
    # print(f'Price: ${price}')
    estimate = estimates[0]['estimatedEpsAvg']
    # print(f'Estimated Average EPS: {estimate}')
    forward_pe = price / estimate
    print(f'Forward P/E: {round(forward_pe, 2)}')
    forward_pe_score = 0
    if forward_pe < trailing_pe:
        forward_pe_score += (15 * trailing_to_forward_pe_weight)
        print(f'Good: +{15 * trailing_to_forward_pe_weight} points')
    elif forward_pe > trailing_pe:
        forward_pe_score -= (15 * trailing_to_forward_pe_weight)
        print(f'Bad: -{15 * trailing_to_forward_pe_weight} points')
    else:
        print(f'Neutral: +0 points')
    print(f'Total Forward/Trialing P/E Ratio Score: {forward_pe_score}')
    print()
    return forward_pe_score


def peRatio(quote, pe_ratio_weight):
    pe_ratio = quote[0]['pe']
    # print(pe_ratio)
    print(f'P/E Ratio: {pe_ratio}')
    print()


def toDatabase(ticker, profile, score, quote, date):
    # print()
    market_cap = quote[0]['marketCap']
    pe_ratio = quote[0]['pe']
    industry = profile[0]['industry']
    # print(f'Ticker: {ticker}')
    # print(f'Score: {score}')
    # print(f'Industry: {industry}')
    # print(f'P/E Ratio: {pe_ratio}')
    # print(f'Market Cap: {market_cap}')
    # print(f'Date: {date}')
    with open('database.json', 'r') as file:
        data = json.load(file)
    # Check if the ticker already exists in the data
    if ticker in data:
        # Update the existing data with the new values
        data[ticker]['score'] = score
        data[ticker]['industry'] = industry
        data[ticker]['pe_ratio'] = pe_ratio
        data[ticker]['market_cap'] = market_cap
        data[ticker]['date'] = date
    else:
        # Create a new entry for the ticker
        data[ticker] = {
            'score': score,
            'industry': industry,
            'pe_ratio': pe_ratio,
            'market_cap': market_cap,
            'date': date
        }
    with open('database.json', 'w') as file:
        json.dump(data, file, indent=4)
    # print()


if __name__ == "__main__":
    tickers = ['GOOGL', 'AMZN', 'MSFT']

    date = datetime.now().strftime('%Y-%m-%d')
    print(f'Date: {date}')
    print()

    for ticker in tickers:
        try:
            print(ticker)
            income_statements = r.get(f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=6&apikey={FMP_KEY}')
            income_statements = income_statements.json()
            # print(income_statements)
            balance_sheets = r.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=6&apikey={FMP_KEY}')
            balance_sheets = balance_sheets.json()
            # print(balance_sheets)
            cash_flow_statements = r.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=6&apikey={FMP_KEY}')
            cash_flow_statements = cash_flow_statements.json()
            # print(cash_flow_statements)
            ratios = r.get(f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?limit=5&apikey={FMP_KEY}')
            ratios = ratios.json()
            # print(ratios)
            quote = r.get(f'https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_KEY}')
            quote = quote.json()
            # print(quote)
            profile = r.get(f'https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_KEY}')
            profile = profile.json()
            # print(profile)
            estimates = r.get(f'https://financialmodelingprep.com/api/v3/analyst-estimates/{ticker}?limit=30&apikey={FMP_KEY}')
            estimates = estimates.json()
            # print(estimates)

            print()

            # Income Metrics:
            gross_profit_ratio_weight = 1
            sga_ratio_weight = 1
            rd_ratio_weight = 1
            depreciation_ratio_weight = 1
            interest_expense_ratio_weight = 1
            net_earnings_ratio_weight = 1
            return_on_equity_weight = 2
            capital_expenditure_ratio_weight = 1
            interest_rate_weight = 1

            # Stability Metrics:
            debt_to_equity_ratio_weight = 3

            # Growth Metrics:
            net_earnings_trend_weight = 1
            eps_trend_weight = 1
            retained_earnings_growth_weight = 3
            pretax_eps_growth_weight = 1
            trailing_to_forward_pe_weight = 3

            # Value Metrics:
            pe_ratio_weight = 0

            print("Income Metrics:")
            print(f'Gross Profit Ratio Weight: {gross_profit_ratio_weight}')
            print(f'SGA Ratio Weight: {sga_ratio_weight}')
            print(f'R&D Ratio Weight: {rd_ratio_weight}')
            print(f'Depreciation Ratio Weight: {depreciation_ratio_weight}')
            print(f'Interest Expense Ratio Weight: {interest_expense_ratio_weight}')
            print(f'Net Earnings to Revenue Ratio Weight: {net_earnings_ratio_weight}')
            print(f'Return on Equity Weight: {return_on_equity_weight}')
            print(f'Capital Expenditure Ratio Weight: {capital_expenditure_ratio_weight}')
            print(f'Equity Bond: Interest Rate Weight: {interest_rate_weight}')
            print()
            print("Stability Metrics:")
            print(f'Debt to Equity Ratio Weight: {debt_to_equity_ratio_weight}')
            print()
            print("Growth Metrics:")
            print(f'Net Earnings Trend Weight: {net_earnings_trend_weight}')
            print(f'Earnings Per Share Trend Weight: {eps_trend_weight}')
            print(f'Retained Ernings Growth Weight: {retained_earnings_growth_weight}')
            print(f'Equity Bond: Pretax EPS Growth Weight: {pretax_eps_growth_weight}')
            print(f'Trailing to Forward P/E Ratio Weight: {trailing_to_forward_pe_weight}')
            print()
            print("Value Metrics:")
            # print(f'P/E Ratio Weight: {pe_ratio_weight}')
            print()

            score = 0

            # Income
            print("~~~Income~~~")
            print()
            score += grossProfitRatio(income_statements, gross_profit_ratio_weight)
            score += expensesSGA(income_statements, sga_ratio_weight) 
            score += expensesRD(income_statements, rd_ratio_weight)
            score += depreciationRatio(income_statements, depreciation_ratio_weight)
            score += interestExpense(income_statements, interest_expense_ratio_weight)
            score += netEarningsRatio(income_statements, net_earnings_ratio_weight)
            score += returnOnEquity(ratios, return_on_equity_weight)
            score += capitalExpenditureRatio(cash_flow_statements, capital_expenditure_ratio_weight)

            # Stability
            print("~~~Stability~~~")
            print()
            score += debtToEquityRatio(ratios, debt_to_equity_ratio_weight)

            # Growth
            print("~~~Growth~~~")
            print()
            score += netEarningsTrend(income_statements, net_earnings_trend_weight)
            score += epsTrend(income_statements, eps_trend_weight)
            score += retainedEarningsGrowth(balance_sheets, retained_earnings_growth_weight)
            score += pretaxEpsGrowth(income_statements, pretax_eps_growth_weight)
            score += trailingToForwardPE(quote, estimates, trailing_to_forward_pe_weight)

            # Value
            print("~~~Value~~~")
            print()
            peRatio(quote, pe_ratio_weight)
            score += interestRate(quote, interest_rate_weight)

            print(f'{ticker} Score: {score}')

            toDatabase(ticker, profile, score, quote, date)

            print()
            print('========================================================')
            print()

        except:
            print()
            print(f'ERROR: {ticker}')
            print()
            print('========================================================')
            print()
