from django.http import HttpResponse
from django.shortcuts import render
import pymysql
from datetime import date
import yfinance as yf
from yahoo_fin import stock_info
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm
import quandl
import json
import numpy as np
import requests
mydb=pymysql.connect(host="localhost",user="Endeavour",password="aspire",database="stockmarket")


def livestock(request):
    return render(request,"LiveStock.html")


def logout(request):
    return render(request,"page1.html")
def userhome(request):
    return render(request,"UserDashboard.html")

def stockpred(request):
    return render(request,"Prediction.html")
def logout(request):
    return render(request,"page1.html")
def mywatchlist(request):
    uid=request.session['uid']
    sql="select * from mywatchlist";
    cur1=mydb.cursor()
    cur1.execute(sql)
    result=cur1.fetchall()
    payload = []
    content={}
    #json=jsonify(result)
    for row in result:
        
            content = {'stockname': row[3]}
            payload.append(content)
            content = {}
    print(f"json: {json.dumps(payload)}")
    return render(request,"MyWatchlist.html", {'list': {'items':payload}})
def mysearches(request):
    uid=request.session['uid']
    sql="select * from mysearches";
    cur1=mydb.cursor()
    cur1.execute(sql)
    result=cur1.fetchall()
    payload = []
    content={}
    #json=jsonify(result)
    for row in result:
        
            content = {'stockname': row[3], 'stockvalue': row[4], 'datetime': row[5]}
            payload.append(content)
            content = {}
    print(f"json: {json.dumps(payload)}")
    return render(request,"MySearches.html", {'list': {'items':payload}})
def predict(request):
    # Quandl API key. Create your own key via registering at quandl.com
    quandl.ApiConfig.api_key = "RHVBxuQQR_xxy8SPBDGV"
    # Getting input from Templates for ticker_value and number_of_days
    ticker_value = request.POST.get('ticker')
    number_of_days = request.POST.get('days')
    number_of_days = int(number_of_days)
    # Fetching ticker values from Quandl API 
    df = quandl.get("WIKI/"+ticker_value+"")
    df = df[['Adj. Close']]
    print(df)
    forecast_out = int(number_of_days)
    df['Prediction'] = df[['Adj. Close']].shift(-forecast_out)
    # Splitting data for Test and Train
    X = np.array(df.drop(['Prediction'], axis=1))
    X = preprocessing.scale(X)
    X_forecast = X[-forecast_out:]
    X = X[:-forecast_out]
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.2)
    # Applying Linear Regression
    clf = LinearRegression()
    clf.fit(X_train,y_train)
    # Prediction Score
    confidence = clf.score(X_test, y_test)
    # Predicting for 'n' days stock data
    forecast_prediction = clf.predict(X_forecast)
    forecast = forecast_prediction.tolist()
    return render(request,'Prediction.html',{'confidence' : confidence,'forecast': forecast,'ticker_value':ticker_value,'number_of_days':number_of_days})


def getstock(request):
    start_date = request.POST.get('from')
    end_date = request.POST.get('to')
    stockname = request.POST.get('stockname')

    request.session['start_date']=start_date
    request.session['end_date']=end_date
    request.session['stockname']=stockname
    
    ticker = stockname
    data1 = yf.download(ticker, start_date, end_date)
    json_records = data1.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    print(data)
    context = {'d': data}
    print(data1['Low'].min())
    print(data1['High'].max())
    return render(request,"ViewStockHistory.html",context)

def dateprediction(request):
    start_date=request.session['start_date']
    end_date=request.session['end_date']
    stockname=request.session['stockname']
    ticker = stockname
    data1 = yf.download(ticker, start_date, end_date)
    json_records = data1.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    #print(name)
    return render(request,"ViewStockHistory.html")


def addwatchlist(request):
    uid=request.session['uid']
    uname=request.session['uname']
    stock=request.session['stockname']
    sql="insert into mywatchlist(stockname,uid,uname)values(%s,%s,%s)";
    values=(stock,uid,uname)
    cur=mydb.cursor()
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"ViewStockHistory.html")


def getcurrentstock(request):
    uid=request.session['uid']
    print(type(uid))
    uname=request.session['uname']
    stockname=request.POST.get('title')
    request.session['stockname']=stockname
    
    stock=stock_info.get_live_price(stockname)
    today = date.today()
    context = {
        "stock" : stock,
        "stockname"  : stockname,
        "today"  : today,
    }
    sql="insert into mysearches(uid,uname,stockname,stockvalue,dtime)values(%s,%s,%s,%s,%s)";
    values=(uid,uname,stockname,str(stock),str(today))
    cur=mydb.cursor()
    cur.execute(sql,values)
    mydb.commit()
   # print(stock)
    return render(request,"GetStockTodays.html",context)
    
