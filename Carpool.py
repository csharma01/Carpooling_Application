#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import tkinter.ttk as ttk 
from ttkthemes import ThemedStyle
from tkinter.scrolledtext import ScrolledText
import sqlite3
from PIL import Image,ImageTk
from tkcalendar import *
import re
from babel.dates import format_date, parse_date, get_day_names, get_month_names
from babel.numbers import *
from tkinter import filedialog


# In[2]:


def profile_picture():
    global l,btn_changedp,img2,img
    con = sqlite3.connect(database = 'carpool.sqlite')
    cursor = con.cursor()
    cursor.execute(f"select path from path where user = '{user}'")
    imgpath = cursor.fetchall()
    con.close()
    
    img = Image.open(*imgpath[0]).resize((100,100))
    img2 = ImageTk.PhotoImage(img,master=frm)
    l = Label(frm,image=img2)
    l.photo = img2
    l.place(relx=.01,rely=.2)

def get_user():
    
    con=sqlite3.connect(database='carpool.sqlite')
    cursor = con.cursor()
    cursor.execute("select username from users")
    users = cursor.fetchall()
    con.close()

    for i in users:
        try:
            con=sqlite3.connect(database='carpool.sqlite', timeout=2)
            cursor = con.cursor()
            cursor.execute("insert into path(user) values(?)",(i[0],))
            print(i[0],"user added")
            con.commit()
            con.close()
        except Exception as e:
            con.close()
            print(e)
            pass

def browse():
#     global l2
    imgpath=filedialog.askopenfilename()
    print(imgpath,bool(imgpath))
    if imgpath == '':     
        pass
    else:
        con = sqlite3.connect(database = 'carpool.sqlite')
        cursor = con.cursor()
        cursor.execute(f"update path set path = '{imgpath}' where user = '{user}'")
        con.commit()
        con.close()

        img = Image.open(imgpath).resize((100,100))
        imgtk = ImageTk.PhotoImage(img)
        l2 = Label(frm,image=imgtk)
        l2.photo = imgtk
        l2.place(relx=.01,rely=.2)
    
def isValid(s):
    Pattern = re.compile("^\s*$|(0|91)?[6-9][0-9]{9}")
    return Pattern.match(s)

def check(email):
    regex = '^\s*$|^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?:[a-zA-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)$'
    return re.search(regex,email)

def reset():
    try:
        e_user.delete(0,"end")
        e_pass.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_user.focus()
    except:
        pass

def logout():
    frm.destroy()
    home_frame()


def back():
    frm.destroy()
    login_frame()

def create_frame():
    global frm
    frame_style = ttk.Style()
    frame_style2 = ttk.Style()
    frame_style2.configure('my2.TFrame', borderwidth = 3, background = "#CEEAFF")
    frame_style.configure('my.TFrame', borderwidth = 3,relief = GROOVE, background = "#CEEAFF")
    frm=ttk.Frame(app,style = 'my.TFrame')
    frm.place(x=400,y=300,relwidth=.5,relheight=.45)
    
    
def home_frame():
    global e_user,e_pass,e_mob,e_email,e_src,e_dest,e_model,e_regno
    create_frame()
    frm.place(x=400,y=300)
    
    def newuser():
        frm.destroy()
        newuser_frame()
            
    def login():
        global user
        user = e_user.get().upper()
        print(user)
        pwd = e_pass.get()
        con = sqlite3.connect(database = 'carpool.sqlite')
        cursor = con.cursor()
        cursor.execute("select * from users where username = ? and password = ?",(user,pwd))
        if cursor.fetchall():
            frm.destroy()
            login_frame()
        elif len(user) == 0 or len(pwd) == 0:
            messagebox.showerror("Error","Enter Username and Password!")
        else:
            messagebox.showerror("Login Failed","Invalid Info!")

    lbl_user=ttk.Label(frm,text="Username",font=('Helvetica',20,'bold'), background="#CEEAFF")
    lbl_pass=ttk.Label(frm,text="Password",font=('Helvetica',20,'bold'), background="#CEEAFF")
    e_user=ttk.Entry(frm, font=('Helvetica',20,'bold'))
    e_user.focus()
    e_pass=ttk.Entry(frm,style = 'my.TEntry',show="*", font=('Helvetica',20,'bold'))
    lbl_user.place(x=150,y=50)
    e_user.place(x=320,y=50)
    lbl_pass.place(x=150,y=130)
    e_pass.place(x=320,y=130)
  
    
    btn_login=ttk.Button(frm,text = "Login",style='my.TButton',command = login)
    btn_login.place(x=250,y=210)
    
    btn_reset=ttk.Button(frm,text = "Reset",style='my.TButton',command = reset)
    btn_reset.place(x=400,y=210)
    
    btn_new=ttk.Button(frm,text = "New User",style='my.TButton',width = 15, command = newuser)
    btn_new.place(x=300,y=280)

