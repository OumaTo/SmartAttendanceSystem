import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import datetime
import openpyxl

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ouma_nyooti",
    database="SmartAttendanceSystem"
)


cursor = conn.cursor()

st.title('SMART ATTENDANCE SYSTEM')

x = datetime.datetime.today().replace(microsecond=0)
year = (x.strftime("%Y"))
month =(x.strftime("%B"))
day = (x.strftime("%A"))
date = (x.strftime("%d"))

hour = (x.strftime("%I"))
Min = (x.strftime("%M"))
am_pm = (x.strftime("%p"))
time_zone = (x.strftime("%Z"))

Time = st.markdown(f"""
        {year} {month} {day} {date}\n
        {hour}:{Min} {am_pm} {time_zone}

        """)

st.sidebar.markdown("# Student Records page ")

st.header('Student Records')

col1, col2 = st.columns(2)
Search_Name = col1.text_input('Enter Admission Number to search')
Search_Button = col1.button('Search')
col2.write('View All Records')
All_Records = col2.button('View')

students = []
if All_Records:
    cursor.execute("SELECT * FROM Student")
    all_records = cursor.fetchall()

    for rec in all_records:
       students.append(rec)
    #    col1.write(students)


    heading = ['Name', 'Admission', 'Course', 'Yos', 'Standing', 'Last_Attendance_Time','id']
    df = pd.DataFrame(students,columns=(heading))
    st.table(df)


    book = openpyxl.Workbook()
# sheet = book['Sheet1']
    sheet = book.active
    i = 0
    for row in all_records:
        i += 1
        j = 1
        for col in row:
            cell = sheet.cell(row = i, column = j)
            cell.value =col
            j += 1
        Book = book.save("Students.xlsx")
        
        # with open ("Students.xlsx", 'rb') as b:
            # Book = "Students.xlsx"
    Sb = open("Students.xlsx", 'rb') 
    s_book = Sb.read()
    st.download_button('Download CSV', s_book, 'Student.xlsx', 'xlsx/csv')


singleStudent = []
if Search_Button:
    col1.write(f'Searching records for {Search_Name}...')
    try:
        search = f"SELECT * FROM Student WHERE Admission ='{Search_Name}' "
        results = cursor.execute(search)
        found_records = cursor.fetchall()
        if found_records:

            for rec in found_records:
                singleStudent.append(rec)
                heading = ['Name', 'Admission', 'Course', 'Yos', 'Standing','Last_Attendance_Time','id']
                df = pd.DataFrame(singleStudent,columns=(heading))
                st.table(df)       
                # col1.write(singleStudent)
        else:
            col1.error('Student Records not found, Make sure you entered correct Admission')
    except:
        col1.error('Sorry an error ocurred with your query')

