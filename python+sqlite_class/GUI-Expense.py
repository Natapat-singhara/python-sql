from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

##########SQL##########
import sqlite3
from datetime import datetime # นำไปไว้บนสุด
conn = sqlite3.connect('expense.sqlite3')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS expense (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                others TEXT,
                timestamp TEXT )""")
def insert_expense(title,price,others):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn:
        command = 'INSERT INTO expense VALUES (?,?,?,?,?)' # SQL
        c.execute(command,(None,title,price,others,ts))
    conn.commit() # save to database
    print('saved')
    
def view_expense():
    with conn:
        command = 'SELECT * FROM expense'
        c.execute(command)
        result = c.fetchall()
    return result

def update_expense(ID,field,newvalue):
    with conn:
        command = 'UPDATE expense SET {} = (?) WHERE ID = (?)'.format(field)
        c.execute(command,(newvalue,ID))
    conn.commit()

def update_table():
    table.delete(*table.get_children()) #Function Clear data in table.
    for row in view_expense():
        table.insert('','end',values=row)

def delete_expense(ID):
    with conn:
        command = 'DELETE FROM expense WHERE ID = (?)'
        c.execute(command,([ID])) #ถ้าเงื่อนไขมีตัวเดียวต้องใส่ [] เพิ่ม.เฉพาะ sqllite\
    conn.commit()


############ END SQL ###################

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช่จ่าย by ลุง')
GUI.geometry('700x600')

FONT1 = ('Angsana New',20)

######TAB######
PATH = os.getcwd() # check current folder

mainincon = os.path.join(PATH,'img\Sheep-CD.ico')
GUI.iconbitmap(mainincon)

Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH,expand=1)

T1 = Frame(Tab)
T2 = Frame(Tab)

icon_t1 = os.path.join(PATH,'img\Form-save-48.png')
icon_t2 = os.path.join(PATH,'img\History-64.png')
iconimage_T1 = PhotoImage(file=icon_t1)
iconimage_T2 = PhotoImage(file=icon_t2)

Tab.add(T1,text='บันทึกค่าใช้จ่าย',image=iconimage_T1,compound='left')
Tab.add(T2,text='ประวัติค่าใช้จ่าย',image=iconimage_T2,compound='left')

###############################

PATH = os.getcwd() # check current folder
icon = os.path.join(PATH,'img\Wallet-64.png')
iconimage = PhotoImage(file=icon)

L = Label(T1,image=iconimage)
L.pack()

L = Label(T1,text='โปรแกรมบันทึกค่าใช่จ่าย',font=('Angsana New',30))
L.pack(pady=10) #ทำให้ข้อความติดอยู่ตรงกลาง เรียงจากข้างบนลงล่าง

L = Label(T1,text='รายการ', font=FONT1)
L.pack()

V_title = StringVar()
E1 = ttk.Entry(T1,textvariable=V_title ,font=FONT1, width=50)
E1.pack()
###############################
L = Label(T1,text='ราคา', font=FONT1)
L.pack()
V_price = StringVar()
E2 = ttk.Entry(T1,textvariable=V_price ,font=FONT1, width=50)
E2.pack()
###############################
L = Label(T1,text='หมายเหตุ', font=FONT1)
L.pack()
V_others = StringVar()
E3 = ttk.Entry(T1,textvariable=V_others ,font=FONT1, width=50)
E3.pack()

def Save(event=None):
    
    if V_price.get()=='':
        E2.focus()
        messagebox.showinfo('ข้อมูลไม่ครบ','กรุณากรอกตัวเลขราคาด้วย')
    else:
        title = V_title.get() # ดึงค่ามาจาก V_title
        price = float(V_price.get())
        others = V_others.get()
        
        print(title, price, others)
        insert_expense(title, price, others)
        
        V_title.set('')
        V_price.set('')
        V_others.set('')
        E1.focus()
        update_table()
        
        # messagebox.showinfo('Message',title)

E3.bind('<Return>',Save) #ใส่ event=Note ในฟังก์ชั่น

B1 = ttk.Button(T1,text='SAVE',command=Save)
B1.pack(ipadx=20,ipady=10)

###############TAB2################

header = ['ID','รายการ','ค่าใช้จ่าย','หมายเหตุ','วัน-เวลา']
hwidth = [50,200,100,200,100]

table = ttk.Treeview(T2, columns=header,show='headings',height=20)
table.pack()

for h,w in zip(header,hwidth):
    table.heading(h,text=h)
    table.column(h,width=w)
    
# table.insert('','end',values=[1,'น้ำดื่ม',10,'ร้านป้าแดง','2024-10-19 15:15:10']) #ตัวอย่างของ Record


############### DELETE ################

def delete_table(event=None):
    try:
        print('delete..')
        select = table.selection()
        ID = table.item(select)['values'][0]
        choice = messagebox.askyesno('ลบข้อมูล','คุณต้องการลบข้อมูลใช่หรือไม่?')
        # print(choice) #Debug check
        if choice == True:
            delete_expense(ID)
            update_table()
    except Exception as e:
            print(e)
            messagebox.showwarning('แจ้งเตือน','กรุณาเลือกรายการที่ต้องการลบ')

table.bind('<Delete>',delete_table)

############### UPDATE ################

def update_data(event=None):
    try:

        select = table.selection()
        data = table.item(select)['values']
        print(data)
        
        GUI2 = Toplevel()
        GUI2.title('แก้ไขและบันทึกข้อมูล')
        GUI2.geometry('700x600')
        
        L = Label(GUI2,image=iconimage)
        L.pack()

        L = Label(GUI2,text='หน้าแก้ไขข้อมูล',font=('Angsana New',30))
        L.pack(pady=10) #ทำให้ข้อความติดอยู่ตรงกลาง เรียงจากข้างบนลงล่าง

        L = Label(GUI2,text='รายการ', font=FONT1)
        L.pack()

        V_title_update = StringVar()
        V_title_update.set(data[1])
        E1 = ttk.Entry(GUI2,textvariable=V_title_update ,font=FONT1, width=50)
        E1.pack()
        ###############################
        L = Label(GUI2,text='ราคา', font=FONT1)
        L.pack()
        V_price_update= StringVar()
        V_price_update.set(data[2])
        E2 = ttk.Entry(GUI2,textvariable=V_price_update ,font=FONT1, width=50)
        E2.pack()
        ###############################
        L = Label(GUI2,text='หมายเหตุ', font=FONT1)
        L.pack()
        V_others_update = StringVar()
        V_others_update.set(data[3])
        E3 = ttk.Entry(GUI2,textvariable=V_others_update ,font=FONT1, width=50)
        E3.pack()
        
        def Edit_data():
            ID = data[0]
            title_update = V_title_update.get()
            price_update = float(V_price_update.get())
            others_update = V_others_update.get()
            update_expense(ID,'title',title_update)
            update_expense(ID,'price',price_update)
            update_expense(ID,'others',others_update)
            update_table() #อัพเดทข้อมูลใหม่ใน Table เสมอ
            # print(title_update , price_update , others_update)
            GUI2.destroy()
            #ติด ยังแก้ไม่ได้ 5555
            
        
        B1 = ttk.Button(GUI2,text='SAVE',command=Edit_data)
        B1.pack(ipadx=20,ipady=10)
        # messagebox.showinfo('แจ้งเตือน','สำเร็จ')
        GUI2.mainloop

    except Exception as e:
            print(e)
            messagebox.showwarning('เลือกรายการ','กรุณาเลือกรายการที่ต้องการอัพเดท')


table.bind('<Double-1>',update_data)

update_table()
GUI.mainloop()
