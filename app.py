# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 20:14:34 2024

@author: MANaser
"""

from hijri_converter import Hijri
from datetime import datetime
import pandas as pd
import psutil
import streamlit as st

# Streamlit page setup
st.set_page_config(page_title="Upcoming Eid Celebrations", page_icon="🌙", layout="centered")
st.title("Upcoming Eid Celebrations 🌙")

# Define Hijri dates for each Eid event
eids_hijri = {
    "Ashoraa": (1, 10),
    "White Days": (Hijri.today().month, 13),  # Every 13th day of the current Hijri month
    "Ramadan": (9, 1),
    "Eid Al-Fitr": (10, 1),
    "Ten Days": (12, 1),
    "Arafa": (12, 9),
    "Eid Al-Adha": (12, 10),
}

# Function to convert Hijri date to Gregorian and calculate months and days until Eid
def calculate_eid_date_and_time(hijri_month, hijri_day):
    today = datetime.today()
    current_hijri_year = Hijri.today().year
    eid_date_hijri = Hijri(current_hijri_year, hijri_month, hijri_day)

    # Convert to Gregorian and then to datetime
    eid_date_gregorian = eid_date_hijri.to_gregorian()
    eid_date = datetime(eid_date_gregorian.year, eid_date_gregorian.month, eid_date_gregorian.day)

    # Check if Eid is in the past this year; if so, move it to next year
    if eid_date < today:
        eid_date_hijri = Hijri(current_hijri_year + 1, hijri_month, hijri_day)
        eid_date_gregorian = eid_date_hijri.to_gregorian()
        eid_date = datetime(eid_date_gregorian.year, eid_date_gregorian.month, eid_date_gregorian.day)
    
    # Calculate months and days until Eid
    days_until_eid = (eid_date - today).days
    months_until_eid = days_until_eid // 30  # Approximate conversion to months
    remaining_days = days_until_eid % 30
    return eid_date.strftime("%B %d, %Y"), months_until_eid, remaining_days

# Function to display a celebration message for the upcoming Eid
def display_celebration_message(eid_name, days_until_eid):
    if days_until_eid == 0:
        st.markdown(f"🎉 Today is {eid_name}! Celebrate and enjoy the blessings of this special day! 🎉")
    elif days_until_eid <= 3:
        st.markdown(f"🌟 {eid_name} is in {days_until_eid} days! Prepare to celebrate this joyous occasion! 🌟")

# Main function to display Eid dates and time until each event
def main():
    # Eid dates and countdowns
    eid_data = []
    for eid_name, dates in eids_hijri.items():
        # Handle recurring dates (e.g., White Days)
        if isinstance(dates, list):
            for month, day in dates:
                eid_date, months_until_eid, days_until_eid = calculate_eid_date_and_time(month, day)
                eid_data.append({"Eid": eid_name, "Date": eid_date, "Months Until Eid": months_until_eid, "Days Until Eid": days_until_eid})
                display_celebration_message(eid_name, days_until_eid)
        else:
            eid_date, months_until_eid, days_until_eid = calculate_eid_date_and_time(*dates)
            eid_data.append({"Eid": eid_name, "Date": eid_date, "Months Until Eid": months_until_eid, "Days Until Eid": days_until_eid})
            display_celebration_message(eid_name, days_until_eid)

    # Display countdown table
    df = pd.DataFrame(eid_data).sort_values(by=["Months Until Eid", "Days Until Eid"]).reset_index(drop=True)
    df.set_index("Eid", inplace=True)
    st.write(df)

# Check system usage before running the main function
def get_system_usage():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    return cpu_percent, mem_percent

def can_serve_user():
    cpu_percent, mem_percent = get_system_usage()
    return cpu_percent < 90 and mem_percent < 90

# Run the app
if can_serve_user():
    main()
else:
    st.warning("System resources are high. Please try again later.")
