import streamlit as st

# --- Configuration de la page ---
st.set_page_config(page_title="YourCarYourWay", page_icon="🚗", layout="wide")

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
st.markdown("### 👤 Choisissez votre rôle")
profil = st.selectbox(
    "Choisissez un profil pour continuer :",
    ["Client", "Service client"]
)

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
