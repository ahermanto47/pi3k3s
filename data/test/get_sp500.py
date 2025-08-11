import pandas as pd

def tickers_sp500(include_company_data = False):
    '''Downloads list of tickers currently listed in the S&P 500 '''
    # get list of all S&P 500 stocks
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    # sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=True)

    if include_company_data:
        return sp500

    sp_tickers = sp500.Symbol.tolist()
    sp_tickers = sorted(sp_tickers)
    
    return sp_tickers

if __name__ == "__main__":
    sp_tickers = tickers_sp500()
    with open("sp500_tickers.txt", "w") as f:
        for ticker in sp_tickers:
            f.write(f"{ticker}\n")
