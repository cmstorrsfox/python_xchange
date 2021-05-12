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
from yfinance.utils import ProgressBar

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

#configure progress bar
def start_progress_bar():
    progress = ProgressBar(root, orient=HORIZONTAL, length=100, mode="indeterminate")
    # Function responsible for the updation
    # of the progress bar value
    def bar():
        import time
        progress['value'] = 20
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 40
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 50
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 60
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 80
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 100
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 80
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 60
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 50
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 40
        root.update_idletasks()
        time.sleep(0.5)
    
        progress['value'] = 20
        root.update_idletasks()
        time.sleep(0.5)
        progress['value'] = 0
    
    bar()


#create df function
def create_df():

    #get ticker data
    ticker_name = stocknamevar.get()
    ticker_symbol = ticker_name.split(" ")[0]
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

    return df


#the stock review function
def draw_chart(*args):
    ticker_name = stocknamevar.get()
    period = periodvar.get()
    interval = intervalvar.get()
    
    #get df info
    data = create_df()


    #mplfinance
    fig, ax = mpf.plot(data, type="candle", style="yahoo", title=ticker_name+" - Interval = "+interval+" - Period = "+period, ylabel="Price ($)", returnfig=True)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    toolbarFrame = Frame(master=root)
    toolbarFrame.grid(row=8,column=0)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

    toolbar.update()

    canvas.get_tk_widget().grid(column=0, row=7, pady=10, padx=10)

    #end of chart function


#save function
def save_df():
    df = create_df()
    output_folder = outputfoldervar.get()
    ticker_name = stocknamevar.get()
    period = periodvar.get()
    interval = intervalvar.get()


    #save data to excel
    df.to_excel(output_folder+"/"+ticker_name+" - Interval = "+interval+" - Period = "+period+".xlsx")


#create GUI
#root
root = Tk()
root.title("Stock Overview App")
root.geometry("850x850")


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
location = ttk.Entry(content, textvariable=outputfoldervar, width=50)
submit = ttk.Button(content, text="Plot chart", command=draw_chart)
save = ttk.Button(content, text="Download data", command=save_df)


#layout
content.grid(column=0, row=0, pady=5, padx=100)
stock_label.grid(column=0, row=1, pady=5)
stock.grid(column=1, row=1, pady=5)
period_label.grid(column=0, row=2, pady=5)
period.grid(column=1, row=2, pady=5)
interval_label.grid(column=0, row=3, pady=5)
interval.grid(column=1, row=3, pady=5)
submit.grid(column=1, row=4, padx=10, pady=10)
browse_label.grid(column=0, row=5, pady=5)
location.grid(column=1, row=5, pady=5)
browse.grid(column=2, row=5, pady=5)
save.grid(column=3, row=5, padx=10, pady=10)

root.mainloop()


