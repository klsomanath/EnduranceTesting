import tkinter as tk
from tkinter import ttk
from tkinter import *
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import time
import TempHumidity
import threading
from PIL import ImageTk, Image, ImageSequence
import datetime
import Temp
import Press
import dataBase
import sqlite3
import csv
global row_num,end_txt
row_num=0
global data
global sensor_data
global flag, temp,pressure,stop,itr_time,sv013,sv02
itr_time=2
flag = 0
stop = False
sensor_data = []
window=tk.Tk()
window.state('zoomed')
window.title("System ON/OFF Controller")
window.grid_propagate(True)
## ------------------------------------ Header Frame -----------------------------------------------------

frame_header = tk.Frame(window, border=4, relief="ridge")
frame_header.place(relx=0, rely=0, relwidth=1, relheight=1/8)

frame_header.grid_propagate(True)

Header = tk.Label(frame_header,text="Nucon Aerospace Private Limited - Hyderabad",font=("Arial", 16,'bold'),foreground="Black")
Header.grid(row=0,column=0,sticky="e")

Header2 = tk.Label(frame_header,text="Endurance Testing",font=("Arial", 14,'bold'),foreground="Black")
Header2.grid(row=1,column=0)

img = Image.open("NuconLogo.png")
img = ImageTk.PhotoImage(img,master=frame_header)
img_label = tk.Label(frame_header,image = img)
img_label.image = img
img_label.grid(row=0,column=1)

now = datetime.datetime.now().strftime('%d-%m-%Y')
Date_Label = tk.Label(frame_header, text=now,font=("Arial", 12,'bold'))
Date_Label.grid(row=1,column=1)

frame_header.rowconfigure(list(range(2)), weight = 1, uniform="Silent_Creme")
frame_header.columnconfigure(list(range(2)), weight = 1, uniform="Silent_Creme")
fault=[]
## --------------------- Header Frame ---------------------------------------------

## --------------------- Frame 1 ---------------------------------------------------
def systemOn():
    SystemOn.config(state=tk.DISABLED)
    CumCycleDownload.config(state=tk.DISABLED)
    global stop
    stop = False
    SystemOff.config(state=tk.NORMAL)
    disp_temp()
    return
def checkPress(press1,press2,i):
    if (press1/i < 1 or press1/i > 5):
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=1,column=3)
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=5,column=4)
        fault.append(5)
        info_box.configure(state="normal")
        info_box.insert(tk.END, f"Faulty Pressure Sensor 1 Please Check Wiring !!!\n\n")
        info_box.see(tk.END)
        info_box.configure(state="disabled")
    if (press2/i < 1 or press2/i > 5):
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=1,column=3)
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=7,column=4)
        fault.append(7)
        info_box.configure(state="normal")
        info_box.insert(tk.END, f"Faulty Pressure Sensor 2 Please Check Wiring !!!\n\n")
        info_box.see(tk.END)
        info_box.configure(state="disabled")
def checkTemp(temp1,temp2,i):
    if (temp1/i < 35 or temp1/i > 40):
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=1,column=3)
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=4,column=4)
        fault.append(4)
        info_box.configure(state="normal")
        info_box.insert(tk.END, f"Faulty Temparature Sensor 1 Please Check Wiring !!!\n\n")
        info_box.see(tk.END)
        info_box.configure(state="disabled")
    if (temp2/i < 35 or temp2/i > 40):
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=1,column=3)
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=6,column=4)
        fault.append(6)
        info_box.configure(state="normal")
        info_box.insert(tk.END, f"Faulty Temparature Sensor 2 Please Check Wiring !!!\n\n")
        info_box.see(tk.END)
        info_box.configure(state="disabled")
def checkTempPress(temp13,press13,temp23,press23,i):
    if (temp13/i >= 35 and temp13/i <= 40) and (temp23/i >= 35 and temp23/i <= 40):
        if (press13/i >= 1 and press13/i <= 5) and (press23/i >= 1 and press23/i <= 5):
            enable=1
            Pass_Label = tk.Label(frame1, text="PASS",font=("Arial", 10,'bold'),foreground="GREEN")
            Pass_Label.grid(row=1,column=3)
        else:
            enable=0
            checkTemp(temp13,temp23,i)
            checkPress(press13,press23,i)
            Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
            Pass_Label.grid(row=1,column=3)
            SystemOff.config(state=tk.NORMAL)
            CycleOn.config(state=tk.DISABLED)
            CycleOff.config(state=tk.DISABLED)
            SystemOn.config(state=tk.DISABLED)
    else:
        enable=0
        checkTemp(temp13,temp23,i)
        checkPress(press13,press23,i)
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=1,column=3)
        SystemOff.config(state=tk.NORMAL)
        CycleOn.config(state=tk.DISABLED)
        CycleOff.config(state=tk.DISABLED)
        SystemOn.config(state=tk.DISABLED)
    return enable
