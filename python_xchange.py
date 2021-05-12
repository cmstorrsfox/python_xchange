import matplotlib
import pandas as pd
import yfinance as yf
import warnings 
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import mplfinance as mpf

matplotlib.use("TkAgg")

warnings.simplefilter(action="ignore")

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

pd.options.plotting.backend = 'matplotlib'

ticker_data = pd.read_csv(r"NASDAQ.txt", delimiter="\t")
ticker_data["full"] = ticker_data["Symbol"]+" ("+ticker_data["Description"]+")"

ticker_list = ticker_data["full"].tolist()

#show folders function
def show_folders():
    output_folder_path = filedialog.askdirectory()
    outputfoldervar.set(output_folder_path)


#the stock review function
def get_stock_info(*args):

    #get ticker data
    ticker_name = stocknamevar.get()
    ticker_symbol = ticker_name.split(" ")[0]
    period = periodvar.get()
    interval = intervalvar.get()
    output_folder = outputfoldervar.get()

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


    #mplfinance
    fig, ax = mpf.plot(df, type="candle", style="yahoo", title=ticker_name+" - Interval = "+interval+" - Period = "+period, ylabel="Price ($)", returnfig=True)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    toolbarFrame = Frame(master=root)
    toolbarFrame.grid(row=7,column=0)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

    toolbar.update()

    canvas.get_tk_widget().grid(column=0, row=6, pady=3)

    #reset index
    df.reset_index(level=0, inplace=True)
    col_names = df.columns

    #remove timezone from columns
    
    df[col_names[0]] = df[col_names[0]].dt.tz_localize(None)

    #save high higher lower to Excel
    df.to_excel(output_folder+"/"+ticker_name+" - Interval = "+interval+" - Period = "+period+".xlsx")


    #root.destroy()
    #end of function


#create GUI
#root
root = Tk()
root.title("Stock Overview App")
root.geometry("800x800")


#variables
stocknamevar = StringVar()
periodvar = StringVar()
intervalvar = StringVar()
outputfoldervar = StringVar()

#elements
content = ttk.Frame(root)
stock_label = ttk.Label(content, text="Choose a stock", anchor="w")
stock = ttk.Combobox(content, values=ticker_list, textvariable=stocknamevar, width=50)
period_label = ttk.Label(content, text="Choose a period to review", anchor="w")
period = ttk.Combobox(content, values=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], textvariable=periodvar, width=50)
interval_label = ttk.Label(content, text="Choose an interval", anchor="w")
interval = ttk.Combobox(content, values=["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo", "3mo"], textvariable=intervalvar, width=50)
browse_label = ttk.Label(content, text="Choose where to save the file", anchor="w")
browse = ttk.Button(content, text="Browse", command=show_folders)
submit = ttk.Button(content, text="Submit", command=get_stock_info)


#layout
content.grid(column=0, row=0, pady=5, padx=100)
stock_label.grid(column=0, row=1, pady=5)
stock.grid(column=1, row=1, pady=5)
period_label.grid(column=0, row=2, pady=5)
period.grid(column=1, row=2, pady=5)
interval_label.grid(column=0, row=3, pady=5)
interval.grid(column=1, row=3, pady=5)
browse_label.grid(column=0, row=4, pady=5)
browse.grid(column=1, row=4, pady=5)
submit.grid(column=1, row=5, columnspan=2, pady=5)

root.mainloop()


