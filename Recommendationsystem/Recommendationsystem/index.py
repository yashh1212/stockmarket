from django.http import HttpResponse
from django.shortcuts import render
import pymysql
mydb=pymysql.connect(host="localhost", user="Endeavour", password="aspire", database="stockmarket")
def page1(request):
    return render(request,"page1.html")
def register(request):
    return render(request,"NewRegistration.html")
def login(request):
    name=request.POST.get('name')
    contact=request.POST.get('cnumber')
    email=request.POST.get('email')
    password=request.POST.get('pass')
    cur=mydb.cursor()
    sql="insert into userdata(Name,Contact,Email,Password)values(%s,%s,%s,%s)";
    values=(name,contact,email,password)
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"page1.html")
def userlogin(request):
    sql="select * from userdata";
    cur1=mydb.cursor()
    cur1.execute(sql)
    data=cur1.fetchall()
    email=request.POST.get('email')
    password=request.POST.get('pass')
    print(email)
    print(password)
    print("111111111111111", data)
    ispresent=False
    uid=""
    uname=""
    if(email=="admin" and password=="admin"):
        return render(request,"AdminDashboard.html")
    else:
        for x in data:
            if(x[3]==email and x[4]==password):
                uid=x[0]
                uname=x[1]
                ispresent=True;
    if(ispresent):
        request.session['uid'] =uid
        request.session['uname'] =uname
        return render(request,"UserDashboard.html")
    else:
        result="Invalid Username or Password"
        return render(request,"page1.html",{'data':result})
        
        
            
    print(ispresent)
