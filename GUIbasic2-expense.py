
from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย V.1.0 by Nakin')
GUI.geometry('700x900+600+0')

# ---------------MENU-------------------
menubar = Menu(GUI)
GUI.config(menu=menubar)

# file menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import csv')
filemenu.add_command(label='Export to Googlesheet')

def Abount():
    print('Abount Menu')
    messagebox.showinfo('Abount','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ขอ 1 BTC ก็พอแล้ว\nBTC Address:abc')


helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='Abount',command=Abount)

def Donate():
    messagebox.showinfo('Donate','XRP Address:rpXTzCuXtjiPDFysxq8uNmtZBe9Xo97JbW\nXRP Deposit Tag:1023997855')    


donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
donatemenu.add_command(label='Donate',command=Donate)







Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)

Tab.pack(fill=BOTH,expand=1)

roob1=PhotoImage(file='Gold.png').subsample(44)
roob2=PhotoImage(file='Gold2.png').subsample(5)
roob3=PhotoImage(file='Eye.png').subsample(7)


Tab.add(T1,text=f'{"Add expense":^{30}}',image=roob1,compound='top')
Tab.add(T2,text=f'{"Expense list":^{30}}',image=roob2,compound='top')



F1 =Frame(T1)
F1.pack()
days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'วันเสาร์',
        'Sun':'อาทิตย์'}


def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    geeaun = v_geeaun.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกราคา')    
        return
    elif geeaun == '':
        geeaun = 1

    try:
        lakartungmod = float(price)*float(geeaun)
        print('รายการ: {} ราคา: {} จำนวน: {} ราคารวม {} '.format(expense,price,geeaun,lakartungmod))
        text ='รายการ: {} ราคา: {} จำนวน: {} ราคารวม {}\n '.format(expense,price,geeaun,lakartungmod)
        today = datetime.now().strftime('%a')
        dt = datetime.now().strftime('%d-%m-%Y-{} %H:%M:%S'.format(days[today]))
        text= text+dt
        v_result.set(text)

        v_expense.set('')
        v_price.set('')
        v_geeaun.set('')
        today = datetime.now().strftime('%a')
        dt = datetime.now().strftime('%d-%m-%Y-{} %H:%M:%S'.format(days[today]))
        print(dt)
        
        with open('savedata.csv','a',encoding='utf-8',newline='') as f:
            fw = csv.writer(f)
            data = [dt,expense,price,geeaun,lakartungmod]
            fw.writerow(data)         

        E1.focus()
        update_table()
    except Exception as e:

        print('ERROR:',e)    
        messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        v_expense.set('')
        v_price.set('')
        v_geeaun.set('')

GUI.bind('<Return>',Save)        

FONT1 = (None,20)

bg = PhotoImage(file='city.png').subsample(7)
citypic = ttk.Label(F1, image=bg)
citypic.pack()

#----------------text1-------------
L = ttk.Label(F1,text = 'รายการค่าใช้จ่าย',font =FONT1).pack()
v_expense =StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#----------------------------------

#----------------text2-------------
L = ttk.Label(F1,text = 'ราคา(บาท)',font =FONT1).pack()
v_price =StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#----------------------------------
#------------------text3--------------------
L = ttk.Label(F1,text = 'จำนวน(ชิ้น)',font =FONT1).pack()
v_geeaun =StringVar()
E3 = ttk.Entry(F1,textvariable=v_geeaun,font=FONT1)
E3.pack()


B2 = ttk.Button(F1,text='Save',image=roob3,compound='top',command=Save)
B2.pack(ipadx=20,ipady=20,pady = 10)

v_result = StringVar()
v_result.set('---------ผลลัพธ์---------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)

#-------------------Tab2---------------------

def read_csv():
    with open('savedata.csv',newline ='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data    
        
#table

L = ttk.Label(T2,text = 'ตารางแสงผลลัพธ์ทั้งหมด',font =FONT1).pack(pady=20)


header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show ='headings',height =20)
resulttable.pack()

for h in header:
    resulttable.heading(h,text = h)

headerwidth = [150,170,80,80,80]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width = w)


def update_table():
    resulttable.delete(*resulttable.get_children())
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()    

GUI.mainloop()
