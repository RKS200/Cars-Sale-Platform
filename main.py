import pyrebase
import pickle
import csv

#Loading Data from the configration file.
file = open("Data.pyrebaseConfig","rb")
config = {}
config = pickle.load(file)
file.close()

#Creating database object.
firebase = pyrebase.initialize_app(config)
db = firebase.database()


a = False

#Functions.........
def insert():
    name = input("Enter the Car in the format 'Brand Model': ")
    year = int(input("Enter the Manufractured Year: "))
    price = int(input("Enter your price: "))
    adv = []
    while True:
        adv.append(input('Say What is working(One by One):'))
        if input('Do you Want to Enter More?(y/n): ') in 'Nn':
            break
    dadv = []
    while True:
        dadv.append(input('Say What is Not working(One by One):'))
        if input('Do you Want to Enter More?(y/n): ') in 'Nn':
            break
    path = "Cars/"+name+"/"
    data = {path:{"year":year,"price":price,"adv":adv,"dadv":dadv}}
    db.update(data)
    print("Data Successfully Inserted!")

def lists():
    all_users = db.child("Cars").get()
    print("***List of Cars***")
    for user in all_users.each():
        print('*',user.key())
    print("\n\nListing Done.....")
        
def remove():
    name = input("Enter the Name: ")
    all_users = db.child("Cars").get()
    for user in all_users.each():
        if(name == user.key()):
            db.child("Cars").child(name).remove()
            print("Car: ",name," removed Successfully!")
            a = True
            break
        else:
            a = False
            continue
    if a == False:
        print("Name does not exists!")
        
def show():
    name = input("Enter the Name: ")
    all_users = db.child("Cars").get()
    for user in all_users.each():
        if(name == user.key()):
            print("Car found!....Showing Data")
            name = user.key()
            data = user.val()
            year = data['year']
            price = data['price']
            adv = data['adv']
            dadv = data['dadv']
            print("\nName: ",name,"\nYear: ",year,"\nPrice: ",price)
            print('What is Working:')
            for i in adv:
                print('*',i)
            print('What is not Working:')
            for i in dadv:
                print('*',i)
            a = True
            break
        else:
            a = False
            continue
    if a == False:
        print("Name does not exists!")

def update():
    name = input("Enter the Name: ")
    all_users = db.child("Cars").get()
    for user in all_users.each():
        if(name == user.key()):
            year = int(input("Enter the Manufractured Year: "))
            price = int(input("Enter your price: "))
            adv = []
            while True:
                adv.append(input('Say What is working(One by One):'))
                if input('Do you Want to Enter More?(y/n): ') in 'Nn':
                    break
            dadv = []
            while True:
                dadv.append(input('Say What is Not working(One by One):'))
                if input('Do you Want to Enter More?(y/n): ') in 'Nn':
                    break
            path = "Cars/"+name+"/"
            data = {path:{"year":year,"price":price,"adv":adv,"dadv":dadv}}
            db.update(data)
            print("Data Successfully Updated!")
            a = True
            break
        else:
            a = False
            continue
    if a == False:
        print("Name does not exists!")
        
def Exportcsv():
    fields = ['Name','Year','Price','What is Working','What is not Working']
    rows = []
    all_users = db.child("Cars").get()
    for user in all_users.each():
        temp = []
        data = user.val()
        adv = data['adv']
        dadv = data['dadv']
        advstr = ''
        for i in adv:
            advstr += i+','
        dadvstr = ''
        for i in dadv:
            dadvstr += i+','
        temp = [user.key(),data['year'],data['price'],advstr,dadvstr]
        rows.append(temp)
    with open("ExportedFile.csv",'w',newline = '\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    print("Data Successfully Exported as .csv!")

def Importcsv():
    fields = []
    rows = []
    with open("ImportFile.csv","r") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
        print("Data imported from .csv file and now Uploading.......")
        for i in rows:
            name = i[0]
            year = i[1]
            price = i[2]
            adv = i[3].strip(',').split(',')
            dadv = i[4].strip(',').split(',')
            path = "Cars/"+name+"/"
            data = {path:{"year":year,"price":price,"adv":adv,"dadv":dadv}}
            db.update(data)
        print("Data Uploaded!")
#End of functions.....




#Printing Menu
print(40*'*')
print("Cars Sales Platform")
print(40*('*'))
print("\n\n             Menu")
print(40*'*')
print('''1.Sell a Car.
2.Remove a Car Data.
3.List all Cars.
4.Search a Car.
5.Update a Car Data.
6.Export the Car Data as .csv file.
7.Import a .csv file and upload it.''')
print(40*'*')


#Getting input and running the entire pgm..
case = int(input("Enter a Operation(Its S.no): "))
if case == 1:
    insert()
elif case == 2:
    remove()
elif case == 3:
    lists()
elif case == 4:
    show()
elif case == 5:
    update()
elif case == 6:
    Exportcsv()
elif case == 7:
    Importcsv()
else:
    print("Operaion Does not Exists!\n\nERR: Not a valid input")

#End of he pgm