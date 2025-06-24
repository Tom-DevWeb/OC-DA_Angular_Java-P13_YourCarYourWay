import streamlit as st

# --- En-tête ---
st.title("🚗 YourCarYourWay")
st.subheader("Bienvenue sur la plateforme de messagerie")
st.markdown("---")

# Étape 1 : Choix du profil
st.markdown("### 1️⃣ Sélection du profil")
st.info(
    """
    Choisissez votre rôle dans la liste déroulante :
    - **Client** : pour accéder à vos échanges avec le service client.
    - **Service client** : pour répondre aux messages des utilisateurs.
    """
)

# Initialiser la valeur par défaut s’il n'y en a pas
if "profil" not in st.session_state:
    st.session_state["profil"] = "Client"

st.markdown("### 👤 Choisissez votre rôle")
profil = st.selectbox(
    "Choisissez un profil pour continuer :",
    ["Client", "Service client"],
    index=["Client", "Service client"].index(st.session_state["profil"]),
)

# Stocker le profil et l'user_id correspondant
st.session_state["profil"] = profil
st.session_state["user_id"] = 2 if profil == "Client" else 3

# Étape 2 : Accéder à la messagerie
st.markdown("### 2️⃣ Accéder aux messages")
st.info(
    """
    Une fois le profil sélectionné, cliquez sur **Messages** dans le menu.

    - Une liste de conversations s'affichera.
    - Sélectionnez une conversation pour afficher l'historique des messages.
    """
)

# Étape 3 : Envoyer un message
st.markdown("### 3️⃣ Envoyer un message")
st.info(
    """
    Dans une conversation, utilisez le champ de saisie pour écrire un message.

    Cliquez ensuite sur **Envoyer** pour transmettre votre réponse.
    """
)

# Fin
st.success("🎉 A vous de jouer ! 😊")
