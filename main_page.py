import datetime
import streamlit as st
import streamlit as st
from streamlit_option_menu import option_menu
import face_recognition
import cv2
import time
from io import StringIO
import numpy as np
from PIL import Image
st.sidebar.markdown("# Home page ")

header = st.container()
with header:
    headercol1, headercol2= st.columns([1,5])
    headercol1.image('./Images/icon.png')
    headercol2.title('SMART ATTENDANCE SYSTEM')

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

    # st.write(datetime.datetime.today().replace(microsecond=0))
    
    # horizontal Menu
    menu = option_menu(None, ["Home", "Attendance", 'Records'], icons=['house', 'person', "card-checklist", 'person-lines-fill'], menu_icon="cast", default_index=0, orientation="horizontal")
    
    if menu == 'Home':
        st.header('Home page')
        st.write("This page gives a brief description of the system and how to move around it to perform different tasks")
        expand = st.expander('learn more')
        with expand:
            st.image('Images/icon.png')
        
    if menu == 'Attendance':
        st.header('Attendance page')
        st.write("This page gives a brief description of the system and how to move around it to perform different tasks")
        expand = st.expander('learn more')
        with expand:
            expandcol1, expandcol2 = st.columns([1,2])
            expandcol1.write('Brief Description of Mark Attendance page')
            expandcol2.image('Images/mark attendance.png')
        
    if menu == 'Records':
        st.header('Records page')
        st.write("This page gives a brief description of the system and how to move around it to perform different tasks")
        expand = st.expander('learn more')
        with expand:
            expandcol1, expandcol2 = st.columns([1,2])
            expandcol1.write('Brief Description of Records page')
            expandcol2.image('Images/records.png')
