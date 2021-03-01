import json
import requests
import sys
import tkinter as tk
colours = ["white","green","blue","purple","pink","yellow","brown","red","orange","grey","teal","lime","hot pink","magenta","black"]
FAVOURITES ={}
ids = {}
stopcode = {}
buses = []
TIMES = []
FAVES=[]
DELETES =[]
P =10
def load():
    
    try:
        op = open("Faves.txt","r")
        global f
        f=json.loads(op.read())
    except FileNotFoundError:
        f = {}
    try:
        Q = open("Colour.txt","r")
        global C_Colour
        C_Colour = Q.read()
    except FileNotFoundError:
        C_Colour = "grey"
    
load()

    
def query(inp,ids):
    url = "https://api.tfl.gov.uk/StopPoint/Search?query={}".format(inp)
    response = requests.get(url)
    data = json.loads(response.text)
    response = str(response) 
    if response != "<Response [200]>":
        t1 =("Bad request")
        a.config(text = t1)
    else:
        if len(data["matches"]) ==0:
            t1 = "Couldn't find stop try not mispelling words"
            a.config(text = t1)
        else:
            z = 0
            try:
                for i in data["matches"]:
                    m = str(data["matches"][z]["id"])
                    if m[3] != "G" or len(m) !=12:
                        z = z + 1
                        continue
                    for x in data["matches"][z]:
                        d = data["matches"][z]["id"]
                        name = data["matches"][z]["name"]
                        ids[name]=d
        
                    d = data["matches"][z]["id"]
                    name = data["matches"][z]["name"]
                    z= z + 1
                    ids[name]=d
            except KeyError:
                a.config(text = "Sorry no matches")
            STOPS(ids,100,130,{})


def STOPS(ids,COUNT,Y,stopcode):
    for b in buses:
        b.destroy()
    A = 0
    for i in ids:
        ur = "https://api.tfl.gov.uk/StopPoint/{}".format(ids[i])
        respons = requests.get(ur)
        dat = json.loads(respons.text)
        try:
            for x in dat["children"]:
                if A > len(dat["children"])-1:
                    A = 0
                    continue
            
                na =  dat["children"][A]["commonName"]
                stop= dat["children"][A]["stopLetter"]
                if "->" in stop:
                    A = A + 1
                    continue
                if len(na)> 10:
                    na = na[0:10]
                STOPS = ("{} ({})").format(na,stop)
                idd = dat["children"][A]["id"]
                stopcode[idd] = STOPS
                A = A + 1
        except KeyError:
            A = A + 1 
            continue
            if len(stop) > 2:
                A= A + 1
                continue
    for i in stopcode:
        if COUNT > 1100:
            Y = Y +40
            COUNT = 100
        button = tk.Button(master = window , text = stopcode[i] , command = lambda  x=i: times(x,100,500,stopcode,False,P),bg="orange",fg="blue")
        button.config(font=("Courier",13,"bold"))
        PLUS=(len(stopcode[i])*13)+10
        buses.append(button)
        button.place(x=COUNT,y=Y)
        COUNT = COUNT + PLUS 
        
    a.config(text = "Click the stop you would like times for below")
    
def times(ia,COUNT,Y,ids,FROM,P):
    if FROM == True:
        for B in buses:
            B.destroy()
    for d in DELETES:
        d.destroy()
    for m in FAVES:
        m.destroy()
    for i in TIMES:
        i.destroy()
    n = 0 
    url2 = "https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(ia)
    response2 = requests.get(url2)
    data2 = json.loads(response2.text)
    lists = []
    try:
        if len(data2) == 0:
            a.config(text="No times for that station")
        while n<= len(data2) - 1:
            names = data2[n]["lineId"]
            time=data2[n]["timeToStation"]
            time = int(int(time)/60)
            if time < 1:
                time = "DUE"
            p = (("{} : {} min ").format(names,str(time)))
            lists.append(p)
            n = n + 1 
    except KeyError:
        n = n + 1
        a.config(text = "That stop has not avaiable times")
        
    for i in lists:
        timee = tk.Label(master = window , text =  i  ,bg="green",fg="Black")
        if COUNT > 1100:
            Y = Y +40
            COUNT = 100
        if Y > 800:
            for i in TIMES:
                i.destroy()
            COUNT = 0
            Y = 600
        timee.config(font=("Courier",12,"bold"))    
        timee.place(x=COUNT,y=Y)
        TIMES.append(timee)
        COUNT = COUNT + (len(i)*10)+10    
    if FROM == False:
        FAV = tk.Button(master = window ,text = "Favourite",bg="yellow",fg="Black",command = lambda :fav(ia,ids[ia],P,ids,FROM))
        FAV.place(x=100,y=450)    
        FAVES.append(FAV)
    if FROM == True:
        DELETE = tk.Button(master = window , text = "Delete",bg="red",command= lambda:fav(ia,0,P,ids,FROM))
        DELETE.place(x=COUNT +50,y =Y)
        DELETES.append(DELETE)                               
    
