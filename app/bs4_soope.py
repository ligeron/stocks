import pickle
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
from data_provider import *
from settings import *

style.use('ggplot')

def compile_data():
    main_df = get_stock_data_by_symbols(get_stock_symbols())
        
    print(main_df.tail())
    main_df.to_csv('sp500_joined_closses.csv')

def visualize_data():
    df = pd.read_csv('sp500_joined_closses.csv')
#    df['AAPL'].plot()
#    plt.show()
    df_corr = df.corr()
    print(df_corr.head())
    
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    heatmap = ax.pcolor(data,cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor = False)
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor = False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labeles = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabelels(column_labeles)
    ax.set_yticklabelels(row_labels)
    plt.xticks(rotation = 90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()

visualize_data()