def checkDHT22(temp,humid):
    enable1=0
    if (temp >= 35 and temp <= 40) and (humid >= 50 and humid <= 70):
        enable1=1
    else:
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=2,column=4)
        Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
        Pass_Label.grid(row=3,column=4)
        info_box.configure(state="normal")
        info_box.insert(tk.END, f"Faulty DHT22 Sensor Please Check Wiring !!!\n\n")
        info_box.see(tk.END)
        info_box.configure(state="disabled")
        SystemOff.config(state=tk.NORMAL)
        CycleOn.config(state=tk.DISABLED)
        CycleOff.config(state=tk.DISABLED)
        SystemOn.config(state=tk.DISABLED)
    return enable1
def disp_temp():
    enable=0
    temp11=temp13=temp23=press13=press23=0
    humid1=0
    for _ in range(2):
        if stop == True:
            return
        time.sleep(1)
        temp,humidity=TempHumidity.getTempHumidity()
        temp11+=float(temp)
        temp = str(temp)+"\N{DEGREE SIGN}C"
        humid1+=float(humidity)
        humidity = str(humidity) + " mg"

        temp_val = tk.Label(frame1, text=temp, font=("Arial",10,'bold'),foreground="Black")
        temp_val.grid(row=2, column=3)

        humidity_val = tk.Label(frame1, text=humidity, font=("Arial", 10,'bold'),foreground="Black")
        humidity_val.grid(row=3, column=3)

        temp1=Temp.getTemp1()
        temp13+=temp1
        temp2=Temp.getTemp2()
        temp23+=temp2
        press1=Press.getPress1()
        press13+=press1
        press2=Press.getPress2()
        press23+=press2
        #temp13=temp23=76
        # press13=press23=6
        temp_label1 = tk.Label(frame1, text=temp1, font=("Arial",10,'bold'),foreground="Black")
        temp_label1.grid(row=4, column=3)

        pressure_label1 = tk.Label(frame1, text=temp2, font=("Arial", 10,'bold'),foreground="Black")
        pressure_label1.grid(row=5, column=3)

        temp_label2 = tk.Label(frame1, text=press1, font=("Arial",10,'bold'),foreground="Black")
        temp_label2.grid(row=6, column=3)

        pressure_label2 = tk.Label(frame1, text=press2, font=("Arial", 10,'bold'),foreground="Black")
        pressure_label2.grid(row=7, column=3)
        window.update()
    if (temp11/2 >= 35 and temp11/2 <= 40) and (humid1/2 >= 50 and humid1/2 <= 70):
        enable=checkTempPress(temp13,press13,temp23,press23,2)
    else:
      Pass_Label = tk.Label(frame1, text="FAIL ",font=("Arial", 10,'bold'),foreground="RED")
      Pass_Label.grid(row=1,column=3)
      info_box.configure(state="normal")
      info_box.insert(tk.END, f"Faulty DHT22 Sensor Please Check Wiring !!!\n\n")
      info_box.see(tk.END)
      info_box.configure(state="disabled")
      checkTemp(temp13,temp23,2)
      checkPress(press13,press23,2)
      SystemOff.config(state=tk.NORMAL)
      CycleOn.config(state=tk.DISABLED)
      CycleOff.config(state=tk.DISABLED)
      SystemOn.config(state=tk.DISABLED)
      return
    for i in range(2,8):
        if i not in fault:
            Pass_Label = tk.Label(frame1, text="PASS",font=("Arial", 10,'bold'),foreground="GREEN")
            Pass_Label.grid(row=i,column=4)   
    if stop == True:
        return
    if enable == 1:
        SystemOff.config(state=tk.NORMAL)
        CycleOn.config(state=tk.NORMAL)
        CycleOff.config(state=tk.DISABLED)
        SystemOn.config(state=tk.DISABLED)
    window.update()
    return
