
'''from tkinter import *
root = Tk()
def prop(n):
    return 360.0 * n / 1000

tkinter.Label(root, text='Pie Chart').pack()
c = tkinter.Canvas(width=154, height=154)
c.pack()
c.create_arc((2,2,152,152), fill="#FAF402", outline="#FAF402", start=prop(0), extent = prop(200))
c.create_arc((2,2,152,152), fill="#00AC36", outline="#00AC36", start=prop(200), extent = prop(400))
c.create_arc((2,2,152,152), fill="#7A0871", outline="#7A0871", start=prop(600), extent = prop(50))
c.create_arc((2,2,152,152), fill="#E00022", outline="#E00022", start=prop(650), extent = prop(200))
c.create_arc((2,2,152,152), fill="#294994", outline="#294994",  start=prop(850), extent = prop(150))

root.geometry
root.mainloop()
'''

from tkinter import *
import random
import MySQLdb
from tkinter import messagebox
from tkinter import font
from PIL import ImageTk,Image
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from datetime import date
from validate_email import validate_email
from smtplib import *
from dateutil.parser import parse
db=MySQLdb.connect("localhost","root","","Expense_Manager")
cursor=db.cursor()
username=''#either email or username
_username=''#strictly username
all_data=tuple
activeState=Canvas
tagged=float
untagged=float
FrameUnderCanvases=Frame
_canvas1=Canvas
Income_label=Label
Expense_label=Label
Status=Label
frame_on_canvas=Frame
Budget_label=Label
Name_Frame=Frame
choice=''
# frame=Frame
# de=DateEntry
cursor.execute(
    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=database() AND TABLE_NAME='manage_expense'")
manage_expense_columns = cursor.fetchall()
cursor.execute(
    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=database() AND TABLE_NAME='users'")
users_columns = cursor.fetchall()
transaction_date=''
transaction_amount=''
transaction_description=''
transaction_tag=''
delete_button=Button
Datewise=DateEntry
Add_tran_date=DateEntry
indeces_of_date=''
Date=''
overall_expense=0
overall_income=0
month_income=0
month_expense=0
#==========================WORKING AND STORING PART====================================================
def get_expenses_and_incomes():
    global transaction_date,transaction_amount,overall_expense,overall_income,month_expense,month_income
    for search in range(0,len(transaction_amount)):
        if transaction_amount[search][0]=="+":
            overall_income+=int(transaction_amount[search])
        else:
            overall_expense+=int(transaction_amount[search])
    if overall_expense < 0:
        overall_expense = -(overall_expense)
    else:
        pass

    _month=datetime.datetime.today().month
    # print(date)
    date_index=[]
    # date_index=[i for i, x in enumerate(transaction_date) if x == date]
    for i in range(0,len(transaction_date)):
        dt = datetime.datetime.strptime(transaction_date[i], '%m/%d/%Y')
        if dt.month==_month:
            date_index.append(i)
        else:
            pass
    print(date_index)
    if len(date_index)>0:
        amount = [v for i, v in enumerate(transaction_amount) if i in date_index]
        for search in range(0, len(amount)):
            if amount[search][0] == "+":
                month_income += int(amount[search])
            else:
                month_expense += int(amount[search])
        if month_expense<0:
            month_expense= -(month_expense)
        else:
            pass
def DatePicker(window,x,y):
 # change ttk theme to 'clam' to fix issue with downarrow button
 style = ttk.Style(window)
 style.theme_use('clam')

 class MyDateEntry(DateEntry):
  def __init__(self, master=None, **kw):
   DateEntry.__init__(self, master=window, **kw)
   # add black border around drop-down calendar
   self._top_cal.configure(bg='black', bd=1)
   # add label displaying today's date below
   Label(self._top_cal, bg='gray90', anchor='w',
         text='Today: %s' % date.today().strftime('%x')).pack(fill='x')

 # create the entry and configure the calendar colors
 de = MyDateEntry(window, year=date.today().year, month=date.today().month, day=date.today().day,
                  width=12,
                  selectbackground='gray80',
                  selectforeground='black',
                  normalbackground='white',
                  normalforeground='black',
                  background='gray90',
                  foreground='black',
                  bordercolor='gray90',
                  othermonthforeground='gray50',
                  othermonthbackground='white',
                  othermonthweforeground='gray50',
                  othermonthwebackground='white',
                  weekendbackground='white',
                  weekendforeground='black',
                  headersbackground='white',
                  headersforeground='gray70')
 de.place(x=x, y=y)
 return de
def delete_transaction(var):
    global transaction_amount,transaction_description,transaction_date,transaction_tag,delete_button,all_data,Date
    print(transaction_amount,"\n",transaction_description,"\n",transaction_date,"\n",transaction_tag)
    if choice=="datewise":
        cursor.execute("select * from manage_expense where username='%s' " % (_username))
        all_data = list(cursor.fetchone())
        # all_data=all_data.split(',')
        split_into_list(all_data)
    else:
        pass
    print(indeces_of_date)
    var0 = int(var.get())
    del transaction_description[var0]
    del transaction_amount[var0]
    del transaction_tag[var0]
    del transaction_date[var0]
    Calculate_tags()
    print("date",transaction_date)
    list_of_list=[transaction_date,transaction_amount,transaction_description,transaction_tag]
    print(transaction_amount, "\n", transaction_description, "\n", transaction_date, "\n", transaction_tag)
    try:
        for set_null in range(0,len(list_of_list)):
            column_name = ''.join(manage_expense_columns[set_null+2])
            cursor.execute("UPDATE manage_expense SET %s =NULL where username='%s'"
                           %(column_name,_username))
            db.commit()
        for col in range(0,4):
            column_name = ''.join(manage_expense_columns[col + 2])
            print("column=",col)
            print(column_name)
            for val in range(len(list_of_list[col])):
                print("value=",val)
                null_or_not=cursor.execute("SELECT * FROM manage_expense WHERE %s IS NULL and username='%s' " % (column_name,_username))
                if null_or_not==0:
                    cursor.execute(
                                       "UPDATE manage_expense SET %s = CONCAT(%s,',%s') where username='%s'"
                                     % (column_name,column_name,list_of_list[col][val], _username))
                    db.commit()
                else:
                    cursor.execute(
                            "UPDATE manage_expense SET %s = '%s' where username='%s'"
                              % (column_name, list_of_list[col][val], _username))
                    db.commit()

        # null_or_not = cursor.execute("SELECT * FROM manage_expense WHERE date IS NULL and username='%s' " % (_username))
        # if null_or_not==0:
        if choice=="all":
            CheckTheButton("tran")
        elif choice=="datewise":
            messagebox.showinfo("", "Transaction deleted successfully.")
            _get_transaction_by_date(Date)
        var.set(None)
        delete_button.config(state='disabled',bg="white",fg="black")

    except:
        messagebox.showerror("","Something went wrong.")
def ShowChoice(var):
    global delete_button

    delete_button.config(state='normal',bg="grey",fg="white",command=lambda:delete_transaction(var))
def data():
    global transaction_date,transaction_amount,transaction_description,transaction_tag,choice,indeces_of_date
    var = StringVar()
    row=10
    length_of_transactions=len(transaction_amount)
    list_of_radiobutton_values=[]
    for value in range(0, length_of_transactions):
        list_of_radiobutton_values.append(value)
    var.set(None)
    for index in range(0,length_of_transactions):

        R=Radiobutton(frame_on_canvas, variable=var, tristatevalue='',
                    command=lambda: (ShowChoice(var)))
        R.place(x=25, y=row)
        if choice == "all":
            R.configure(value=list_of_radiobutton_values[index])
        else:
            R.configure(value=indeces_of_date[index])
        Label(frame_on_canvas,text=transaction_date[index],font=("calibri",13)).place(x=140,y=row)
        amount=transaction_amount[index]
        if amount[:1]=='+':
            Label(frame_on_canvas, text=transaction_amount[index], font=("calibri", 13),fg="green").place(x=280, y=row)
        else:
            Label(frame_on_canvas, text=transaction_amount[index], font=("calibri", 13),fg="red").place(x=280, y=row)
        Label(frame_on_canvas, text=transaction_description[index].capitalize(), font=("calibri", 13)).place(x=450, y=row)
        Label(frame_on_canvas, text=transaction_tag[index], font=("calibri", 13)).place(x=990, y=row)
        row+=50
def _get_transaction_by_date(_Date):
    global Datewise,choice,activeState,indeces_of_date,transaction_date,transaction_amount,transaction_description,transaction_tag,Date,frame_on_canvas
    Date=_Date
    indeces_of_date=[i for i, x in enumerate(transaction_date) if x == Date]
    print(indeces_of_date)
    print(transaction_date)
    if len(indeces_of_date)>0:
        transaction_date = [v for i, v in enumerate(transaction_date) if i in indeces_of_date]
        transaction_amount = [v for i, v in enumerate(transaction_amount) if i in indeces_of_date]
        transaction_description = [v for i, v in enumerate(transaction_description) if i in indeces_of_date]
        transaction_tag = [v for i, v in enumerate(transaction_tag) if i in indeces_of_date]
        choice = "datewise"
        # print("transaction date", (transaction_date))
        activeState.destroy()
        _ManageTransactions()
        cursor.execute("select * from manage_expense where username='%s' " % (_username))
        all_data = list(cursor.fetchone())
        split_into_list(all_data)

    else:
        if choice=="all":
            messagebox.showerror("", "No Transactions made on %s" % (Date))
        else:
            messagebox.showinfo("", "All transactions made on %s are deleted successfully" % (Date))
            CheckTheButton("tran")
def add_transaction_to_database(add_var,amount,variable,description):
    global manage_expense_columns,all_data,Add_tran_date
    if description.get() == '':
        des = "none"
    else:
        des=description.get()
    if (add_var.get() and amount.get() and variable.get() and Add_tran_date.get())!='':
        def is_date(string):
            try:
                parse(string)
                return True
            except ValueError:
                return False

        verify_date_format = is_date(Add_tran_date.get())
        verify_amount = amount.get().isdigit()
        print(verify_date_format,verify_amount)
        if (verify_amount and verify_date_format)==True:
            if  add_var.get()=="expense":
                list_of_values=[Add_tran_date.get(),"-%s"%(amount.get()),des,variable.get()]
                print(list_of_values)
            else:
                list_of_values=[Add_tran_date.get(),"+%s"%(amount.get()),des,variable.get()]
                print(list_of_values)
            null_or_not=cursor.execute("SELECT * FROM manage_expense WHERE date IS NULL and username='%s' " % (_username))
            if null_or_not==0:
                for k in range(2,6):
                    print(k)
                    column_name=''.join(manage_expense_columns[k])
                    cursor.execute("UPDATE manage_expense SET %s = CONCAT(%s,',%s')"
                                   " where username='%s'" % (column_name,column_name,list_of_values[k-2],_username))
                    db.commit()
                add_var.set(None)
                amount.delete(0,"end")
                variable.set("NO TAG")
                description.delete(0,"end")

                messagebox.showinfo("SUCCESS", "Transaction added successfully.")
                CheckTheButton("tran")
                add_transaction_setup()
            else:
                for k in range(2, 6):
                    column_name = ''.join(manage_expense_columns[k])
                    cursor.execute("UPDATE manage_expense SET %s = '%s' where username='%s'" % (
                    column_name, list_of_values[k - 2], _username))
                    db.commit()
                add_var.set(None)
                amount.delete(0, "end")
                variable.set("NO TAG")
                description.delete(0, "end")

                messagebox.showinfo("SUCCESS", "Transaction added successfully.")
                CheckTheButton("tran")
                add_transaction_setup()

            # except:
            #     messagebox.showerror("","Something went wrong.\nUnable to store data.")#MySQL stores limited amount of data,it cannot hold unlimited data
                #LONGTEXT is used as data type for each column.When the data in columns will exceed the length then this popup will occur

        else:
            messagebox.showerror("ERROR!","Invalid date format or amount.")

    else:
        messagebox.showerror("ERROR!","All fields are compulsary except 'DESCRIPTION.'")
def add_transaction_setup():
    global Add_tran_date
    Add=Toplevel(activeState)
    Add.geometry("480x400+450+250")
    Add.title("Add a new transaction!")
    # Add.attributes('-topmost', 'true')
    Add.grab_set()
    add_var = StringVar()
    Label(Add, text="Type: ", font=("georgia",10,"bold")).place(x=10,y=10)
    Label(Add, text="Amount:", font=("georgia",10,"bold")).place(x=10,y=80)
    Label(Add, text="Date:", font=("georgia",10,"bold")).place(x=330,y=80)
    Label(Add, text="Description:", font=("georgia", 10, "bold")).place(x=10, y=160)
    Label(Add, text="Tag:", font=("georgia",10,"bold")).place(x=10,y=250)


    R1 = Radiobutton(Add, text="Expense", variable=add_var, value="expense",tristatevalue=0)
    R1.place(x=10,y=40)

    R2 = Radiobutton(Add, text="Income", variable=add_var, value="income",
                     tristatevalue=0)
    R2.place(x=110,y=40)

    R3 = Radiobutton(Add, text="Refund", variable=add_var, value="refund",tristatevalue=0)
    R3.place(x=210,y=40)

    amount = Entry(Add, width=30,bd=2)
    amount.place(x=10,y=125)
    description = Entry(Add, width=60, bd=2)
    description.place(x=10, y=200)
    Add_tran_date = DatePicker(Add, 330, 120)
    add_btn = Button(Add, text='Add Transaction',relief=FLAT
                 ,bd=0,bg="grey",fg="white",font=("calibri",14,"italic"),
                     command=lambda :add_transaction_to_database(add_var,amount,variable,description)
                 )
    add_btn.place(x=180,y=350)


    OPTIONS = [
        "FOOD",
        "ENTERTAINMENT",
        "SHOPPING",
        "TRANSPORTATION",
        "TRAVEL",
        "SALARY",
        "OTHER",
        "NO TAG"
    ]

    variable = StringVar(Add)
    variable.set(OPTIONS[-1])  # default value

    tags = OptionMenu(Add, variable, *OPTIONS)
    tags.place(x=10,y=280)
    tags.config(bg="grey",fg="white")
    tags['menu'].config(bg="white")
def Frame_and_labels(Heading,k):
 global Name_Frame,delete_button,overall_income,overall_expense,month_income,month_expense
 Name_Frame = Frame(_canvas1, width=1166, height=60, bd=0, bg="White")
 Name_Frame.place(x=0, y=0)

 Page_lbl = Label(Name_Frame, text=Heading, font=("georgia", 22), fg="#36C2FF", bg="white")
 Page_lbl.place(x=40, y=10)
 if k==0:
  Income_label=Label(_canvas1,text="Overall Income | Income this month",fg="#606472",font=("georgia",14))
  Income_label.place(x=100,y=100)

  Label(_canvas1, text=u"\u20B9"+str(overall_income), fg="green", font=("georgia", 14)).place(x=130, y=130)
  #Label(_canvas1, text="|", fg="#606472", font=("georgia", 14)).place(x=230,y=130)
  Label(_canvas1, text=u"\u20B9"+str(month_income), fg="green", font=("georgia", 14)).place(x=300, y=130)

  Expense_label = Label(_canvas1, text="Overall Expense | Expense this month", fg="#606472", font=("georgia", 14))
  Expense_label.place(x=700, y=100)

  Label(_canvas1, text=u"\u20B9"+str(overall_expense), fg="red", font=("georgia", 14)).place(x=730, y=130)
  # Label(_canvas1, text="|", fg="#606472", font=("georgia", 14)).place(x=230,y=130)
  Label(_canvas1, text=u"\u20B9"+str(month_expense), fg="red", font=("georgia", 14)).place(x=950, y=130)


 else:
  Tran_Frame = Frame(_canvas1, width=1155,relief=RAISED,bd=2, height=60, bg="White")
  Tran_Frame.place(x=5, y=120)

  Overall_button=Button(_canvas1,relief=RIDGE,bd=2,activeforeground="powder blue",text="All transations till date",font=("georgia",12),command=lambda :CheckTheButton("tran"))
  Overall_button.place(x=40,y=70)

  Datewise_Label = Label(_canvas1,
                          text="Transactions made on a date:", font=("georgia", 12))
  Datewise_Label.place(x=250, y=75)
  Datewise=DatePicker(_canvas1,480,75)
  Search_button = Button(_canvas1, relief=RIDGE, bd=1, activeforeground="powder blue",
                         text="Search Transactions", font=("georgia", 10), command=lambda :_get_transaction_by_date(Datewise.get()))
  Search_button.place(x=585, y=73)
  Total = Label(Name_Frame, bg="white", font=("georgia", 12, "italic"), text="Total:")
  Total.place(x=700, y=12)
  Tran_Label1 = Label(Name_Frame, text="Tagged:", bg="white", font=("georgia", 12,"italic"))
  Tran_Label1.place(x=800, y=12)
  Tran_Label2 = Label(Name_Frame, text="Untagged:", bg="white", font=("georgia", 12,"italic"))
  Tran_Label2.place(x=900, y=12)

  Add_Transaction_btn=Button(_canvas1,bg="grey",text="Add Transaction",fg="white",relief=FLAT,font=("calibiri",12,"italic"),command=add_transaction_setup)
  Add_Transaction_btn.place(x=980,y=70)

  delete_button=Button(Tran_Frame, bd=0,state="disabled",text="Delete",bg="white", font=("georgia", 14))
  delete_button.place(x=20, y=12)
  Tran_Label4 = Label(Tran_Frame, text="Date", bg="white", font=("georgia", 14))
  Tran_Label4.place(x=150, y=0)
  Tran_Label8 = Label(Tran_Frame, text="(MM/DD/YYYY)", bg="white",fg="grey", font=("georgia", 8))
  Tran_Label8.place(x=130, y=30)
  Tran_Label5 = Label(Tran_Frame, text="Amount"+'('+u"\u20B9"+')', bg="white", font=("georgia", 14))
  Tran_Label5.place(x=280, y=12)
  Tran_Label6 = Label(Tran_Frame, text="Description", bg="white", font=("georgia", 14))
  Tran_Label6.place(x=450, y=12)
  Tran_Label7 = Label(Tran_Frame, text="Tag", bg="white", font=("georgia", 14))
  Tran_Label7.place(x=1000, y=12)
i=0
def Draw_canvas1():
 global  _canvas1,activeState
 _canvas1 = Canvas(FrameUnderCanvases, width=1166, height=768, bd=0, highlightthickness=0)
 _canvas1.grid(row=1, column=1)

 _canvas1.grid_propagate(0)
 activeState=_canvas1
def CheckTheButton(i):
 global activeState,de,choice
 if i=="tran":
   activeState.destroy()
   choice = "all"
   try:
       de.destroy()
       _ManageTransactions()
   except:
       _ManageTransactions()
 elif i=="rep":
  activeState.destroy()
  try:
      de.destroy()
      _Reports()
  except:
      _Reports()
 elif i=="bud":
  activeState.destroy()
  try:
      de.destroy()
      _Budgets()
  except:
      _Budgets()
 elif i=="rem":
  activeState.destroy()
  try:
      de.destroy()
      _Reminders()
  except:
      _Reminders()
 elif i=="ser":
  try:

      de.destroy()
      _Search()
  except:
      _Search()
 elif i=="reset":
     try:
         de.destroy()
         _reset_password()
     except:
         _reset_password()

 elif i=="acc":
  activeState.destroy()
  try:
      de.destroy()
      _Accounts()
  except:
      _Accounts()
 elif i=="dash":
  activeState.destroy()
  try:
      de.destroy()
      _Dashboard()
  except:
      _Dashboard()
def scrolling_canvas(number_of_transaction):
 global frame_on_canvas
 frame = Frame(_canvas1, width=1121, height=410, bg="white")
 frame.place(y=180, x=5)
 scroll_canvas = Canvas(frame, width=1121, height=410)
 vbar = Scrollbar(frame, orient=VERTICAL)
 vbar.pack(side=RIGHT, fill=Y)
 vbar.config(command=scroll_canvas.yview)
 #scroll_canvas.config(width=1121, height=410)
 scroll_canvas.config( yscrollcommand=vbar.set)
 scroll_canvas.pack(side=LEFT, expand=True, fill=BOTH)
 frame_on_canvas = Frame(scroll_canvas, width=1120,relief=SUNKEN,bd=2)
 frame_on_canvas.place(x=2, y=2)
 frame_on_canvas.propagate(0)
 if len(transaction_amount)>8:
     frame_on_canvas.configure(height=len(transaction_amount)*63)
 else:
     frame_on_canvas.configure(height=450)
 if number_of_transaction==0:
     Label(frame_on_canvas,text="No Transactions Yet", font=("georgia", 22), fg="#36C2FF").place(x=400,y=150)

 #HEIGHT OF FRAME ABOVE CANVAS IS TEMPORARILY SET TO 10,000 WHICH IS ENOUGH FOR 100 ENTRIES TO BE SHOWN AS TRANSACTION
  #IF NUMBER OF TRANSACTIONS ARE HIGHER THEN KINDLY INCREASE THE HEIGHT OF THE FRAME_ON_CANVAS
 else:
     def myfunction(event):
      scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

     scroll_canvas.create_window((0, 0), window=frame_on_canvas
                                  )  # (0,0)=x,y
     scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
     frame_on_canvas.bind("<Configure>", myfunction)
     print(transaction_date,transaction_amount,"\n",choice)
def _Dashboard():
 global choice,month_income,month_expense,overall_expense,overall_income,frame_on_canvas
 Draw_canvas1()
 get_expenses_and_incomes()
 Frame_and_labels("DASHBOARD",0)
 choice="all"
 month_expense=0
 overall_expense=0
 month_income=0
 overall_income=0
 scrolling_canvas(1)
 # frame_on_canvas.configure(bg="white",bd=0)

def _Reports():
 global choice,month_income,month_expense,overall_expense,overall_income
 Draw_canvas1()
 get_expenses_and_incomes()
 Frame_and_labels("REPORTS",0)
 choice="all"
 month_expense = 0
 overall_expense = 0
 month_income = 0
 overall_income = 0
def _Budgets():
 Draw_canvas1()
def _Reminders():
 Draw_canvas1()
def _Search():
 # Draw_canvas1()
 splashscreen = Toplevel(activeState, relief=RAISED,bd=2, bg="#CCD6E5")
 splashscreen.overrideredirect("True")
 splashscreen.geometry("400x120+500+350")
 Quit_btn=Button(splashscreen,text="Quit",fg="red",activebackground="#CCD6E5",font=10,command=splashscreen.destroy
                 ,relief=FLAT,bd=0,bg="#CCD6E5").place(y=85,x=180)
 Label(splashscreen,text="Search Tagged Transaction",bg="#CCD6E5",font=10).place(x=100,y=5)
 Tag_Entry=Entry(splashscreen,width=40,bd=2).place(x=15,y=50)
 Search_tag_transaction=Button(splashscreen,text="Search")
 Search_tag_transaction.place(x=300,y=50)
def _Accounts():
 Draw_canvas1()
def _ManageTransactions():
 global _username,all_data,frame_on_canvas,\
     transaction_date,transaction_amount,transaction_description,transaction_tag,choice
 Draw_canvas1()
 Frame_and_labels("MANAGE TRANSACTIONS",1)
 cursor.execute("select username from users where (username='%s' or email='%s' )"%(username,username))
 _username=cursor.fetchone()
 _username=''.join(_username)
 null_or_not = cursor.execute("SELECT * FROM manage_expense WHERE date IS NULL and username='%s' " % (_username))
 if null_or_not==0:
     if choice=="all":
         cursor.execute("select * from manage_expense where username='%s' " % (_username))
         all_data = list(cursor.fetchone())
    # all_data=all_data.split(',')
         split_into_list(all_data)
         Calculate_tags()
         if(len(all_data[2])>0):
             scrolling_canvas(1)
             data()

         else:
             scrolling_canvas(0)
             frame_on_canvas.configure(height=500)
     elif choice=="datewise":
         Calculate_tags()
         scrolling_canvas(1)
         data()

 else:
     scrolling_canvas(0)
def Calculate_tags():
    global transaction_tag,tagged,untagged,Name_Frame
    untagged=transaction_tag.count("NO TAG")
    tagged=len(transaction_tag)-untagged
    TagLabel=Label(Name_Frame, bg="white", font=("georgia", 12,"italic"))
    TagLabel.place(x=870, y=12)
    UnTagLabel=Label(Name_Frame, bg="white", font=("georgia", 12,"italic"))
    UnTagLabel.place(x=980, y=12)
    TotalLabel = Label(Name_Frame, bg="white", font=("georgia", 12, "italic"))
    TotalLabel.place(x=750, y=12)
    if len(transaction_tag)>0:
        TotalLabel.configure(text=tagged+untagged)
        TagLabel.configure(text=tagged)
        UnTagLabel.configure(text=untagged)
    else:
        TotalLabel.configure(text="0")
        TagLabel.configure(text="0")
        UnTagLabel.configure(text="0")
def _check_password(reset,new_pass,confirm_pass):
    if new_pass.get()=="" or confirm_pass.get()=="":
        new_pass.configure(highlightbackground="red",highlightthickness=1)
        confirm_pass.configure(highlightbackground="red", highlightthickness=1)
        popup = messagebox.showerror("ERROR", "Kindly fill both the entries.", parent=reset)
        # time.sleep(2)
        new_pass.configure(highlightbackground=None, highlightthickness=0)
        confirm_pass.configure(highlightbackground=None, highlightthickness=0)
    elif new_pass.get()!=confirm_pass.get():
        messagebox.showerror("ERROR","Passwords are not matching",parent=reset)
    elif new_pass.get()==confirm_pass.get() :
        if len(new_pass.get())>=8 and len(new_pass.get())<13:
            store=cursor.execute("update users set password='%s' where (username='%s' or email='%s')"%(new_pass.get(),username,username))
            db.commit()
            if store==1:
                messagebox.showinfo("SUCCESS","Password changed successfully.",parent=reset)
                reset.destroy()
        else:
            messagebox.showerror("ERROR!","Password should have a minimum length of 8\nand maximum length of 12",parent=reset)
def _reset_password():
    reset=Toplevel(activeState)
    reset.geometry("500x150+450+250")
    reset.title("Change password!")
    reset.attributes('-topmost', 'true')
    reset.grab_set()
    Label(reset,text="New Password :",font=3).grid(row=0,column=0,pady=(15,10),padx=(20,0),sticky=NW)
    Label(reset, text="Confirm Password :",font=3).grid(row=1, column=0, pady=(15,10), padx=(20,0),sticky=NW)
    new_pass=Entry(reset,width=50,show="\u2022")
    new_pass.grid(row=0,column=1,pady=(20,0),sticky=NW)
    confirm_pass = Entry(reset, width=50,show="\u2022")
    confirm_pass.grid(row=1, column=1, pady=(20, 0), sticky=NW)
    btn = Button(reset, text='Change Password',width=20,command=lambda : _check_password(reset,new_pass,confirm_pass))
    btn.grid(row=3,column=1,pady=(10,0),padx=(20,0))
def Manage(canvas,name):
 global activeState,FrameUnderCanvases,_canvas1
 root.title("USER: "+name)
 canvas.destroy()
 FrameUnderCanvases=Frame(root,width=1366,height=693)
 FrameUnderCanvases.grid(row=1,column=0)

 _canvas = Canvas(FrameUnderCanvases, width=210,bg="#2D3439", height=768, bd=0, highlightthickness=0)
 _canvas.grid(row=1, column=0)
 _canvas.grid_propagate(0)

 Draw_canvas1()

 _canvas1.create_text(600, 200, text="Welcome " + username + " !", font=("Times new roman", 35, "bold"))
 _canvas1.create_text(600, 300, text="Track your wallet with 'Expense Tracker'.", font=("Times new roman", 30, "bold"))
 activeState=_canvas1

 '''_button_frame=Frame(_canvas,bg="black",height=768,width=200)
 _button_frame.grid(row=0,column=0)
 _button_frame.grid_propagate(0)'''
 dash= ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/dashboard1.png"))
 dash_lbl=Label(_canvas,image=dash,bg="#2D3439",height=55)
 dash_lbl.grid(row=1,column=0,pady=(1,0),sticky=W)
 dash.image=dash

 report = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/report1.png"))
 report_lbl=Label(_canvas, image=report, bg="#2D3439", height=55,width=25)
 report_lbl.grid(row=2, column=0,pady=(1,0),sticky=W)
 report.image = report

 budget = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/budgets1.png"))
 budget_lbl=Label(_canvas, image=budget, bg="#2D3439", height=55, width=25)
 budget_lbl.grid(row=3, column=0, pady=(1, 0), sticky=W)
 budget.image = budget

 reminder = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/reminder1.png"))
 reminder_lbl = Label(_canvas, image=reminder, bg="#2D3439", height=55, width=25)
 reminder_lbl.grid(row=4, column=0, pady=(1, 0), sticky=W)
 reminder.image = reminder

 search = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/search1.png"))
 search_lbl= Label(_canvas, image=search, bg="#2D3439", height=55, width=25)
 search_lbl.grid(row=5, column=0, pady=(1, 0), sticky=W)
 search.image = search

 account = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/accounts1.png"))
 account_lbl=Label(_canvas, image=account, bg="#2D3439", height=55, width=25)
 account_lbl.grid(row=6, column=0, pady=(1, 0), sticky=W)
 account.image = account

 transaction = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/transaction1.png"))
 transaction_lbl=Label(_canvas, image=transaction, bg="#2D3439", height=55, width=25)
 transaction_lbl.grid(row=7, column=0, pady=(1, 0), sticky=W)
 transaction.image = transaction

 reset = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/reset1.png"))
 reset_lbl=Label(_canvas, image=reset, bg="#2D3439", height=55, width=25)
 reset_lbl.grid(row=8, column=0, pady=(1, 0), sticky=W)
 reset.image = reset

 logout = ImageTk.PhotoImage(Image.open("C:/Users/priyanka/Desktop/My Stuff/logout1.png"))
 logout_lbl = Label(_canvas, image=logout, bg="#2D3439", height=55, width=25)
 logout_lbl.grid(row=9, column=0, pady=(1, 0), sticky=W)
 logout.image = logout

 _canvas.create_line(0, 0, 211, 0,fill="black")
 Dashboard_btn=Button(_canvas, text="      DASHBOARD >",font=("georgia",14),bd=0,
                      activebackground="#2D3439",activeforeground="powder blue",command=lambda :CheckTheButton("dash"),bg="#2D3439",relief=FLAT,fg="white",compound="left",height=2,width=16)
 Dashboard_btn.grid(row=1,column=1,pady=(1,0),sticky=W)
 _canvas.create_line(0, 60, 211, 60, fill="black")
 Report_btn=Button(_canvas, text="      REPORTS       >",font=("georgia",14),bd=0,
                      activebackground="#2D3439",activeforeground="powder blue",command=lambda :CheckTheButton("rep"),bg="#2D3439",relief=FLAT,fg="white",compound="left",height=2,width=16)
 Report_btn.grid(row=2,column=1,sticky=W,pady=(1,0))
 _canvas.create_line(0, 120, 211, 120, fill="black")
 Budget_btn=Button(_canvas, text="      BUDGETS       >",font=("georgia",14),bd=0,
                      activebackground="#2D3439",activeforeground="powder blue",bg="#2D3439",command=lambda :CheckTheButton("bud"),relief=FLAT,fg="white",compound="left",height=2,width=16)
 Budget_btn.grid(row=3,column=1,sticky=W,pady=(1,0))
 _canvas.create_line(0, 180, 211, 180, fill="black")
 Reminder_btn=Button(_canvas, text="      REMINDER    >",font=("georgia",14),bd=0,
                      activebackground="#2D3439",activeforeground="powder blue",bg="#2D3439",relief=FLAT,command=lambda :CheckTheButton("rem"),fg="white",compound="left",height=2,width=16)
 Reminder_btn.grid(row=4,column=1,sticky=W,pady=(1,0))
 _canvas.create_line(0, 240, 211, 240, fill="black")
 Search_btn=Button(_canvas, text="      SEARCH         >",font=("georgia",14),bd=0,
                      activebackground="#2D3439",activeforeground="powder blue",bg="#2D3439",relief=FLAT,fg="white",command=lambda :CheckTheButton("ser"),compound="left",height=2,width=16)
 Search_btn.grid(row=5,column=1,sticky=W,pady=(1,0))
 _canvas.create_line(0,300, 211, 300, fill="black")
 Account_btn=Button(_canvas, text="      ACCOUNTS    >",font=("georgia",14),bd=0,
                      activebackground="#2D3439",activeforeground="powder blue",bg="#2D3439",relief=FLAT,fg="white",compound="left",command=lambda :CheckTheButton("acc"),height=2,width=16)
 Account_btn.grid(row=6,column=1,sticky=W,pady=(1,0))
 _canvas.create_line(0, 360, 211, 360, fill="black")
 Manage_btn = Button(_canvas, text="      MANAGE\n TRANSACTIONS >", font=("georgia", 14), bd=0,
                      activebackground="#2D3439", activeforeground="powder blue", bg="#2D3439", relief=FLAT, fg="white",
                      compound="left", height=2,width=16,command=lambda :CheckTheButton("tran"))
 Manage_btn.grid(row=7, column=1,sticky=W,pady=(1,0))
 _canvas.create_line(0, 420, 211, 420, fill="black")
 Reset_btn=Button(_canvas,text="RESET\n     PASSWORD    >",command=lambda :CheckTheButton("reset"), font=("georgia", 14), bd=0,
                      activebackground="#2D3439", activeforeground="powder blue", bg="#2D3439", relief=FLAT, fg="white",
                      compound="left", height=2,width=16)
 Reset_btn.grid(row=8,column=1,pady=(1,0))
 _canvas.create_line(0, 480, 211, 480, fill="black")

 Logout_btn = Button(_canvas, text="    LOGOUT           >", command=lambda: _logout(FrameUnderCanvases),
                     font=("georgia", 14), bd=0,
                     activebackground="#2D3439", activeforeground="powder blue", bg="#2D3439", relief=FLAT, fg="white",
                     compound="left", height=2, width=16)
 Logout_btn.grid(row=9, column=1, pady=(1, 0))
 _canvas.create_line(0, 540, 211, 540, fill="black")

 dash_lbl.grid_propagate(0);report_lbl.grid_propagate(0);search_lbl.grid_propagate(0);account_lbl.grid_propagate(0);transaction_lbl.grid_propagate(0)
 logout_lbl.grid_propagate(0);Dashboard_btn.grid_propagate(0);Report_btn.grid_propagate(0);Reminder_btn.grid_propagate(0);Account_btn.grid_propagate(0)
 Manage_btn.grid_propagate(0);Logout_btn.grid_propagate(0);Search_btn.grid_propagate(0);budget_lbl.grid_propagate(0);Budget_btn.grid_propagate(0)
def split_into_list(data0):
    global all_data, transaction_amount, transaction_tag, transaction_description, transaction_date
    print(data0)
    transaction_date=data0[2].split(",")
    transaction_amount = data0[3].split(",")
    transaction_description = data0[4].split(",")
    transaction_tag= data0[5].split(",")
    # print(transaction_date)
def smtp(from_user,from_pwd,to_user,subject,message):
    # header = 'to:' + to_user + '\n' + 'From:' + from_user + '\n' + 'Subject:' + subject

    msg =  'Subject: {}\n\n{}'.format(subject,message)
    smtpObj = SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(from_user, from_pwd)
    smtpObj.sendmail(from_user, to_user, msg)
def SignIn(w,user,password):
    global username,all_data
    username=user.get()
    _pass=password.get()
    if username!='' and password!='':
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        if not EMAIL_REGEX.match(username):
            result = cursor.execute("select * from users where username='%s' and (password='%s' or forgot_password='%s')" % (username, _pass,_pass))
            if result == 1:
                cursor.execute("select name from users where username='%s'" % (username))
                name = cursor.fetchone()
                name=''.join(name)
                name=name.title()
                Manage(w, name)
                cursor.execute("update users set forgot_password =NULL where username='%s'" % (username))
                db.commit()
                null_or_not = cursor.execute(
                    "SELECT * FROM manage_expense WHERE date IS NULL and username='%s' " % (username))
                if null_or_not==0:
                    cursor.execute("select * from manage_expense where username='%s' " % (username))
                    all_data = list(cursor.fetchone())
                    split_into_list(all_data)

            else:
                messagebox.showerror("ERROR","Incorrect username or password.")
        else:
            result = cursor.execute("select * from users where email='%s' and (password='%s' or forgot_password='%s')" % (username, _pass,_pass))
            if result == 1:
                cursor.execute("select name from users where email='%s'" % (username))
                name=cursor.fetchone()
                name = ''.join(name)
                name = name.title()
                Manage(w,name)
                cursor.execute(
                    "update users set forgot_password =NULL where email='%s'" % (username))
                db.commit()
                cursor.execute("select username from users where email='%s'"%(username))
                _User_by_email=cursor.fetchone()
                null_or_not = cursor.execute(
                    "SELECT * FROM manage_expense WHERE date IS NULL and username='%s' " % (_User_by_email))
                if null_or_not == 0:
                    cursor.execute("select * from manage_expense where username='%s' " % (_User_by_email))
                    all_data = list(cursor.fetchone())
                    split_into_list(all_data)

            else:
                messagebox.showerror("ERROR","Incorrect email or password.")

    else:
        messagebox.showerror("","Both fields are necessary to get access.")
def forgot_password(user):
    username=user.get()
    if username!='':
        result=cursor.execute("select * from users where (username='%s' or email='%s')" % (username,username))
        if result==1:
            details=cursor.fetchone()
            to_user=''.join(details[3])
            name=''.join(details[1])
            print(details,to_user,name)
            new_password = str(random.randint(1, 9999))
            cursor.execute("update users set forgot_password ='%s' where (username='%s' or email='%s')"%(new_password,username,to_user))
            db.commit()
            message = "Hi " + name + ",\nYour OTP is: " + new_password + "\nReset your password after login"
            subject= "OTP"
            smtp("spri645@gmail.com", "priyanka@239", to_user,subject, message)
            messagebox.showinfo("SUCCESS", "We have mailed you an OTP.\nKindly resent after login.")
        else:
           messagebox.showerror("ERROR","The username or email does not match any account."
                                        "\nSign Up for an account.")
    else:
        messagebox.showerror("ERROR","Username or email is required.")
def SignUp(F_name,L_name,email,create_password):
    fname=F_name.get()
    lname=L_name.get()
    Email=email.get()
    password=create_password.get()

    result=cursor.execute("select * from users where email='%s'"%(Email))
    print(result)
    if result==1:
        messagebox.showerror("ERROR","Account already exists.")

    else:
        is_valid = validate_email(Email, verify=True)
        if (fname!='' and lname!='' and Email!='' and password!=''):
            if is_valid==True:
                if len(password)>=8:
                    username=Email.split("@")[0]
                    cursor.execute("insert into users(Name,username,email,password) values ('%s','%s','%s','%s')"%(fname+" "+lname,username,Email,password))
                    db.commit()
                    cursor.execute("INSERT INTO Manage_Expense (username) value ('%s')"%(username))
                    db.commit()
                    message="Hi "+fname+" "+lname+",\nYour Username is: "+username
                    subject="Username for expense tracker access"
                    smtp("spri645@gmail.com","priyanka@239",Email,subject,message)
                    messagebox.showinfo("SUCCESS","Successfully registered.\nWe have mailed you an username.")
                    F_name.delete(0,"end")
                    L_name.delete(0,"end")
                    email.delete(0,"end")
                    create_password.delete(0,"end")


                else:
                    messagebox.showwarning("ERROR","Minimum length of password should be 8 and maximum length should be 12.")
            else:
                messagebox.showerror("ERROR","Invalid email address.")
        else:
            messagebox.showerror("ERROR","Fill up all the fields.")
def _logout(canvas):

 canvas.destroy()
 root.title("Expense Manager")
 main_window()
def main_window():

 w = Canvas(root, width=1366, height=600,bd=0,highlightthickness=0)
 w.grid(row=1,column=0)
 w.grid_propagate(0)
 w.create_line(683, 100, 683, 500, fill="black")
 #w.create_line(0, 100, 200, 0, fill="red")
 #===================================FRAMES====================================================
 SignUpFrame=Frame(w,width=520,height=450)
 SignUpFrame.grid(row=0,column=0,padx=(90,0),pady=(80,0))

 SignInFrame=Frame(w,width=520,height=450)
 SignInFrame.grid(row=0,column=1,padx=(150,0),pady=(80,0))

 SignInFrame.grid_propagate(0)
 SignUpFrame.grid_propagate(0)

 #===================================SIGN UP===================================================
 SignUp_lbl=Label(SignUpFrame,text="Sign Up",font=("georgia",20,"bold"),fg="steel blue")
 SignUp_lbl.grid(row=0,column=1)

 s3 = Label(SignUpFrame, text="FIRST NAME :", font=('georgia', 11))
 s3.grid(row=2,column=0,pady=(50,0),padx=(40,0))

 F_name = Entry(SignUpFrame, font=('georgia', 11), bd=3, width=25)
 F_name.grid(row=2,column=1,pady=(50,0),padx=(30,0))

 s5 = Label(SignUpFrame, text="LAST NAME :", font=('georgia', 11))
 s5.grid(row=4,column=0,padx=(40,0),pady=(40,0))

 L_name = Entry(SignUpFrame, font=('georgia', 11), bd=3, width=25)
 L_name.grid(row=4,column=1,padx=(30,0),pady=(40,0))

 s6 = Label(SignUpFrame, text="EMAIL :", font=('georgia', 11))
 s6.grid(row=5,column=0,padx=(40,0),pady=(40,0))

 email = Entry(SignUpFrame, font=('georgia', 11), bd=3, width=25)
 email.grid(row=5,column=1,padx=(30,0),pady=(40,0))

 s7 = Label(SignUpFrame, text="CREATE A PASSWORD :", font=('georgia', 11))
 s7.grid(row=6,column=0,padx=(40,0),pady=(40,0))

 create_password= Entry(SignUpFrame, show="*",font=('georgia', 11), bd=3, width=25)
 create_password.grid(row=6,column=1,padx=(30,0),pady=(40,0))



 log_button = Button(SignUpFrame, text="REGISTER", bg="powder blue", width=25,relief=GROOVE,
                     command=lambda :SignUp(F_name,L_name,email,create_password))
 log_button.grid(row=7,column=1,padx=(0),pady=(40,0))


 #================= SIGN IN====================================================================

 SignIn_lbl=Label(SignInFrame,text="Sign In",font=("georgia",20,"bold"),fg="steel blue")
 SignIn_lbl.grid(row=0,column=1)

 s3 = Label(SignInFrame, text="EMAIL OR USERNAME : ", font=('georgia', 11))
 s3.grid(row=2,column=0,pady=(50,0))

 user = Entry(SignInFrame, font=('georgia', 11), bd=3, width=25)
 user.grid(row=2,column=1,pady=(50,0))

 s5 = Label(SignInFrame, text="PASSWORD :", font=('georgia', 11))
 s5.grid(row=4,column=0,padx=(0),pady=(40,0))

 password = Entry(SignInFrame, show="*", font=('georgia', 11), bd=3, width=25)
 password.grid(row=4,column=1,padx=(0),pady=(40,0))

 log_button = Button(SignInFrame, text="SIGN IN", bg="powder blue", width=25,relief=GROOVE,command=lambda :SignIn(w,user,password))
 log_button.grid(row=6,column=1,padx=(0),pady=(40,0))

 forgot_button = Button(SignInFrame, text="Forgot Password?",
                        command=lambda :forgot_password(user),activeforeground="steel blue", relief=FLAT,bd=0, width=15)
 forgot_button.grid(row=5,column=1,padx=(0),pady=(0))

 Label(SignInFrame, text="OR", font=('georgia', 14)).grid(row=8,column=1,padx=(0),pady=(40,0))

 image =PhotoImage(file="C:/Users/priyanka/Desktop/My Stuff/google+.png")
 Google_button = Button(SignInFrame, text=" |     "+"Sign in with GOOGLE+",image=image,font=("georgia",12),bd=1, activebackground="#DD4B39",activeforeground="white",bg="#DD4B39",relief=FLAT,fg="white",compound="left")
 Google_button.grid(row=9,column=1,padx=(0),pady=(40,0))

 root.mainloop()
root = Tk()
root.geometry("1366x768+0+0")
root.title("Expense Manager")
frame = Frame(root, width=1366, height=75, bg="#2D3439", relief=GROOVE, bd=1, highlightbackground="grey",
             )
frame.grid(row=0, column=0,sticky=W)
frame.grid_propagate(0)
Main_label = Label(frame, text="Expense Tracker", bg="#2D3439", font=("calibri", 21, "bold"), fg="White")
Main_label.grid(row=0, column=0, padx=10,pady=(10))

main_window()

