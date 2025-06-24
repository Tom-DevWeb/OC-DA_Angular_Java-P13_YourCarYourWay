import streamlit as st

# --- Configuration de la page ---
st.set_page_config(page_title="YourCarYourWay", page_icon="🚗", layout="wide")

# --- Choix du profil dans la sidebar ---
st.sidebar.markdown("## 👤 Sélection du profil")

# Valeur par défaut
if "profil" not in st.session_state:
    st.session_state["profil"] = "Client"
if "user_id" not in st.session_state:
    st.session_state["user_id"] = 2

# Dropdown dans la barre latérale
profil = st.sidebar.selectbox(
    "Choisissez un rôle :",
    ["Client", "Service client"],
    index=["Client", "Service client"].index(st.session_state["profil"]),
)

# Mise à jour du contexte utilisateur
if st.session_state["profil"] != profil:
    st.session_state["profil"] = profil
    st.session_state["user_id"] = 2 if profil == "Client" else 1
    st.rerun()  # Recharge la page avec le nouveau rôle

# --- Définition des pages ---
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
