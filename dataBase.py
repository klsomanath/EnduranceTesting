def addSensorData(sensor_data):
    import sqlite3
    conn = sqlite3.connect('EnduranceTesting.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE SensorData(SNo VARCHAR(255), DateTime VARCHAR(255), PressureSensor1 VARCHAR(255), TemparatureSensor1 VARCHAR(255), PressureSensor2 VARCHAR(255), TemparatureSensor2 VARCHAR(255));""")
        #cursor.execute(table)
    except:
         pass
    vals = (sensor_data[0],sensor_data[1],sensor_data[2],sensor_data[3],sensor_data[4],sensor_data[5])
    cursor.execute('''INSERT INTO SensorData VALUES (?,?,?,?,?,?)''',vals)
    conn.commit() 
    conn.close()

def addCycleData(cycle_data):
    import sqlite3
    conn = sqlite3.connect('EnduranceTesting.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE CycleData(SNo VARCHAR(255), DateTime VARCHAR(255), SV01 VARCHAR(255), SV02 VARCHAR(255), SV03 VARCHAR(255));""")
    except:
        pass

    vals = (cycle_data[0],cycle_data[1],cycle_data[2],cycle_data[3],cycle_data[4])
    cursor.execute('''INSERT INTO CycleData VALUES (?,?,?,?,?)''',vals)
    conn.commit() 

    conn.close()