def systemOff():
    info_box.config(state='normal')
    info_box.delete(1.0,END)
    info_box.config(state='disabled')
    Pass_Label = tk.Label(frame1, text="          ",font=("Arial", 10,'bold'))
    Pass_Label.grid(row=1,column=3)
    for i in range(2,8):
        Pass_Label = tk.Label(frame1, text="          ",font=("Arial", 10,'bold'))
        Pass_Label.grid(row=i,column=4)
    global stop
    stop = True
    #window.update()
    SystemOn.config(state=tk.NORMAL)
    CycleOn.config(state=tk.DISABLED)
    CycleOff.config(state=tk.DISABLED)
    SystemOff.config(state=tk.DISABLED)
    CumCycleDownload.config(state=tk.DISABLED)
    window.update()
    return
def cycleOn():
    initialDate=datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S")
    global flag
    flag = 0
    global itr_time
    global sensor_data
    global stop
    global sv013,sv02
    sv013=0
    sv02=0
    stop = True
    CycleOff.config(state=tk.NORMAL)
    CycleOn.config(state=tk.DISABLED)
    CumCycleDownload.config(state=tk.DISABLED)
    #disp_tempPress()
    pressure_label2 = tk.Label(frame1, text="CYCLE ON", font=("Arial", 12,'bold'),foreground="Black")
    pressure_label2.grid(row=3, column=5,sticky="w")
    fixed_size=(20,20)
    gif = Image.open("DownloadFile.gif")
    frames = [ImageTk.PhotoImage(frame.copy().resize(fixed_size, Image.Resampling.LANCZOS)) for frame in ImageSequence.Iterator(gif)]
    ProgressLabel = tk.Label(frame1)
    ProgressLabel.grid(row=3, column=6)
    def update_frame(frame_number):
       frame=frames[frame_number]
       ProgressLabel.config(image=frame)
       frame_number+=1

       if frame_number == len(frames):
          frame_number=0
       frame1.after(100,update_frame,frame_number)
    frame1.after(0,update_frame,0)
    while True:
      itr_time+=1
      if flag == 1:
         return
      sensor_data=[]
      sensor_data.append(str(i+1))
      now=datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S")
      sensor_data.append(now)
      sensor_data.append(Press.getPress1())
      sensor_data.append(Temp.getTemp1())
      sensor_data.append(Press.getPress2())
      sensor_data.append(Temp.getTemp2())
      temp,humidity=TempHumidity.getTempHumidity()
      temp=54
      enable1=checkDHT22(temp,humidity)
      enable=checkTempPress(sensor_data[3],sensor_data[2],sensor_data[5],sensor_data[4],1)
      if enable == 0 or enable1 == 0:
        pressure_label2 = tk.Label(frame1, text="                    ", font=("Arial", 10,'bold'))
        pressure_label2.grid(row=3, column=5,sticky="w")
        ProgressLabel1 = tk.Label(frame1,text="                    ",height=1)
        ProgressLabel1.grid(row=3, column=6)
        return
      cycle_data=[]
      cycle_data.append(str(i+1))
      cycle_data.append(now)
      if itr_time%2==1:
        cycle_data.append(1)
        cycle_data.append(0)
        cycle_data.append(1)
        sv013+=1
      else:
        cycle_data.append(0)
        cycle_data.append(1)
        cycle_data.append(0)
        sv02+=1
      disp_tempPress(sv013,sv02,initialDate,sensor_data[2],sensor_data[3],sensor_data[4],sensor_data[5])
      dataBase.addSensorData(sensor_data)
      dataBase.addCycleData(cycle_data)
      time.sleep(1)
    window.update()
    return
def cycleOff():
    for i in range(2,8):
        Pass_Label = tk.Label(frame1, text="              ",font=("Arial", 10,'bold'),foreground="GREEN")
        Pass_Label.grid(row=i,column=4)
    pressure_label2 = tk.Label(frame1, text="                    ", font=("Arial", 10,'bold'),foreground="Black")
    pressure_label2.grid(row=3, column=5,sticky="w")
    ProgressLabel = tk.Label(frame1,text="                    ",height=1)
    ProgressLabel.grid(row=3, column=6)
    global data
    global end_txt
    end_txt = datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S")
    global stop
    global row_num
    global flag
    flag = 1
    row_num = row_num+1
    label = tk.Label(frame, text=end_txt, font=("Arial", 12))
    label.grid(row=row_num, column=2)
    txt=data[1]
    global downloadButton
    downloadButton = tk.Button(frame, text="Download",command=lambda: export_data(txt,end_txt))
    downloadButton.grid(row=row_num, column=9,padx=68)
    stop = False
    CycleOn.config(state=tk.NORMAL)
    CycleOff.config(state=tk.DISABLED)
    CumCycleDownload.config(state=tk.NORMAL)
    downloadButton.config(state=tk.NORMAL)
    window.update()
    return
