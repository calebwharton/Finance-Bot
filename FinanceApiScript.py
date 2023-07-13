#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 17:28:02 2023

This is a programme that grabs data on certain stocks and reports if they have
increased or decreased by a certain amount. 

@author: calebwharton
"""

from yahoo_fin.stock_info import get_data
import pandas as pd

def main():
    research_stock = create_all_stock_files()
    make_stock_comparisons(research_stock)
    
def create_all_stock_files():
    sheet_name = "Sheet1"
    no_of_stocks = int(input("How many stocks would you like to compare: "))
    research_stock = create_stock_spreadsheet(sheet_name)
    for i in range(1, no_of_stocks):
        research_stock.new_ticker()
        research_stock.add_file()
        research_stock.get_api_data()
        research_stock.add_stock()
    return research_stock
           
def create_stock_spreadsheet(sheet_name):
    research_stock = get_ticker_data(sheet_name)
    research_stock.get_api_data()
    research_stock.add_stock()
    return research_stock
  
def get_ticker_data(sheet_name):
    ticker = input("Enter your stock's ticker: ")
    start_date = input("Enter the start date for your research (mm/dd/yyyy): " )
    end_date = input("Enter the end date for your research (mm/dd/yyyy): ")
    interval = input("Enter an Interval (Day = 1d, Week = 1wk, Month = 1mo): ")
    file_name = "./FinanceAPI_" + ticker + ".xlsx"
    return Stock(ticker, start_date, end_date, interval, file_name, sheet_name)

def make_stock_comparisons(research_stock):
    stock_comparison = Comparisons(research_stock.ticker_files, research_stock)
    which_comparison = input("Which comparison would you " +
                             "like to make? (% change, simulate): ")
    if which_comparison == "simulate":
        stock_comparison.simulate_investment()
class Comparisons:
    
    def __init__(self, ticker_files, research_stock):
        self.ticker_files = ticker_files
        self.research_stock = research_stock
    
    def __str__():
        return "This is a class which compares different stocks"
    
    def percentage_over_period(self):
        print()
    
    def simulate_investment(self):
        simulated_value = float(input("Enter the value you would like to simulate: "))
        start_end_price = self.research_stock.read_price_change()
        for i in range(len(start_end_price)):
            new_value = round(simulated_value / float(start_end_price[i][0])
                            * float(start_end_price[i][1]), 2)
            print(f"If you invested ${simulated_value} in " +
                  f" {self.research_stock.ticker_names[i]} on" +
                  f" {self.research_stock.start_date} you would have" +
                  f" ${new_value} on {self.research_stock.end_date}") 
        
class Stock:
    
    def __init__(self, ticker, start_date, end_date,
                 interval, file_name, sheet_name):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.ticker_files = [self.file_name]
        self.ticker_names = [self.ticker]
    
    def __str__(self):
        return "This is a stock of a company"

    def get_api_data(self):
        self.ticker_data =  dict(get_data(self.ticker, self.start_date,
                    self.end_date, False, self.interval))
    
    def add_stock(self):
        for key in self.ticker_data:
            self.ticker_data[key] = list(self.ticker_data[key])
        index_length = []
        for i in range(len(self.ticker_data["open"])):
            index_length.append(i + 1)

        df = pd.DataFrame(
            {
            "date" : self.ticker_data["date"],
            "open": self.ticker_data["open"],
            "high": self.ticker_data["high"],
            "low": self.ticker_data["low"],
            "close": self.ticker_data["close"],
            "adjclose": self.ticker_data["adjclose"],
            "volume": self.ticker_data["volume"],
            "ticker": self.ticker_data["ticker"]
            },
            index= index_length,
            columns=['date', 'open', 'high', 'low', 'close',
                     'adjclose', 'volume', 'ticker']
            )
        
        df.to_excel(self.file_name, self.sheet_name, index=True, header=True)
    
    def print_file(self):
        printed_file = pd.read_excel(self.file_name, self.sheet_name)
        for key in dict(printed_file):
            print(dict(printed_file[key]))
            
    def add_file(self):
        self.file_name = "./FinanceAPI_" + self.ticker + ".xlsx"
        self.ticker_files.append(self.file_name)
        self.ticker_names.append(self.ticker)
    
    def new_ticker(self):
        self.ticker = input("What is the ticker of this stock: ")
        
    def print_tickers(self):
        for ticker in self.ticker_names:
            print(ticker)
    
    def read_price_change(self):
        max_mins = []
        for file in self.ticker_files:
            read_file = pd.read_excel(file, self.sheet_name)
            adjusted_values = dict(read_file)["adjclose"]
            max_mins.append((adjusted_values[0],
                           adjusted_values[len(adjusted_values) - 1]))
        return max_mins
            

           

main()