def newuser_frame():
    global e_user,e_pass,e_mob,e_email,e_src,e_dest,e_model,e_regno
    frm.destroy()
    create_frame()
    frm.place(x=400,y=200,relwidth=.5,relheight=.55)

    def reg_todb():
        username=e_user.get().upper()
        password=e_pass.get()
        mobile=e_mob.get().upper()
        email=e_email.get().lower()
        if(len(username)==0 or len(password)==0 or len(mobile)==0 or len(email)==0):
            messagebox.showerror('Empty',"Fields can't be Empty!")
        elif not isValid(mobile):
            messagebox.showerror('Validation','Please enter a valid Phone Number!')
        elif not check(email):
            messagebox.showerror('Validation','Please enter a valid Email Address!')
        else:
            try:
                con=sqlite3.connect(database="carpool.sqlite")
                cursor=con.cursor()
                cursor.execute("insert into users values(?,?,?,?)",(username,password,mobile,email))
                con.commit()
                con.close()
                messagebox.showinfo("Registration","Registration Done!\nLogin using your credentials!")
                get_user()
                frm.destroy()
                home_frame()
                
            except Exception as e:
                messagebox.showerror("Registration","Username already exists!")
                print(e)
        
    def back():
        frm.destroy()
        home_frame()

    lbl_user=ttk.Label(frm,text="Username",font = ('Helvetica',20,'bold'),background="#CEEAFF")
    lbl_pass=ttk.Label(frm,text="Password",font=('Helvetica',20,'bold'),background="#CEEAFF")
    lbl_mob=ttk.Label(frm,text="Mobile",font=('Helvetica',20,'bold'),background="#CEEAFF")
    lbl_email=ttk.Label(frm,text="Email",font=('Helvetica',20,'bold'),background="#CEEAFF")
    
    e_user=ttk.Entry(frm,font=('Helvetica',20,'bold'))
    e_user.focus()
    e_pass=ttk.Entry(frm,font=('Helvetica',20,'bold'),show="*")
    e_mob=ttk.Entry(frm,font=('Helvetica',20,'bold'))
    e_email=ttk.Entry(frm,font=('Helvetica',20,'bold'))
        
    lbl_user.place(x=150,y=50)
    e_user.place(x=320,y=50)
    lbl_pass.place(x=150,y=130)
    e_pass.place(x=320,y=130)
    lbl_mob.place(x=150,y=210)
    e_mob.place(x=320,y=210)
    lbl_email.place(x=150,y=290)
    e_email.place(x=320,y=290)

    btn_reg=ttk.Button(frm,text = 'Register',style='my.TButton',command = reg_todb)
    btn_reg.place(x=250,y=370)
    
    btn_reset=ttk.Button(frm,text = 'Reset',style = 'my.TButton',command = reset)
    btn_reset.place(x=420,y=370)
    
    btn_back=ttk.Button(frm,text = "Back",style = 'my2.TButton',width=5,command = back)
    btn_back.place(relx=0.01,rely=.1)

    
def login_frame():
    create_frame()
    frm.place(x=300,y=200,relwidth=.65,relheight=.55)
    profile_picture()
    btn_changedp = ttk.Button(frm,text = 'Change Dp',style = "my2.TButton",command = browse) 
    btn_changedp.place(relx=.01,rely=.45)

        
    def search():
        frm.destroy()
        searchpool_frame()
        
    def create():
        frm.destroy()
        createpool_frame()    
     
    def update():
        frm.destroy()
        updateprofile_frame()
        
    lbl_wel=ttk.Label(frm,text=f"Welcome, {user.lower()}",font=('Helvetica',10,'bold'), background = "#CEEAFF")
    lbl_wel.place(x=5,y=5)
    
    btn_logout=ttk.Button(frm,text = "Logout",style='my2.TButton',width=7,command = logout)
    btn_logout.place(relx=.89,rely=0.02)
    
    btn_search=ttk.Button(frm,text="Search Pool",style = 'my.TButton',width=20,command=search)
    btn_search.place(relx=.35,rely=.25)
    
    btn_create=ttk.Button(frm,text="Create Pool",style = 'my.TButton',width=20,command=create)
    btn_create.place(relx=.35,rely=.45)

    btn_profile=ttk.Button(frm,text="Update profile",style = 'my.TButton',width=20,command=update)
    btn_profile.place(relx=.35,rely=.65)
    
    
