import sqlite3

# เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect('expense.sqlite3')
# ตัวดำเนินการ
c = conn.cursor()

# สร้างตารางชื่อ expense
c.execute("""CREATE TABLE IF NOT EXISTS expense (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    price REAL,
                    others TEXT,
                    timestamp TEXT )""")

# ทดลอง insert ข้อมูล
from datetime import datetime # นำเข้าฟังกชั่น

def insert_expense(title,price,others):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn:
        command = 'INSERT INTO expense VALUES (?,?,?,?,?)' #SQL
        # c.execute(command,(None,'อาหารเช้า',20,'ข้าวต้ม','2024-10-12 15:15:40'))
        c.execute(command,(None,title,price,others,ts))
    conn.commit() # save to database , ถ้ามีการแก้ไขใน DB ให้มี commit | View or select ไม่ต้องมี
    print('saved')
    
# insert_expense('ไข่ล้วก',50,'ร้านป้าศรี') #ดั้มข้อมูล
# print('###########โปรแกรมค่าใช้จ่ายประจำวัน#######')
# for i in range(3):
#     print('###########{}#######'.format(i+1)) #.format ใช้าำหรับข้อความเท่านั้น
#     title = input('รายการ: ')
#     prcie = float(input('ราคา: ')) # float โปรแกรมแปลงค่า ทศนิยม
#     others = input('หมายเหตุ: ')
#     insert_expense(title,prcie,others)

def view_exprnse():
    with conn:
        command = 'SELECT * FROM expense'
        # command = 'SELECT title, price FROM expense'
        c.execute(command)
        result = c.fetchall()
    # print(result)
    return result

#ฟังก์ชั่นดึงดาต้าออกมาแสดงจากการ return ค่าของฟังก์ชั่น view_exprnse
# data = view_exprnse() 
# for d in data:
#     print(d[1:3]) #ทำการ sliding ด้วยการเลือก index ที่ต้องการ

def update_expense(ID,field,newvalue):
    with conn:
        command = 'UPDATE expense SET {} = (?) WHERE ID = (?)'.format(field)
        c.execute(command,(newvalue,ID))
    conn.commit()
    
#ID ของข้อมูล , หัวข้อ ใน DB , result ที่อยากให้ออก    
# update_expense(1,'others','ลุงศร')
update_expense(4,'title','ชาเขียวปั่นโอริโอ้')

def delete_expense(ID):
    with conn:
        command = 'DELETE FROM expense WHERE ID = (?)'
        c.execute(command,([ID])) #ถ้าเงื่อนไขมีตัวเดียวต้องใส่ [] เพิ่ม.เฉพาะ sqllite\
    conn.commit()
    
delete_expense(6)

data = view_exprnse() 
for d in data:
    print(d)