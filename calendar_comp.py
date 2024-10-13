import streamlit as st
from datetime import datetime

def show_calendar():
    # Initialize state variable for showing the calendar
    if 'show_calendar' not in st.session_state:
        st.session_state.show_calendar = True

    # Toggle button for the calendar
    if st.button("Toggle Calendar"):
        st.session_state.show_calendar = not st.session_state.show_calendar
        st.rerun()

    # Show the calendar if show_calendar is True
    if st.session_state.show_calendar:
        selected_date = st.date_input("Select a date", datetime.now())
        # You can use the selected_date value in your task manager logic (e.g., in your Game class)