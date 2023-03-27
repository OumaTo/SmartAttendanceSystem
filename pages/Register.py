import streamlit as st
import cv2
import numpy as np
import streamlit as st
import mysql.connector
import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ouma_nyooti",
    database="SmartAttendanceSystem"
)
cursor = conn.cursor()


def save(Name):
        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()

        if cap.isOpened():
            _,frame = cap.read()
            # cap.release()
            if _ and frame is not None:
                cv2.imwrite(f'Images/Known_faces/{Name}.jpg', frame)
                         
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        image = f'Images/Known_faces/{Name}.jpg'
        return image




st.sidebar.markdown("# Student Registration page ")

# Photo = []
st.header('STUDENT REGISTRATION')
with st.form('STUDENT REGISTRATION'):
        col1, col2, col3 = st.columns([3,1,3])
        
        date_time = datetime.datetime.today().replace(microsecond=0)
        st.write("Date and Time :")

        Name = col1.text_input('Student Name')
        col2.write(' ')
        Admission = col3.text_input('Admission Number')
        Course = col1.text_input('Course')
        col2.write(' ')
        Yos = col3.selectbox("Year of Study", [1,2,3,4])

        Date_Time = st.write(date_time)
        # student_photo = st.button('Capture image')
        
        
        
        submit = st.form_submit_button('Capture & Save', type = 'primary')
        
        if submit:
            if Name  and Admission and Course :
            
                # with open (f'./Images/Known_faces/{Name}.png','wb') as file:
                #     file.write(student_photo.getbuffer())
                image = save(Name)
                st.image(image)

                student = "INSERT INTO student(Name, Admission, Course, Yos, Attended, Last_Attendance_Time) VALUES(%s,%s, %s, %s, %s, %s)"
                student_data = (Name, Admission, Course, Yos, 1, date_time)

                # Student_image = Photo.append(student_photo) 

                cursor.execute(student, student_data)
                conn.commit()
                st.success("Student Registered successfully")
                
            