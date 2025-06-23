import streamlit as st

# --- Configuration de la page ---
st.set_page_config(page_title="YourCarYourWay", page_icon="🚗", layout="wide")

pages = {
    "Instructions 💡": [
        st.Page("Instructions.py", title="YourCarYourWay"),
    ],
    "Démo 👀": [
        st.Page("Discussions.py", title="Discussions"),
    ],
    "": [
        st.Page("Messages.py", title="")
    ]
}
pg = st.navigation(pages)
pg.run()
