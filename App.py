from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
import time

"""import mysql.connector as mysql"""

root = Tk()
root.title("Welcome !")
root.geometry("300x150")

city = ["MARINA","JBR","JLT","DEIRA","ABOU DABI"]


e = Entry(root, width=25)
e.insert(0, 'Enter your name')
e.pack()
e.place(x=70,y=10)

def open():
    global name
    name = e.get()
    root.destroy()

    global top
    top = Tk()
    top.title("The basket project")
    top.geometry("800x300")

    myLabel = Label(top, text = 'Hello ' + name + '! What can we do for you today ?')
    myLabel.pack()

    global clicked
    clicked = StringVar()
    clicked.set('TENNIS')
    drop = OptionMenu(top,clicked,'BASKET','TENNIS','FOOTBALL')
    drop.pack()
    drop.place(x=40,y=60)

    global clicked_1
    clicked_1 = StringVar()
    clicked_1.set(city[0])
    drop1 = OptionMenu(top,clicked_1,*city)
    drop1.pack(expand=True)
    drop1.place(x=170,y=60)

    global clicked_2
    clicked_2 = StringVar()
    clicked_2.set('-')
    drop2 = OptionMenu(top,clicked_2,'-','FREE COURT','PAYING COURT')
    drop2.pack()
    drop2.place(x=310,y=60)

    global List
    List = Listbox(top,width=50)
    List.place(x=440, y =60)

    global Crenel
    Crenel = Entry(top, width=30)
    Crenel.insert(0, 'Enter a time for your reservation')
    Crenel.pack()
    Crenel.place(x=40,y=140)

    global Name
    Name = Entry(top, width=30)
    Name.insert(0, name)
    Name.pack()
    Name.place(x=40,y=100)


    SearchButton = Button(top, text = 'Search a court',bg='#76c893', command=SearchCourt)
    SearchButton.pack(anchor=CENTER)
    SearchButton.place(x=100,y=250)

    ReservationButton = Button(top, text='Make a reservation',bg='#76c893', command=Reservation)
    ReservationButton.pack(anchor=CENTER)
    ReservationButton.place(x=300,y=250)

    AvailableButton = Button(top, text='Check reservation',bg='#76c893', command=Availability)
    AvailableButton.pack(anchor=CENTER)
    AvailableButton.place(x=500,y=250)

    MVPButton = Button(top, text='MVP',bg='#76c893', command=mvp)
    MVPButton.pack(anchor=CENTER)
    MVPButton.place(x=700,y=250)

def mvp():
    con = mysql.connect(host="localhost", user="root",password="root", database = "basket")
    custor = con.cursor()

    custor.execute("select sport, count(*) as number from Court c join Reservation r on c.court_id=r.court_id group by c.sport order by count(*) DESC;")
    result = custor.fetchall()

    List.delete(0,END)
    for row in result:
        insertData = str(row[0])+ '    ' + str(row[1])
        List.insert(List.size()+1,insertData)

    con.close()

def Reservation():
    if len(List.curselection()) == 0 :
        response = MessageBox.showwarning("The Basket team","You must select a court and choose a time to make a reservation.")
    else:
        for i in List.curselection():
            resa_id = List.get(i)
        court_id = resa_id.split(' ')[0]
        crenel = Crenel.get()
        name = Name.get()
        ts = time.time()
        resa_id = str(int(ts))
        con = mysql.connect(host="localhost", user="root",password="root", database = "basket")
        custor = con.cursor()
        custor.execute("insert into reservation values ('" + resa_id + "','"+ name +"','" + court_id +  "','"+crenel+"');")
        custor.execute("commit")

        response = MessageBox.showinfo("The Basket team","Your reservation has been done successfuly  🎉")
        """Label(root,text=response).pack()"""

        con.close()



def Availability():
    if len(List.curselection()) == 0 :
        response = MessageBox.showwarning("The Basket team","Please select a court to see its reservation")
    else:
        for i in List.curselection():
            resa_id = List.get(i)
        court_id = resa_id.split(' ')[0]
        con = mysql.connect(host="localhost", user="root",password="root", database = "basket")
        custor = con.cursor()
        custor.execute("select * from Reservation where court_id = '" + court_id  + "';")
        result = custor.fetchall()
        con.close()
    show2(result)


def SearchCourt():
    con = mysql.connect(host="localhost", user="root",password="root", database = "basket")
    custor = con.cursor()

    free = clicked_2.get()
    if free == '-':
        custor.execute("select * from court where sport = '" + str(clicked.get()) + "' and city = '" + str(clicked_1.get()) + "';")
        result = custor.fetchall()
    elif free == 'FREE COURT':
        custor.execute("select * from court where sport = '" + str(clicked.get()) + "' and city = '" + str(clicked_1.get()) + "' and price = 0;")
        result = custor.fetchall()
    else:
        custor.execute("select * from court where sport = '" + str(clicked.get()) + "' and city = '" + str(clicked_1.get()) + "' and price <> 0;")
        result = custor.fetchall()

    show(result)
    con.close()
    

def show(result):
    List.delete(0,END)
    if len(result) == 0:
        response = MessageBox.showinfo("Basket team","Sorry, there are no sports fields available for your search 😢")

    for row in result:
        insertData = str(row[0])+ '    ' + str(row[1] + '   ' + str(row[2]) + '   ' + str(row[3]))
        List.insert(List.size()+1,insertData)

def show2(result):
    List.delete(0,END)
    if len(result) == 0:
        response = MessageBox.showinfo("Basket team","No reservation has been made yet for this court !")

    for row in result:
        insertData = str(row[0])+ '    ' + str(row[1] + '   ' + str(row[2]) + '   ' + str(row[3]))
        List.insert(List.size()+1,insertData)


myButton = Button(root, text = 'Start a reservation',command=open)
myButton.pack(anchor=CENTER)
myButton.place(x=90,y=50)


'''response = MessageBox.showinfo("Basket team","Your reservation has been done successfuly  🎉")
    Label(root,text=response).pack()
'''
root.mainloop()
top.mainloop()
