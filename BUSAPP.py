import json
import requests
import sys
import tkinter as tk
import winsound
colours = ["white","green","blue","purple","pink","yellow","brown","red","orange","grey","teal","lime","hot pink","magenta","black"]
FAVOURITES ={}
ids = {}
stopcode = {}
buses = []
TIMES = []
FAVES=[]
DELETES =[]
P =10
SET_ACTIVE = False
def load():
    
    try:
        op = open("Faves.txt","r")
        global f
        f=json.loads(op.read())
    except FileNotFoundError:
        f = {}
    try:
        S = open("Settings.txt","r")
        global Settings
        Settings = json.loads(S.read())
    except (FileNotFoundError , json.decoder.JSONDecodeError):
        
        Settings = {"volume":"500","bg_colour":"orange","text_colour":"grey","bus_colour":"orange","sound":"F","time_colour":"green"}
        
    
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
            STOPS(ids,100,130,{},Settings["bus_colour"])


def STOPS(ids,COUNT,Y,stopcode,Colour):
    High = 0 
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
        button = tk.Button(master = window , text = stopcode[i] , command = lambda  x=i: times(x,100,500,stopcode,False,P,Settings["time_colour"]),bg=Colour,fg="blue")
        button.config(font=("Courier",13,"bold"))
        PLUS=(len(stopcode[i])*13)+10
        buses.append(button)
        button.place(x=COUNT,y=Y)
        COUNT = COUNT + PLUS 
        
    a.config(text = "Click the stop you would like times for below")
    
def times(ia,COUNT,Y,ids,FROM,P,colour):
    beep()
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
        timee = tk.Label(master = window , text =  i  ,bg=colour,fg="Black")
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
        REFRESH = tk.Button(master = window , text = "Refresh",bg="lime",command = lambda:times(ia,100,500,stopcode,False,P,colour))
        FAVES.append(REFRESH)
        REFRESH.place(x=180,y=450)
    if FROM == True:
        DELETE = tk.Button(master = window , text = "Delete",bg="red",command= lambda:fav(ia,0,P,ids,FROM))
        DELETE.place(x=COUNT +50,y =Y)
        DELETES.append(DELETE)                               
        REFRESH = tk.Button(master = window , text = "Refresh",bg="lime",command = lambda:times(ia,100,150,stopcode,True,P,colour))
        DELETES.append(REFRESH)
        REFRESH.place(x=COUNT +100,y=Y)
def fav(i,c,P,ids,FROM):
    if FROM == True:
        for L in DELETES:
            L.destroy()
        for T in TIMES:
            T.destroy()
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
                pass            
            else:
                P = P + 50 
                F_B = tk.Button(master = window , text = c , command = lambda x= c:times(f[c],100,150,ids,True,P))
                F_B.place(y=P)
                FAVOURITES[i]=F_B
        else:
            a.config(text="Already in Favourites")
        
def s():
    beep()
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
t1 = "Enter what stop you want to search by tying your search in the entry box below then pressing the 'ENTER' button or Enter on your keyboard:"

def beep():
    if Settings["sound"] == "T":
    
        volume = int(Settings["volume"])
        # Set Duration To 1000 ms == 1 second
        winsound.Beep(volume,68)
def sound_on():
    beep()
    S = open("Settings.txt","w")
    S.truncate(0)
    Settings["sound"] = "T"
    S.write(json.dumps(Settings))
    S.close()
def sound_off():
    beep()
    S = open("Settings.txt","w")
    S.truncate(0)
    Settings["sound"] = "F"
    S.write(json.dumps(Settings))
    S.close()
def colour_load(y,TYPE):
    x= 10 
    for COLOUR in colours:
        if COLOUR == "black":
            C_Label = tk.Button(master = SET , text = "Black" ,fg="White", bg = COLOUR ,command  = lambda Z = COLOUR,X =TYPE :colour_change(Z,X))
            C_Label.place(x=x,y=y)
            x= x + (len("black")*8)
        else:
            C_Label = tk.Button(master = SET , text = COLOUR , bg = COLOUR ,command  = lambda Z = COLOUR,X=TYPE:colour_change(Z,X))
            C_Label.place(x=x,y=y)
            x= x + (len(COLOUR)*8)
