import json
import requests
import sys
print("Welcome to my bus App , you will need an active internet connection ")
try:
    op = open("Faves.txt","r")
    f=json.loads(op.read())
except FileNotFoundError:
    f = {}
def l():
    print("----------------------------------------------------------------")
    


def main(z,stopcode,ids):
    if len(f) == 0:
        print("You do not have any favourites")
        l()
    else:
        print("Favourites:")
        for i in f:
            print(i)
    l()        
    search = input("Enter what stop you want to search\nYou can also use a stop symbol from your favourites\nTo remove a favourite stop type 'delete'\n:")
    if search.isspace() == True:
        print("Couldn't find Stop try not mispelling words")
        l()
        main(z,stopcode,ids)
    if (search == "Delete" or search == "delete") and len(f) != 0:
        dele = str(input("Please enter the stop you want to remove from the stop\n:"))
        if dele in f:
            f.pop(dele)
            print(("{} deleted from favourties").format(dele))
            o = open("Faves.txt","w")
            o.write(json.dumps(f))
            o.close()
            l()
            main(z,stopcode,ids)
        else:
            main(z,stopcode,ids)
    if search in f:
        n=0
        u= "https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(f[search])
        respon = requests.get(u)
        da = json.loads(respon.text)
        lists = []
        while n<= len(da) - 1:
            names = da[n]["lineId"]
            time=da[n]["timeToStation"]
            time = int(int(time)/60)
            lists.append(names)
            if time < 1:
                time = "DUE"
            print(("{} : {} min").format(names,str(time)))
            l()
            n = n + 1
        main(z,stopcode,ids)
    if (search == "Delete" or search == "delete") and len(f) == 0:
        main(z,stopcode,ids)
    url = "https://api.tfl.gov.uk/StopPoint/Search?query={}{}".format(search,"&modes=bus")
    response = requests.get(url)
    data = json.loads(response.text)
    if len(data["matches"]) ==0:
        print("Couldn't find Stop try not mispelling words")
        main(z,stopcode,ids)
   
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

   
    a = 0
    for i in ids:
        ur = "https://api.tfl.gov.uk/StopPoint/{}".format(ids[i])
        respons = requests.get(ur)
        dat = json.loads(respons.text)
        for x in dat["children"]:
            if a > len(dat["children"])-1:
                a = 0
                continue
            try:
                na =  dat["children"][a]["commonName"]
                stop= dat["children"][a]["stopLetter"]
            except KeyError:
                continue
            if len(stop) > 2:
                a= a + 1
                continue
            idd = dat["children"][a]["id"]
            print(("{}  , {} ").format(na,stop))
            stopcode[stop] = idd
            l()
            a = a + 1       
    
    times(stopcode)
    
    
def times(stopcode):
    l()
    n=0
    choice = input("Please enter the Stop you want to find the times for by typing the symbol\nType 'Exit' or 'exit' to search places again\n:")
    if choice == "Exit" or choice == "exit":
        main(0,{},{})
    if choice not in stopcode:
        print("That's not a valid stop symbol please try again")
        times(stopcode)
    url2 = "https://api.tfl.gov.uk/StopPoint/{}/Arrivals".format(stopcode[choice])
    response2 = requests.get(url2)
    data2 = json.loads(response2.text)
    lists = []
    if len(data2) == 0:
        print("No times ")
        times(stopcode)
    while n<= len(data2) - 1:
        names = data2[n]["lineId"]
        time=data2[n]["timeToStation"]
        time = int(int(time)/60)
        lists.append(names)
        if time < 1:
            time = "DUE"
        print(("{} : {} min").format(names,str(time)))
        n = n + 1
        l()
        
    yn = input("Would you like to favourite this stop?\nPlease enter 'y' for yes \n:")
    if yn == 'y':
        fav(choice,stopcode[choice])
        times(stopcode)        
        
    times(stopcode)
def fav(i,c):
    f[i]=c
    o = open("Faves.txt","w")
    o.write(json.dumps(f))
    o.close()
    print(("You have added {} to your favourites").format(i))
    
    
try:    
    main(0,{},{})
except (requests.ConnectionError, requests.Timeout) as exception:
    print("No connection ,Exiting ...")
    sys.exit(3)
