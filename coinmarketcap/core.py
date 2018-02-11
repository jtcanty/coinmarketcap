#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import requests
import json
import logging
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

MARKET_URL = 'https://api.coinmarketcap.com/v1/ticker/'

def main():
    '''Fetches and displays cryptocurrency prices from the 
       coinmarketcap API.
       
    '''
    opts = parse_args()
    
    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        
    market = Market()
    
    if os.path.exists(opts.data_file):
        with open(opts.data_file) as fp:
            market.load_from_file(fp)       
    else:
        market.load_from_url(opts.market_url, save_as_file=opts.data_file)
        
    if opts.plot_file:
        generate_plot(opts.market_data, opts.plot_file)       
    if opts.csv_file:
        generate_csv(opts.data_file, opts.csv_file)
        
                                                             
def parse_args():
    '''Parse arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-file', default=os.path.join(os.path.dirname(__file__),
                                       'market_data.txt'),                                     
                        help='Path to the file containing the' 
                             'market data from CoinMarketCap (or target file if it' 
                             'needs to be downloaded')    
    parser.add_argument('--debug', default=False, action='store_true',
                        help='Increases the output level.')
    parser.add_argument('--market-url', default=MARKET_URL,
                        help='URL which should be used as market data source')
    parser.add_argument('--csv-file', 
                        help='Path to the file that includes the' 
                             'data output')
    parser.add_argument('--plot-file', 
                        help='Path to the file that includes a plot of the' 
                             'the data output')
    parser.add_argument('--market-data', 
                       help='Specified market data to plot')
                       
    parser.add_argument('--limit', type=int, default=10,
                        help='Lowest rank of currencies to be considered' )
    opts = parser.parse_args() 
    return opts
    
    
def generate_csv(data_file, output_file):
    '''Writes the given market data into CSV file specified
       by the output_file parameter. 
       
    '''
    with open(data_file) as fp:
        data = pd.read_json(fp)
        data.to_csv(output_file, sep='\t', encoding='utf-8')
    

def generate_plot(self, market_data, output_file):
    ''' Generates a bar plot for the specified currency data and
        outputs the plot into a saved PNG image.
        
    '''   
    # Generate the labels (x-axis) and values (y-axis) 
    # of the bar plots
    labels = []
    values = []
    for currency in market_data:
        labels.append(currency)
        values.append(market_data[currency])
     
    ind = np.arange(len(values))
    width = 0.3
    
    fig = plt.figure(figsize=(len(labels) * 2, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(ind, values, width, align='center')
    
    # Generate bar plot and format it
    plt.ylabel('Price (USD)')
    plt.xlabel('Currency')
    ax.set_xticks(ind + 0.3)
    ax.set_xticklabels(labels)
    fig.autofmt_xdate()
    plt.grid(True)
    plt.savefig(output_file, dpi=72)
    

class Market(object):
    '''Primary wrapper object for the CoinMarketCap.
       API.
    
    '''
    def __init__(self,
                 start=0,
                 limit=10):
        
        self.start = start
        self.limit = limit
        self.market_cap_usd = {}
        self.price_usd = {}
        self.price_btc = {}
        self.daily_volume_usd = {}
        self.volume_24h_usd = {}
        self.percent_change_7d = {}
        self.available_supply = {}
        self.total_supply = {}
        self.max_supply = {}
        self.percent_change_1h = {}
        self.percent_change_24h = {}
        self.percent_change_7d = {}
        
        
    def load_from_url(self, url, save_as_file=None):
        ''' 
        Loads data from a given URL. Data is saved into
        a file. This file can be fetched later.

        '''
        fp = requests.get(url, stream=True,
                          headers={'Accept-Encoding': None}).raw

        if save_as_file is None:
            return self.load_from_file(fp)

        else:
            with open(save_as_file, 'wb+') as out:
                while True:
                    buffer = fp.read(81920)
                    if not buffer:
                        break
                    out.write(buffer)
            with open(save_as_file) as fp:
                return self.load_from_file(fp)


    def load_from_file(self, fp):
        '''
        Loads data from the created file object.

        '''
        data = json.load(fp) 
        for line in range(self.start, self.limit):
            currency = data[line]

            # Save currency name 
            name = currency['id']

            # Current market cap
            self.market_cap_usd[name] = currency['market_cap_usd']

            # Price in USD
            self.price_usd[name] = currency['price_usd']
            
            # Price in BTC
            self.price_btc[name] = currency['price_btc']
            
            # Current daily volume
            self.volume_24h_usd[name] = currency['24h_volume_usd']

            # Current 7 day price change
            self.percent_change_7d[name] = currency['percent_change_7d']
            
            # Available supply
            self.available_supply[name] = currency['available_supply']
            
            # Total supply
            self.total_supply[name] = currency['total_supply']
            
            # Maximum supply
            self.max_supply[name] = currency['max_supply']
            
            # Percent change 1 hour
            self.percent_change_1h[name] = currency['percent_change_1h']
            
            # Percent change 24 hour
            self.percent_change_24h[name] = currency['percent_change_24h']
            
            # Percent change 7 day
            self.percent_change_7d[name] = currency['percent_change_7d']

            
if __name__ == '__main__':
    main()
            
        

            
        