def settings():
    global SET_ACTIVE
    SET_ACTIVE = True
    beep()
    global SET
    SET = tk.Tk() 
    SET.title("Settings")
    SET.geometry("700x500")
    SET.protocol("WM_DELETE_WINDOW", s_EXIT)
    SET.attributes("-toolwindow",True)
    SET.config(bg=Settings["bg_colour"])
    EXIT_button = tk.Button(master = SET, text ="EXIT",bg="Red",command =s_EXIT)
    EXIT_button.place(x=630)
    EXIT_button.config(font=("Century Gothic",15,"bold"))
    colour_label = tk.Label(master = SET , text = "Colour of background:",bg = "Grey")
    colour_label.place(x=0,y=0)
    colour_load(30,"win")
    Times_label = tk.Label(master = SET , text = "Colour of menu text :",bg="grey")
    Times_label.place(x=0,y=110)
    colour_load(130,"text")
    Bus_Label = tk.Label(master = SET ,text = "Colour of stop buttons:", bg  = "grey")
    Bus_Label.place(x=0,y=160)
    colour_load(190,"bus")
    Times_Label = tk.Label(master = SET , text = "Colour of stop times:" , bg = "grey")
    Times_Label.place(x=0,y=220)
    colour_load(250,"time")
    Sound_label = tk.Label(master = SET , text = "Sound:",bg = "grey")
    Sound_label.place(x=0,y=60)
    ON = tk.Button(master = SET , text = "ON",bg="green",command = sound_on)
    OFF = tk.Button(master = SET , text = "OFF",bg="red",command = sound_off)
    ON.place(x=0,y=83)
    OFF.place(x=30,y=83)
    SET.mainloop()

def m_EXIT():
    beep()
    window.destroy()
    if SET_ACTIVE == True:
        SET.destroy()
    sys.exit()
def s_EXIT():
    beep()
    SET.destroy()
    global SET_ACTIVE
    SET_ACTIVE = False
def load_fav(P):
    for b in buses:
        b.destroy()
    if len(f) == 0:
        fa=("You do not have any favourites")
    else:
        fa=("Favourites:")
        for i in f:
            P = P + 50 
            FAV_BUTTONS = tk.Button(master = window , text = i , command = lambda x=f[i]:times(x,100,150,stopcode,True,P,Settings["time_colour"]))
            FAV_BUTTONS.place(x=0,y=P)
            FAVOURITES[f[i]]=FAV_BUTTONS
        return P   
    faves = tk.Label(text=fa)
    faves.place(y=35)
    return P

def colour_change(colour,Type):
    beep()
    if Type == "win":
        window.config(bg=colour)
        SET.config(bg=colour)
        global Settings
        Settings["bg_colour"] = colour
    if Type == "text":
        a.config(bg=colour)
        greeting.config(bg=colour)
        Settings["text_colour"] = colour
    if Type == "bus":
        Settings["bus_colour"] = colour
    if Type == "time":
        Settings["time_colour"] = colour
    O = open("Settings.txt","w")
    O.truncate(0)
    O.write(json.dumps(Settings))
    
    O.close()
def key_press(event):
    Key = event.keycode
    if Key == 13:
        s()

try:
    window = tk.Tk()
    window.title("Bus Times")
    window.attributes("-fullscreen",True)
    window.config(bg=Settings["bg_colour"])                     
    a = tk.Label(master = window,text=t1,bg=Settings["text_colour"])
    a.config(font=("Century Gothic",13))
    searc = tk.Entry(master = window,font=("Courier",15))
    b = tk.Button(master=window,text="ENTER",command = s)
    greeting = tk.Label(master = window,text=t2,bg=Settings["text_colour"])
    greeting.config(font=("Century Gothic",18))
    greeting.pack(side=tk.TOP)
    a.pack()
    F_Label = tk.Label(master = window , text = "Favourites:", bg = "Yellow")
    F_Label.config(font=("Century Gothic",15))
    F_Label.place(x=0,y=2)
    exit_button = tk.Button(master = window , text = "EXIT",command=m_EXIT,bg= "red")
    exit_button.config(font=("Century Gothic",12))
    exit_button.place(x=1300)
    setting_button = tk.Button(master = window , text = "SETTINGS",command = settings,bg="Blue")
    setting_button.place(x=1200)
    setting_button.config(font=("Century Gothic",13,"bold"))
    b.place(x=230,y=85)
    searc.place(x=280,y=85)
    search = searc.get()
    P = load_fav(P)
    window.bind("<Key>",key_press)
    window.mainloop()
except (requests.ConnectionError, requests.Timeout) as exception:
    a.config(text = "No connection , please recconect and exit")
    


