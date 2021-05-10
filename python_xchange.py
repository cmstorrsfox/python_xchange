import pandas as pd
import yfinance as yf
from ta import add_all_ta_features
import finplot as fplt
import warnings 
from tkinter import *
from tkinter import ttk
warnings.simplefilter(action="ignore")

ticker_data = pd.read_csv(r"src\NASDAQ.txt", delimiter="\t")
ticker_data["full"] = ticker_data["Symbol"]+" ("+ticker_data["Description"]+")"

ticker_list = ticker_data["full"].tolist()




#the stock review function
def get_stock_info(*args):
    #get ticker data
    ticker_name = stocknamevar.get()
    ticker_symbol = ticker_name.split()[0]
    period = periodvar.get()
    interval = intervalvar.get()

    ticker_data = yf.Ticker(ticker_symbol)

    df = ticker_data.history(period=period, interval=interval)

    #work out patterns
    #get previous and next day highs as columns in df
    df["Previous Day High"] = df["High"].shift(periods=-1)
    df["Next Day High"] = df["High"].shift(periods=1)
    df["Day After Next High"] = df["High"].shift(periods=2)

    #get previous and next day lows as columns in df
    df["Previous Day Low"] = df["Low"].shift(periods=-1)
    df["Next Day Low"] = df["Low"].shift(periods=1)
    df["Day After Next Low"] = df["Low"].shift(periods=2)

    #add percentage change to df
    df["Percentage Change"] = df["High"].pct_change(periods=1)


    #function to add True to rows that match the desired pattern
    def higher_pattern(row):
        if (row["High"] > row["Previous Day High"]) & (row["Next Day High"] > row["High"]) & (row["Next Day High"] > row["Day After Next High"]):
            val = True
        else:
            val = False
        return val

    #create column that shows whether or not a day is a match
    df["higher_pattern"] = df.apply(higher_pattern, axis=1)

    #function to add True to rows that match the desired pattern
    def lower_pattern(row):
        if (row["Low"] < row["Previous Day Low"]) & (row["Next Day Low"] < row["Low"]) & (row["Next Day Low"] > row["Day After Next Low"]):
            val = True
        else:
            val = False
        return val

    #create column that shows whether or not a day is a match
    df["lower_pattern"] = df.apply(lower_pattern, axis=1)

    #remove unnecessary columns from df
    df = df[["Open", "Close", "High", "Low", "Percentage Change", "higher_pattern", "lower_pattern"]]



    #reset index
    df.reset_index(level=0, inplace=True)
    col_names = df.columns

    #remove timezone from columns
    
    df[col_names[0]] = df[col_names[0]].dt.tz_localize(None)

    #save high higher lower to Excel
    df.to_excel(ticker_name+" - Interval = "+interval+" - Period = "+period+".xlsx")

    ax = fplt.create_plot(ticker_name+" - "+interval+" - "+period, rows=1)
    candles = df[[col_names[0], "Open", "Close", "High", "Low"]]
    fplt.candlestick_ochl(candles, ax=ax)
    high_wicks = df["higher_pattern"]
    df.loc[(high_wicks), 'marker'] = df['High']
    fplt.plot(df[col_names[0]], df['marker'], ax=ax, color='#4a5', style='^', legend='HH')

    fplt.show()
    root.destroy()
    #end of function

#create GUI
#root
root = Tk()

#variables
stocknamevar = StringVar()
periodvar = StringVar()
intervalvar = StringVar()

#elements
content = ttk.Frame(root)
stock_label = ttk.Label(content, text="Choose a stock")
stock = ttk.Combobox(content, values=ticker_list, textvariable=stocknamevar)
period_label = ttk.Label(content, text="Choose a period to review")
period = ttk.Combobox(content, values=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], textvariable=periodvar)
interval_label = ttk.Label(content, text="Choose an interval")
interval = ttk.Combobox(content, values=["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo", "3mo"], textvariable=intervalvar)
submit = ttk.Button(content, text="Submit", command=get_stock_info)


#layout
content.grid(column=0, row=0, pady=3, padx=3)
stock_label.grid(column=0, row=1, pady=3, padx=3)
stock.grid(column=1, row=1, pady=3, padx=3)
period_label.grid(column=0, row=2, pady=3, padx=3)
period.grid(column=1, row=2, pady=3, padx=3)
interval_label.grid(column=0, row=3, pady=3, padx=3)
interval.grid(column=1, row=3, pady=3, padx=3)
submit.grid(column=0, row=4, columnspan=2, pady=3, padx=3)

root.mainloop()


