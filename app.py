from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path("data/checkins.csv")


def save_checkin(row: dict) -> None:
    """Add a check-in to the CSV. One entry per day: saving again replaces it."""
    DATA_FILE.parent.mkdir(exist_ok=True)
    new_row = pd.DataFrame([row])

    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        df = df[df["date"] != row["date"]]  # drop an older entry for the same day
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(DATA_FILE, index=False)


st.title("Mission Control")
st.subheader("Daily check-in")

with st.form("checkin_form"):
    day = st.date_input("Date", value=date.today())
    sleep = st.number_input("Hours slept", min_value=0.0, max_value=14.0, value=7.0, step=0.5)
    study = st.number_input("Hours studied / project work", min_value=0.0, max_value=16.0, value=2.0, step=0.5)
    mood = st.slider("Mood (1 = awful, 10 = great)", 1, 10, 6)
    energy = st.slider("Energy (1 = drained, 10 = buzzing)", 1, 10, 6)
    note = st.text_input("One-line note (optional)")
    submitted = st.form_submit_button("Save check-in")

if submitted:
    save_checkin({
        "date": str(day),
        "sleep_hours": sleep,
        "study_hours": study,
        "mood": mood,
        "energy": energy,
        "note": note,
    })
    st.success("Saved!")