def export_data(timestamp,end_txt):
    conn = sqlite3.connect('EnduranceTesting.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CycleData WHERE DateTime BETWEEN ? AND ?", (timestamp,end_txt,))
    rows = cursor.fetchall()
    #conn.close()

    # Write to a CSV file
    filename = f"export_Cycle_Count_{timestamp.replace(' ', '_').replace(':', '-')}.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["S.No", "Time", "SV - 01","SV - 02","SV - 03"])
        csvwriter.writerows(rows)

    cursor.execute("SELECT * FROM SensorData WHERE DateTime BETWEEN ? AND ?", (timestamp,end_txt,))
    rows = cursor.fetchall()
    conn.close()

    # Write to a CSV file
    filename1 = f"export_SensorData_{timestamp.replace(' ', '_').replace(':', '-')}.csv"
    with open(filename1, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["S.No", "Time", "Pressure Sensor - 1","Temparature Sensor - 1","Pressure Sensor - 2","Temparature Sensor - 2"])
        csvwriter.writerows(rows)
    
    print(f"Data for {timestamp} exported to {filename}")
    print(f"Data for {timestamp} exported to {filename1}")
    info_box.configure(state="normal")
    info_box.insert(tk.END, f"Data for {timestamp} exported to {filename}\n\n")
    info_box.insert(tk.END, f"Data for {timestamp} exported to {filename1}\n\n")
    info_box.see(tk.END)
    info_box.configure(state="disabled")

def system_starter():
  t1 = threading.Thread(target=systemOn)
  t1.start()
def system_stopper():
  t2 = threading.Thread(target=systemOff)
  t2.start()
def Cycle_starter():
  t3 = threading.Thread(target=cycleOn)
  t3.start()
def Cycle_stopper():
  t4 = threading.Thread(target=cycleOff)
  t4.start()

def Cycle_downloader():
   t5 = threading.Thread(target=export_data)
   t5.start()
def CumCycle_downloader():
    print("Downloading...")
    conn = sqlite3.connect('EnduranceTesting.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SensorData")
    rows = cursor.fetchall()
    #conn.close()

    # Write to a CSV file
    filename = f"export_AllSensorData.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["S.No", "Time", "Pressure Sensor - 1","Temparature Sensor - 1","Pressure Sensor - 2","Temparature Sensor - 2"])
        csvwriter.writerows(rows)
    
    cursor.execute("SELECT * FROM SensorData")
    rows = cursor.fetchall()
    conn.close()

    # Write to a CSV file
    filename1 = f"export_AllCycleData.csv"
    with open(filename1, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["S.No", "Time", "SV - 01","SV - 02","SV - 03"])
        csvwriter.writerows(rows)

    print(f"Data exported to {filename}")
    print(f"Data exported to {filename1}")
    info_box.configure(state="normal")
    info_box.insert(tk.END, f"Data exported to {filename}\n\n")
    info_box.insert(tk.END, f"Data exported to {filename1}\n\n")
    info_box.see(tk.END)
    info_box.configure(state="disabled")
frame_body = tk.Frame(window, border=4, relief="ridge")
frame_body.place(relx=0, rely=1/9, relwidth=1, relheight=1/2)
frame_body.grid_propagate(True)

frame1 = tk.Frame(frame_body, border=2)
frame1.grid(row=0, column=0)

frame_body1_right = tk.Frame(frame_body, border=2)
frame_body1_right.grid(row=0, column=1, sticky="nsew")

info_box = tk.Text(frame_body1_right, state="disabled", width=80, height=16)
info_box.pack()

frame1.rowconfigure(list(range(9)), weight = 1, uniform="Silent_Creme")
frame1.columnconfigure(list(range(2,7)), weight = 1, uniform="Silent_Creme")

SystemOn = tk.Button(frame1, text="System On",command=system_starter,font=("Arial", 12,'bold'),width=10)
SystemOn.grid(row=0, column=0)

SystemOff = tk.Button(frame1, text="System Off",command=system_stopper,font=("Arial", 12,'bold'),width=10)
SystemOff.grid(row=1, column=0)
SystemOff.config(state=tk.DISABLED)

CycleOn = tk.Button(frame1, text="Cycle On",command=Cycle_starter,font=("Arial", 12,'bold'),width=10)
CycleOn.grid(row=2, column=0)
CycleOn.config(state=tk.DISABLED)

labels = ["POWER ON","PASS","SYSTEM ON","Env. Temparature","Env. Humidity","Temp. sensor - 1","Press. Sensor - 1","Temp. sensor - 2","Press. Sensor - 2"]
row_num1=0
for label_it in labels:
    if label_it == "PASS":
        label = tk.Label(frame1, text="PASS",font=("Arial",10,'bold'),foreground="Green")
        label.grid(row=0,column=3)
    else:
        label = tk.Label(frame1, text=label_it,font=("Arial",12,'bold'),foreground="Black")
        label.grid(row=row_num1,column=2,sticky="w")
        row_num1+=1

pressure_label2 = tk.Label(frame1, text="           ", font=("Arial", 12,'bold'),foreground="Black")
pressure_label2.grid(row=8, column=1,sticky="w")

# #--------------------- Table Frame ------------------------

frame_table = tk.Frame(window, border=4,relief=RIDGE)
frame_table.place(relx=0, rely=1/2.18, relwidth=1, relheight=1/2)

header_labels = ["S No", "Start Date & Time", "End Date & Time", "SV01", "SV02","Press. Sensor 1","Temp. Sensor 1","Press. Sensor 2","Temp. Sensor 2","Download"]

# frame_table = tk.Frame(window,width=800,height=300)
# frame_table.grid(row=14,column=0)
#header_labels = ["S No", "Start Date & Time", "End Date & Time", "   SV01   ", "SV02","Download"]
widthlist=[]
for i, label_text in enumerate(header_labels):
    chars=len(label_text)
    label = tk.Label(frame_table, text=label_text, font=("Arial", 12, "bold"),width=chars+4)
    widthlist.append(chars+4)
    label.grid(row=0, column=i)

canvas = tk.Canvas(frame_table)
scrollbar = tk.Scrollbar(frame_table, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=1, column=0, columnspan=len(header_labels), sticky="nsew")
scrollbar.grid(row=1, column=len(header_labels), sticky="ns")
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.config(scrollregion=(0, 0, frame.winfo_width(), frame.winfo_height()))
canvas.yview_moveto(1.0)
downloadButton = tk.Button(frame_table, text="")
downloadButton.config(state="disabled")

def disp_tempPress(sv013,sv02,now,press1,temp1,press2,temp2):
  global data,flag
  if flag==1:
     return
  global downloadButton
  global txt
  data=[0,0,0,0,0,0,0,0,0]
  data[0]=row_num+1
  data[1]=now
  data[3]=sv013
  data[4]=sv02
  data[5]=press1
  data[6]=temp1
  data[7]=press2
  data[8]=temp2
  for col_num, data_item in enumerate(data):
    if col_num==2:
        widths=20
    else:
       widths = widthlist[col_num]+1
    label = tk.Label(frame, text=data_item, font=("Arial", 12),width=widths)
    label.grid(row=row_num + 1, column=col_num,pady=10)

  canvas.create_window((0, 0), window=frame, anchor="nw")
  canvas.config(scrollregion=(0, 0, frame.winfo_width(), frame.winfo_height()))
  canvas.yview_moveto(1.0)
  frame.update_idletasks() 
  if stop == False or flag==1:
      return 

#--------------------------- Bottom Frame ----------------------
frame2 = tk.Frame(window, border=4, relief="ridge")
frame2.place(relx=0, rely=7/7.7, relwidth=1, relheight=1/4)

CycleOff = tk.Button(frame2, text="Cycle Off",command=Cycle_stopper,font=("Arial", 12,'bold'),width=10)
CycleOff.grid(row=0, column=0)
CycleOff.config(state=tk.DISABLED)

CumCycleDownload = tk.Button(frame2, text="Cum Cycles Download",command=CumCycle_downloader,foreground="Black",font=("Arial", 12,'bold'),width=20)
CumCycleDownload.grid(row=0, column=3)
CumCycleDownload.config(state=tk.DISABLED)
frame2.rowconfigure(list(range(2)), weight = 1, uniform="Silent_Creme")
frame2.columnconfigure(list(range(4)), weight = 1, uniform="Silent_Creme")

window.mainloop()