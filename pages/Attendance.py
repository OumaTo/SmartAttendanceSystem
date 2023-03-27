import datetime
import time
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import matplotlib as plt
import plotly.express as px
import cv2
import sys
import os
import numpy as np
import face_recognition

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ouma_nyooti",
    database="SmartAttendanceSystem"
)
cursor = conn.cursor()

students = []
Attendance_Number = []
Attendances = []
Names = []
Admissions = []
st.title('SMART ATTENDANCE SYSTEM')
st.subheader(" ATTENDANCE")

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

st.sidebar.markdown("# Attendance Page")

def detect_face():
    import face_recognition as fr
    import cv2
    import numpy as np
    import os

    path = "./Images/Known_faces/"

    known_names = []
    known_name_encodings = []

    images = os.listdir(path)
    for _ in images:
        image = fr.load_image_file(path + _)
        image_path = path + _
        encoding = fr.face_encodings(image)[0]

        known_name_encodings.append(encoding)
        known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())

    print(known_names)

    # test_image = "./test/test.jpg"
    # image = cv2.imread(test_image)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    cap = cv2.VideoCapture(0)

    while True:
        Ret, image = cap.read()
        imgS = cv2.resize(image, (0, 0), None, 0.5, 0.5)
        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)


        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_name_encodings, face_encoding)
            name = ""

            face_distances = fr.face_distance(known_name_encodings, face_encoding)
            best_match = np.argmin(face_distances)

            if matches[best_match]:
                name = known_names[best_match]

            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



        cv2.imshow("Image", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return imgS, name, best_match


def time_check(student):
    Time = datetime.datetime.today().replace(microsecond=0)

    sql = 'SELECT Last_Attendance_Time FROM Student WHERE name =%s'
    val = (student,)
    cursor.execute(sql,val)
    Attendance_time = cursor.fetchone()
    conn.commit()

    time = datetime.datetime.strptime(Attendance_time[0],"%Y-%m-%d %H:%M:%S")
    st.write(f"Time :  {Time}")
    datetimeObject = datetime.datetime.strptime(Attendance_time[0],"%Y-%m-%d %H:%M:%S")
    secondsElapsed = (Time - datetimeObject).total_seconds()
    return Time, secondsElapsed

def status_check(single_attendance):
    Expected_Attendance = 16
    Min_Attendance = Expected_Attendance/2
    if single_attendance >= Min_Attendance:
        eligibility = "Eligible to sit for Exams"
        # status = [single_name, single_admission, single_attendance, eligibility]
    else:
        eligibility = 'Not Eligible to sit for an exam'
        # status = [single_name, single_admission, single_attendance, eligibility]
    return eligibility


menu = option_menu(None, ["Mark Attendance", "View Attendance"], icons=["card-checklist", 'person-lines-fill'], menu_icon="cast", default_index=0, orientation="horizontal")

if menu == "Mark Attendance":
    st.header('Mark Attendance')
    
    AttendanceCol1, AttendanceCol2 = st.columns(2)
    # image = AttendanceCol1.file_uploader('Upload image')
    Button = AttendanceCol1.button('Start')
    
    if Button:

        # try:

                imgS, student,index = detect_face()
                Time,Elapsed = time_check(student)

                my_bar = AttendanceCol2.progress(0, "Detecting image. Please wait.....")
                for percent_complete in range(100):
                    time.sleep(0.01)
                my_bar.progress(percent_complete + 1, "Detecting image. Please wait.....")
                
                sql = "SELECT * FROM Student WHERE Name = %s"
                value = (student,)
                cursor.execute(sql, value)
                all_records = cursor.fetchall()
                conn.commit()
                
                # students.append(all_records)
                # Attendance = students[4]
                for rec in all_records:
                    for final_rec in rec:
                        students.append(final_rec)
                       

                if Elapsed >=120: 

                    New_Last_Time_Attendance = Time

                    up= "UPDATE Student SET Last_Attendance_Time =%s WHERE Name = %s"
                    new_up = (Time, student)
                    cursor.execute(up, new_up)
                    conn.commit()
                    
                    Attendance = students[4]
                    New_Attendance = students[4]
                    New_Attendance +=1
                    sql = "UPDATE Student SET Attended =%s WHERE Name = %s"
                    new_values = (New_Attendance, student)
                    cursor.execute(sql, new_values)
                    conn.commit()
                    
                    updating = "SELECT Attended FROM Student WHERE name =%s "
                    updates = (student,)
                    cursor.execute(updating, updates)
                    new_updates = cursor.fetchall()
                    conn.commit()
                    for Attend in new_updates:
                        Attendance_Number.append(Attend)
                    
                    AttendanceCol1.image(imgS)
                    AttendanceCol2.success(f'Image Recognized as {student} ')
                    AttendanceCol2.markdown(f'''Name: {students[0]} \n 
            Admission: {students[1]}\n 
            Course: {students[2]}\n 
            Current Year: {students[3]} \n
            No. Attendance: {Attendance_Number[0][0]}''')
                    
                else:
                    AttendanceCol1.image(imgS)
                    AttendanceCol2.error("Student Already Marked")
                # st.write(secondsElapsed)
                if not student:
                    AttendanceCol2.error('Student not registered, please register first')
            # else:
            #     st.error("Student Already Marked")
        # except:
        #         AttendanceCol2.error('Unable to recognize image')
            
if menu == 'View Attendance':

    Select = st.selectbox("Select", ["Single Student", "All Students"])

    if Select == "Single Student":
        Student_Adm = st.text_input("Enter Student Admission")
        Search_Button = st.button("Search")

        if Search_Button:

            Status = []     
            cursor.execute(f"SELECT Name, Admission,Course, yos, Attended FROM Student WHERE Admission ='{Student_Adm}'")
            records = cursor.fetchall()

            for rec in records:

                Student_name = rec[0]
                Student_Admission = rec[1]
                Student_Course = rec[2]
                Student_yos = rec[3]
                Student_Attendance = rec[4]
                # st.write(records)
                eligibility = status_check(Student_Attendance)

                s = [Student_name , Student_Admission, Student_Course, Student_yos, Student_Attendance,eligibility]
                Status.append(s)

            heading = ['Name', 'Admission',"Course", "Year", "Attendance",'eligibility']
            df = pd.DataFrame(Status,columns=(heading))
            st.table(df)


    if Select == "All Students":
        Search_Button = st.button("Search")
        if Search_Button:

            Status = []     
            cursor.execute("SELECT Name, Admission,Course, yos, Attended FROM Student")
            records = cursor.fetchall()

            for rec in records:

                Student_name = rec[0]
                Student_Admission = rec[1]
                Student_Course = rec[2]
                Student_yos = rec[3]
                Student_Attendance = rec[4]
                # st.write(records)
                eligibility = status_check(Student_Attendance)

                s = [Student_name , Student_Admission, Student_Course, Student_yos, Student_Attendance,eligibility]
                Status.append(s)

            heading = ['Name', 'Admission',"Course", "Year", "Attendance",'eligibility']
            df = pd.DataFrame(Status,columns=(heading))
            st.table(df)






    st.header('Attendance Records')

    column1,column2 = st.columns([1,1])
    All_records = column1.button('Graphs And Charts')
    # Chart_view = column2.button('Manipulate Graphs') 
    Eligibility = column2.button('Eligibility Table')

    students = []

    if All_records:

        Status = []
        Total_Students = []    
        cursor.execute("SELECT Name, Admission,Course, Attended FROM Student")
        records = cursor.fetchall()

        for total_students in range(len(records)):
            Total_Students.append(total_students)
        for rec in records:

            for Att in rec:
                A = Att
            # st.write(Att)

            Student_name = rec[0]
            Student_Admission = rec[1]
            Student_Course = rec[2]
            Student_Attendance = rec[3]
            # st.write(records)
            eligibility = status_check(Att)


            s = [Student_name , Student_Admission, Student_Course, Student_Attendance,eligibility]
            Status.append(s) 


        heading = ['Name', 'Admission','Course', "Attendance",'eligibility']
        df = pd.DataFrame(Status,columns=(heading))
        # st.table(df)
        st.subheader('Attendance bar chart') 

        # d = px.data.gapminder()
        b = px.bar(df, x='Admission', y = 'Attendance')
        st.write(b)

    # if Chart_view:
   
    #     Status = []
    #     Total_Students = []    
    #     cursor.execute("SELECT Name, Admission,Course, Attended FROM Student")
    #     records = cursor.fetchall()

    #     for total_students in range(len(records)):
    #         Total_Students.append(total_students)
    #     for rec in records:

    #         for Att in rec:
    #             A = Att
    #         # st.write(Att)

    #         Student_name = rec[0]
    #         Student_Admission = rec[1]
    #         Student_Course = rec[2]
    #         Student_Attendance = rec[3]
    #         # st.write(records)
    #         eligibility = status_check(Att)



    #         s = [Student_name , Student_Admission, Student_Course, Student_Attendance,eligibility]
    #         Status.append(s)
    #         # st.write(f'{rec[0]} {rec[1]} {eligibility}') 

    #     # st.write(Status)

    #     heading = ['Name', 'Admission','Course', "Attendance",'eligibility']
    #     df = pd.DataFrame(Status,columns=(heading))

    #     st.header('Attendance charts') 

    #     b = px.bar(df, x='Name', y = 'Attendance')
    #     st.write(b)

    if Eligibility:
        st.header('ELigibility')        
        Status = []     
        cursor.execute("SELECT Name, Admission, Attended FROM Student")
        records = cursor.fetchall()

        for rec in records:
            for Att in rec:
                A = Att
            # st.write(Att)

            Student_name = rec[0]
            Student_Admission = rec[1]
            Student_Attendance = rec[2]
            # st.write(records)
            eligibility = status_check(Att)

            s = [Student_name , Student_Admission, Student_Attendance,eligibility]
            Status.append(s)
            # st.write(f'{rec[0]} {rec[1]} {eligibility}') 
        # st.write(Status)

        heading = ['Name', 'Admission', "Attendance",'eligibility']
        df = pd.DataFrame(Status,columns=(heading))
        st.table(df)
