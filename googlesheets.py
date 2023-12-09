import streamlit as st
import streamlit_gsheets as gsheets
import pandas as pd



#Display and Title
st.title("Request Portal")
st.markdown("Enter your details please.")

conn = st.connection("gsheets", type=gsheets.GSheetsConnection)

existing_data = conn.read(worksheet="Requests", usecols=list(range(4)), ttl=5)
existing_data = existing_data.dropna(how="all")


GRADES = [
    "Freshman",
    "Sophomore",
    "Junior",
    "Senior"
]

SUBJECTS = [
    "Math",
    "Science",
    "English",
    "History",
    "Computer Science",
    "Spanish",
    "French",
    "Other"
]

with st.form(key="request_form"):
    name = st.text_input("First and Last Name*")
    email = st.text_input("Email*")
    subject = st.selectbox("Subject(s)?*", options=SUBJECTS, index=None)
    grade = st.selectbox("What is your grade?", options=GRADES, index=None)
    
    st.markdown("Fields marked with * are required.")
    
    submit = st.form_submit_button(label="Submit")
    
    if submit:
        #check fields are filled out
        if not name or not email or not subject:
            st.error("Please fill out the required fields.")
            st.stop()
        elif existing_data.loc[existing_data["Email"]==email].shape[0] > 0:
            st.error("You have already submitted a request with this email.")
            st.stop()
        else:
            # create new row 
            student_data = pd.DataFrame(
                {
                    "Name": [name],
                    "Email": [email],
                    "Subject": [subject],
                    "Grade": [grade]
                }
            )
            
            # append new row to existing data
            updated_df = pd.concat([existing_data, student_data], ignore_index=True)
            
            # update google sheets
            conn.update(worksheet="Requests", data=updated_df)
            
            st.success("Thank you for your submission! We will be in touch soon.")
            