def fav(i,c,P,ids,FROM):
    if FROM == True:
        for W in f:
            if i == f[W]:
                f.pop(W)
                FAVOURITES[i].destroy()
                FAVOURITES.pop(i)
                o = open("Faves.txt","w")
                o.write(json.dumps(f))
                o.close()
                break
    if FROM == False:
        if c not in f:
            f[c]=i
            o = open("Faves.txt","w")
            o.write(json.dumps(f))
            o.close()
            a.config(text=("You have added {} to your favourites").format(c))
            if len(f) == 0:
                fa=("You do not have any favourites")
            
            else:
                P = P + 50 
                F_B = tk.Button(master = window , text = c , command = lambda x= c:times(f[c],100,150,ids,True,P))
                F_B.place(y=P)
                FAVOURITES[i]=F_B
        else:
            a.config(text="Already in Favourites")
        
def s():
    o = searc.get()
    searc.delete(0,len(o))
    DEL()
    if len(o) < 5 :
        a.config(text = "No results")
    if o.isspace()==True or len(o) ==0:
        T = ("Couldn't find Stop try not mispelling words")
        a.config(text=T)
    else:
        query(o.lower(),{})
        
def DEL():
    for i in buses:
        i.destroy()
    for b in FAVES:
        b.destroy()
    for x in TIMES :
        x.destroy()
    for d in DELETES:
        d.destroy()
t2 = "Welcome to my bus App , you will need an active internet connection"
t1 = "Enter what stop you want to search:"




def EXIT():
    window.destroy()
    sys.exit()
def load_fav(P):
    for b in buses:
        b.destroy()
    if len(f) == 0:
        fa=("You do not have any favourites")
    else:
        fa=("Favourites:")
        for i in f:
            P = P + 50 
            FAV_BUTTONS = tk.Button(master = window , text = i , command = lambda x=f[i]:times(x,100,150,stopcode,True,P))
            FAV_BUTTONS.place(x=0,y=P)
            FAVOURITES[f[i]]=FAV_BUTTONS
        return P   
    faves = tk.Label(text=fa)
    faves.place(y=35)
    return P

def colour_change(colour):
    if colour in colours:
        window.config(bg=colour)
    O = open("Colour.txt","w")
    O.truncate(0)
    O.write(colour)
    O.close()
def COLOURS():
    Y = 40
    for COLOUR in colours:
        if COLOUR == "black":
            C_Label = tk.Button(master = window , text = "Black" ,fg="White", bg = COLOUR ,command  = lambda x = COLOUR:colour_change(x))
            C_Label.place(x=1300,y=Y)
            Y = Y +40
        else:
            C_Label = tk.Button(master = window , text = COLOUR , bg = COLOUR ,command  = lambda x = COLOUR:colour_change(x))
            C_Label.place(x=1300,y=Y)
            Y = Y +40
try:
    window = tk.Tk()
    window.title("Bus Times")
    window.attributes("-fullscreen",True)
    window.config(bg=C_Colour)
    a = tk.Label(text=t1)
    a.config(font=("Century Gothic",20))
    searc = tk.Entry(master = window,font=("Courier",15))
    b = tk.Button(text="ENTER",command = s)
    greeting = tk.Label(text=t2)
    greeting.config(font=("Century Gothic",18))
    greeting.pack(side=tk.TOP)
    a.pack()
    F_Label = tk.Label(master = window , text = "Favourites:", bg = "Yellow")
    F_Label.config(font=("Century Gothic",15))
    F_Label.place(x=5,y=2)
    exit_button = tk.Button(master = window , text = "EXIT",command=EXIT,bg= "red")
    exit_button.config(font=("Century Gothic",12))
    exit_button.place(x=1300)
    b.place(x=230,y=85)
    searc.place(x=280,y=85)
    search = searc.get()
    P = load_fav(P)
    COLOURS()
    window.mainloop()
except (requests.ConnectionError, requests.Timeout) as exception:
    a.config(text = "No connection , please recconect and exit")
    