def searchpool_frame():
    global e_src,e_dest
    def show():
        src = e_src.get().upper()
        dest = e_dest.get().upper()
        con = sqlite3.connect(database = 'carpool.sqlite')
        cursor = con.cursor()
        cursor.execute("select * from cars where src = ? and dest = ?",(src,dest))
        pools = cursor.fetchall()
        pools.reverse()
        con.close()
        if len(src)==0 or len(dest) == 0:
            messagebox.showerror("Empty","No Input Detected!")
        elif len(pools) == 0:
            messagebox.showerror("Error","No Pools found!")
        else:
            
            img.resize((70,70))
            l.place(relx=.1,rely=.01)

            frm.place(x=30,y=170,relwidth=.97,relheight=.70)
            scroll_style = ttk.Style()
            scroll_style.configure('Vertical.TScrollbar',background = "#CEEAFF")
            frm2 = ttk.Frame(frm,style='my2.TFrame')
            frm2.place(x=35,y=160,relwidth=.96,relheight=.55)
            st=Text(frm2,width=175,font=('Helvetica',11,'bold'),bg = "#CEEAFF",pady=10)
            st.pack(side='left',fill='both')
            vsb = ttk.Scrollbar(frm2, command=st.yview, orient="vertical",style = 'Vertical.TScrollbar')
            st.configure(yscrollcommand=vsb.set)
            vsb.pack(side = "right",fill='y')
            
            st.insert("end","  Username\t\tMobile\t\tEmail\t\t  Source\t\tDestination\t\tCar Number\t\tModel\t\tSeat Capacity\t\tFuel Type\t\tStart Time\t\tReturn Time")
            for pool in range(len(pools)):
                con = sqlite3.connect(database = 'carpool.sqlite')
                cursor = con.cursor()
                cursor.execute(f"select mobile,email from users where username = '{pools[pool][0]}'")
                users = cursor.fetchall()
                st.insert("end",f"\n\n  {pools[pool][0]}\t\t{users[0][0]}\t\t{users[0][1]}\t\t   {pools[pool][1]}\t\t{pools[pool][2]}\t\t{pools[pool][3]}\t\t{pools[pool][4]}\t\t          {pools[pool][5]}\t\t{pools[pool][6]}\t\t{pools[pool][7]}\t\t{pools[pool][8]}","config")
                st.tag_config('config',foreground='red',font = ('Helvetica',10))
                con.close()
            st.config(state = 'disabled')

            btn_search=ttk.Button(frm,text = "Search",style = 'my2.TButton',command = show, width = 6.2)
            btn_search.place(relx=.89,rely=.2)
        
    create_frame()
    frm.place(x=300,y=200,relwidth=.65,relheight=.55)
    
    welcome_screen() 
    profile_picture()
    lbl_src=ttk.Label(frm,text="Source",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_src.place(relx=.2,rely=.2)
   
    e_src=ttk.Entry(frm, font=('Helvetica',10,'bold'))
    e_src.focus()
    e_src.place(relx=.31,rely=.2)
    
    lbl_dest=ttk.Label(frm,text="Destination",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_dest.place(relx=.52,rely=.2)
   
    e_dest=ttk.Entry(frm, font=('Helvetica',10,'bold'))
    e_dest.place(relx=.68,rely=.2)
    
    btn_search=ttk.Button(frm,text = "Search",style = 'my.TButton',command = show)
    btn_search.place(relx=.42,rely=.39)
    
def welcome_screen():
    lbl_wel=ttk.Label(frm,text=f"Welcome, {user.lower()}",font=('Helvetica',10,'bold'), background = "#CEEAFF")
    lbl_wel.place(x=5,y=5)
    
    
    btn_logout=ttk.Button(frm,text = "Logout",style='my2.TButton',width=7,command = logout)
    btn_logout.place(relx=.89,rely=0.02)
  

    btn_back=ttk.Button(frm,text = "Back",style = 'my2.TButton',width=5,command = back)
    btn_back.place(relx=0.01,rely=.1)
    

def createpool_frame():
    global e_src,e_dest,e_model,e_regno,cb_fueltype,cb_seat,btn_starttime,btn_endtime,e_endtime,e_starttime
    def submit(): 
        src = e_src.get().upper()
        dest = e_dest.get().upper()
        model = e_model.get().upper()
        regno = e_regno.get().upper()
        fuel = cb_fueltype.get().upper()
        seats = cb_seat.get().upper()
        start_time = e_starttime.get().upper()
        end_time = e_endtime.get().upper()
        if len(src) == 0 or len(dest) == 0 or len(model) == 0 or len(regno) == 0 or len(start_time) == 0 or len(end_time) == 0:
            messagebox.showerror("Empty","Fields can't be Empty!")
        elif end_time < start_time:
            messagebox.showerror("Validation","End cannot be less than Start!")
        else:
            try:
                con = sqlite3.connect(database='carpool.sqlite')
                cursor = con.cursor()
                cursor.execute("insert into cars values(?,?,?,?,?,?,?,?,?)",(user,src,dest,regno,model,seats,fuel,start_time,end_time))
                con.commit()
                con.close()
                messagebox.showinfo("SUCCESS","Pool Created Successfully!")
            except Exception as e:
                messagebox.showinfo("Failed!","Car already registered in the pool!")

    def reset():
        e_src.delete(0,"end")
        e_dest.delete(0,"end")
        e_model.delete(0,"end")
        e_regno.delete(0,"end")
        cb_fueltype.delete(0,"end")
        cb_seat.delete(0,"end")
    
    create_frame()
    frm.place(x=300,y=200,relwidth=.65,relheight=.55)
    
    frm2_style = ttk.Style()
    frm2_style.configure('frm2.TFrame',background = "#CEEAFF")
    frm2 = ttk.Frame(frm,style = 'frm2.TFrame')
    frm2.place(x=200,y=100,relwidth=.7,relheight=.7)
    
    welcome_screen()
    profile_picture()

    lbl_src=ttk.Label(frm2,text="Source",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_src.grid(row=0,column=0,pady=4,sticky=W)
   
    e_src=ttk.Entry(frm2, font=('Helvetica',10))
    e_src.focus()
    e_src.grid(row=0,column=1,pady=4,padx=4)
    
    
    lbl_dest=ttk.Label(frm2,text="Destination",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_dest.grid(row=0,column=4,pady=4,sticky=W)
    
    e_dest=ttk.Entry(frm2,style='my.TEntry')
    e_dest.grid(row=0,column=5,pady=4,padx=4)
    
    
    
    lbl_model=Label(frm2,text="Car Model",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_model.grid(row=1,column=0,pady=10,sticky=W)
    
    e_model=ttk.Entry(frm2,style='my.TEntry')
    e_model.grid(row=1,column=1,pady=4)
    
    lbl_seat=Label(frm2,text="Seats",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_seat.grid(row=1,column=4,pady=4,sticky=W)
    
    cb_seat=ttk.Combobox(frm2,values=[2,3,4,5,6,7],style = 'my.TCombobox', background = "#CEEAFF")
    cb_seat.current(3)
    cb_seat.grid(row=1,column=5,pady=4)
    
    lbl_regno=Label(frm2,text="Car Regno",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_regno.grid(row=2,column=0,pady=20,sticky=W)
    
    e_regno=ttk.Entry(frm2,style='my.TEntry')
    e_regno.grid(row=2,column=1,pady=4)
    
    lbl_fueltype=Label(frm2,text="Fuel Type",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_fueltype.grid(row=2,column=4,pady=4,sticky=W)
    
    cb_fueltype=ttk.Combobox(frm2,values=['Petrol','Diesel','Petrol+CNG','Petrol+LPG','Electric'],style = 'my.TCombobox', background = "#CEEAFF")
    cb_fueltype.current(0)
    cb_fueltype.grid(row=2,column=5,pady=4)
    
    lbl_starttime = Label(frm2,text="Start Date/Time",font=('Helvetica',17,'bold'), background = "#CEEAFF")
    lbl_starttime.grid(row=3,column=0,pady=4,sticky=W)
    
    e_starttime = ttk.Entry(frm2,style='my.TEntry',width = 15,state='disabled')
    e_starttime.grid(row = 3, column = 1,pady=4,padx= 4,sticky = W)
    
    lbl_endtime = Label(frm2,text="End Date/Time",font=('Helvetica',17,'bold'), background = "#CEEAFF") 
    lbl_endtime.grid(row=3,column=4,pady=4,sticky=E)
    
    e_endtime = ttk.Entry(frm2,style='my.TEntry',width = 15,state='disabled')
    e_endtime.grid(row = 3, column = 5,pady=4,padx= 4,sticky=W)
    
    btn_starttime = ttk.Button(frm,text = "Set",style = 'my3.TButton', command = set_datetime,image = cal_img)
    btn_starttime.place(relx=.5,rely=.616)
    btn_endtime = ttk.Button(frm,text = "Set",style = 'my3.TButton', command = end_datetime,image = cal_img)
    btn_endtime.place(relx=.828,rely=.616)
    
    btn_submit=ttk.Button(frm,text = "Submit",style = 'my.TButton',command=submit)
    btn_submit.place(relx=.35,rely=.8)
    
    btn_reset=ttk.Button(frm,text = 'Reset', style = 'my.TButton',command = reset)
    btn_reset.place(relx=.5,rely=.8)
    
def updateprofile_frame():
    newuser_frame()
    frm.place(x=300,y=200,relwidth=.65,relheight=.55)
    welcome_screen()
    profile_picture()
    def reg_todb():
        global password,mobile,email
        password=e_pass.get()
        mobile=e_mob.get().upper()
        email=e_email.get().lower()
        
        if len(password) == 0 and len(mobile) == 0 and len(email) == 0:
            messagebox.showerror("Empty","Fields can't be Empty!")
        elif check(email) is None:
            messagebox.showerror("Validation","Enter a valid Email Address!")
        elif isValid(mobile) is None:
            messagebox.showerror("Validation","Enter a valid Mobile Number!")
        else:
            my_dict = {'password':password,'mobile':mobile,'email':email}
            keys = list(my_dict.keys())
            values = list(my_dict.values())
            con = sqlite3.connect(database='carpool.sqlite')
            cursor = con.cursor()
            for i in values:
                if bool(i)==True:
                    cursor.execute(f"update users set '{keys[values.index(f'{i}')]}' = '{values[values.index(f'{i}')]}' where username = '{user}' ")
                    con.commit()
            con.close()
            messagebox.showinfo("Success","Updated!")
            
    con = sqlite3.connect(database='carpool.sqlite')
    cursor = con.cursor()
    cursor.execute(f"select password,mobile,email from users where username = '{user}'")
    details = cursor.fetchall()
    con.close()
    pwd = details[0][0]
    mob = details[0][1]
    e = details[0][2]
    
    
    e_user.insert("end",f"{user}")
    e_user.config(state="disabled")
    e_pass.insert("end",f"{pwd}")
    e_pass.config(show="*")
    e_mob.insert("end",f"{mob}")
    e_email.insert("end",f"{e}")
    
    btn_reg=ttk.Button(frm,text = 'Update',style='my.TButton',command = reg_todb)
    btn_reg.place(x=250,y=370)
    
    
def date_time_picker():
    global ws,min_sb,sec,cal,sec_hour
    ws = Tk()
    ws.title("Set Date")
    ws.geometry("290x360")
    style = ThemedStyle(ws)
    style.set_theme("breeze")
    ws.config(bg="#CEEAFF")
    cal_image = PhotoImage(file = "images/cal_icon.png")
    cal_img = cal_image.subsample(11, 11)
    hour_string=StringVar()
    min_string=StringVar()
    last_value_sec = ""
    last_value = ""        
    f = ('Helvetica', 20)
    if last_value == "59" and min_string.get() == "0":
        hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)   
        last_value = min_string.get()

    if last_value_sec == "59" and sec_hour.get() == "0":
        min_string.set(int(min_string.get())+1 if min_string.get() !="59" else 0)
    if last_value == "59":
        hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)            
        last_value_sec = sec_hour.get()

    fone = Frame(ws)
    ftwo = Frame(ws)

    fone.pack(pady=10)
    ftwo.pack(pady=10)

    cal = Calendar(
        fone, 
        selectmode="day"
        )
    cal.pack()

    min_sb = Spinbox(
        ftwo,
        from_=0,
        to=23,
        wrap=True,
        textvariable=hour_string,
        width=2,
        state="readonly",
        font=f,
        justify=CENTER
        )
    sec_hour = Spinbox(
        ftwo,
        from_=0,
        to=59,
        wrap=True,
        textvariable=min_string,
        font=f,
        width=2,
        justify=CENTER
        )

    sec = Spinbox(
        ftwo,
        from_=0,
        to=59,
        wrap=True,
        textvariable=sec_hour,
        width=2,
        font=f,
        justify=CENTER
        )

    min_sb.pack(side=LEFT, fill=X, expand=True)
    sec_hour.pack(side=LEFT, fill=X, expand=True)
    sec.pack(side=LEFT, fill=X, expand=True)

    msg = Label(
        ws, 
        text="Hour  Minute  Seconds",
        font=("Times", 12),
        bg="#CEEAFF"
        )
    msg.pack(side=TOP)
    

def set_datetime():
    global start
    btn_starttime.config(state = 'disabled',image = cal_img)
    btn_endtime.config(state = 'disabled')
    date_time_picker()
    
    def assign():
        global start
        e_starttime.config(state='normal')
        date = cal.get_date()
        m = min_sb.get()
        h = sec_hour.get()
        s = sec.get()
        e_starttime.delete(0,"end")
        e_starttime.insert("end",f"{date} {m}:{h}:{s}")
        start = date + h + m + s
        ws.destroy()
        e_starttime.config(state = 'disabled')
        btn_starttime.config(state='normal')
        btn_endtime.config(state='normal')
    btn_set = ttk.Button(
        ws,
        text="Set",
        style = 'my.TButton',
        command=assign
    )
    btn_set.pack(pady=10)
    
    def on_closing():
        ws.destroy()
        btn_starttime.config(state = 'normal')
        btn_endtime.config(state='normal')
        
    ws.protocol("WM_DELETE_WINDOW", on_closing)
    ws.mainloop()
    
    
def end_datetime():
    btn_endtime.config(state='disabled',image = cal_img)
    btn_starttime.config(state='disabled')
    date_time_picker()
    def assign():
        e_endtime.config(state='normal')
        date = cal.get_date()
        m = min_sb.get()
        h = sec_hour.get()
        s = sec.get()
        end = date + m + h + s
        try: 
            if end < start or end == start:
                messagebox.showerror("Invalid date","End date must be greater than start date!")
                e_endtime.config(state='disabled')
            else:
                ws.destroy()
                e_endtime.delete(0,"end")
                e_endtime.insert("end",f"{date} {m}:{h}:{s}")
                e_endtime.config(state='disabled')
                btn_endtime.config(state='normal')
                btn_starttime.config(state='normal')
        except Exception as e:
            print(e)
            

    btn_set = ttk.Button(
        ws,
        text="Set",
        style = 'my.TButton',
        command=assign
    )
    btn_set.pack(pady=10)
    
    def on_closing():
        ws.destroy()
        btn_endtime.config(state = 'normal')
        btn_starttime.config(state='normal')
    
    ws.protocol("WM_DELETE_WINDOW", on_closing)
    ws.mainloop()


# In[3]:


app = Tk()
app.state("zoomed")
app.title("Carpooling Project")
#Setting Theme
style = ThemedStyle(app)
style.set_theme("breeze")
app.configure(bg="#CEEAFF")
#Setting Styles
entry_style = ttk.Style()
entry_style.configure('my.TEntry', font=('Helvetica',20,'bold'))

button_style = ttk.Style()
button_style.configure('my.TButton', font=('Helvetica', 15,'bold'))
button_style_2 = ttk.Style()
button_style_2.configure('my2.TButton', font=('Helvetica',10,'bold'))
button_style_3 = ttk.Style()
button_style_3.configure('my3.TButton', font=('Helvetica',7,'bold'),width=2,padding = 0)
btn_change_dp = ttk.Style()
lbl_title=ttk.Label(app,text="Car Pooling",font=('',90,'bold','underline'),foreground="#065285",background = "#CEEAFF")
lbl_title.pack()
combo_style = ttk.Style()
combo_style.configure('my.TCombobox',font=('Helvetica',20,'bold'))
#Home_Page Pictures
carpool_img=Image.open("images/cp4.jpg").resize((400,150))
carpool_imgtk=ImageTk.PhotoImage(carpool_img,master=app)
carpool_lbl_img=Label(app,image=carpool_imgtk,borderwidth=2, relief="solid")
carpool_lbl_img.place(relx=.001,rely=0)
carpool_img2=Image.open("images/cp2.jpg").resize((400,150))
carpool_imgtk2=ImageTk.PhotoImage(carpool_img2,master=app)
carpool_lbl_img2=Label(app,image=carpool_imgtk2,borderwidth=2, relief="solid")
carpool_lbl_img2.place(relx=.747,rely=0)
#Calander Icon
cal_image = PhotoImage(file = "images/cal_icon.png")
cal_img = cal_image.subsample(11, 11)


# In[4]:


home_frame()
app.mainloop()

