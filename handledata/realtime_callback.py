import json
import pandas as pd
from collections import defaultdict

class RealtimeCallback:
    def __init__(self, plot_widget, stock):
        # Initialize a default dictionary to cache partial data for each URL
        self.data_cache = defaultdict(str)
        self.plot_widget = plot_widget
        # Dictionary to store DataFrames for each URL
        self.data_frames = defaultdict(lambda: pd.DataFrame(columns=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amount', 'VWAP']))
        self.stock = stock

    def callback(self, stock, data_str):
        stock = self.stock
        # Append new data to the cache
        if self.data_cache[stock.full_code] == "" or self.data_cache[stock.full_code] is None:
            self.data_cache[stock.full_code] = data_str[6:]
        else:
            self.data_cache[stock.full_code] += data_str

        while True:
            try:
                print(f"Parsing data for {stock.full_code}: {self.data_cache[stock.full_code]}")
                # Parse the cached data as a JSON object
                data = json.loads(self.data_cache[stock.full_code])
                # If successful, process the data and clear the cache
                self.process_data(stock, data)
                self.data_cache[stock.full_code] = ""
                break
            except json.JSONDecodeError as e:
                print(f"Data parsing error for {stock.full_code}: {e}")
                # Find the error position
                idx = e.pos
                if idx < len(self.data_cache[stock.full_code]):
                    # Split the cached data and keep the unparsed part
                    self.data_cache[stock.full_code] = self.data_cache[stock.full_code][idx:]
                else:
                    break

    def process_data(self, stock, data):
        if data['data'] is None or data['data'] == '':
            return
        # Extract trends data
        trends = data['data']['trends']

        # Process trends data, keeping the date-time and all other parts
        processed_data = []
        for trend in trends:
            parts = trend.split(',')
            processed_data.append(parts)

        # Create a temporary DataFrame with the new data
        temp_df = pd.DataFrame(processed_data, columns=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amount', 'VWAP'])
        
        # Append the new data to the persistent DataFrame for the specific stock.full_code
        self.data_frames[stock.full_code] = pd.concat([self.data_frames[stock.full_code], temp_df], ignore_index=True)
        
        # Plot the updated DataFrame
        self.plot_widget.plot(self.data_frames[stock.full_code], stock)