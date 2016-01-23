# -*- coding: utf-8 -*-
'''
authored by albert zhao
NJU dislab
'''
import sys;
import os;
import tushare as tu;
import time;
from sklearn import tree;
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from util import *
ONE_DAY = 86400;
BACKWARD = 50;
STOCK = '600895'
OPEN_PRICE = 20

def get_time_interval( end, interval):
    if not isinstance(interval, int):
        print('ERROR in get_time_interval(): argument \'interval\' not int')
        exit(1)
    start = time.strftime('%Y-%m-%d', time.localtime( end-interval*ONE_DAY))
    end = time.strftime('%Y-%m-%d', time.localtime( end))
    return ( start, end)
    
if __name__ == "__main__":
    start_d, end_d = get_time_interval(time.time()-ONE_DAY,BACKWARD)
    
    if len(sys.argv)%2 !=1:
        print 'Format1:\npython stockPredictor -n STOCK_num -o OPEN_PRICE [-d BACKWARD_DAYS]'
        exit(0)
    flag = 0
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-n' and flag ==0:
            STOCK = sys.argv[i+1]
            flag =1
        elif sys.argv[i] == '-o' and flag ==0:
            OPEN_PRICE = float(sys.argv[i+1])
            flag = 1
        elif sys.argv[i] == '-d' and flag ==0:
            BACKWARD = int( sys.argv[i+1])
            flag = 1
        elif flag == 1:
            flag = 0
            continue
        else:
            print 'Format2:\npython stockPredictor -n STOCK_num -o OPEN_PRICE [-d BACKWARD_DAYS]'
            exit(0)
    print start_d," ",end_d,'\n',BACKWARD,'days'
    path = '/home/albert/Documents/CODE/SCRIPT/DIY_Utilities/stock_predictor/data/'+ STOCK+'.pkl'
    if os.path.isfile( path):
        stock150153 = pd.load( path)
        if Need_Update.need_update( stock150153.index[0]):
            print "hooking and saving data of "+STOCK
            stock150153 = tu.get_hist_data( STOCK)
            stock150153.save( path)
        else:
            print "loading data of "+STOCK
    else:
        print "hooking and saving data of "+STOCK
        stock150153 = tu.get_hist_data( STOCK)
        stock150153.save( path)
        
    training_data = stock150153[0:BACKWARD][::-1]
    model_high = tree.DecisionTreeRegressor()
    model_low = tree.DecisionTreeRegressor()
    ens_model_high = RandomForestRegressor()
    ens_model_low = RandomForestRegressor()
    label_high = training_data['high'].as_matrix()
    label_low = training_data['low'].as_matrix()
    del training_data['high']
    del training_data['price_change']
    del training_data['p_change']
    del training_data['close']
    del training_data['low']
    #del training_data['volume']
    matrix = training_data.as_matrix()
    
    model_high.fit(matrix,label_high)
    model_low.fit(matrix, label_low)
    ens_model_high.fit(matrix, label_high)
    ens_model_low.fit(matrix,label_low)
    
    test_data = stock150153[0:1]
    print 'It\'s',time.strftime('%m-%d,%A',time.localtime(time.time())),'today'
    del test_data['high']
    del test_data['price_change']
    del test_data['p_change']
    del test_data['close']
    del test_data['low']
    #del test_data['volume']
    test_matrix = test_data.as_matrix()
    test_matrix[0,0] = OPEN_PRICE # todey's open price
    
    print stock150153.head(1)
    print model_high.score(matrix, label_high), ens_model_high.score(matrix, label_high)
    print model_high.predict(test_matrix),'as high price', ens_model_high.predict(test_matrix)
    print model_low.predict( test_matrix),'as low price',ens_model_low.predict(test_matrix)
    print 'Done'