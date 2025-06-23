import streamlit as st
from datetime import datetime
from sqlalchemy import text

st.set_page_config(page_title="Messages du thread", layout="wide")

conn = st.connection("postgresql", type="sql")

user_id = 2  # exemple, à remplacer par l'id connecté

# Vérification du rôle
if "profil" not in st.session_state:
    st.warning("⚠️ Aucun profil sélectionné. Veuillez retourner à l'accueil pour choisir un rôle.")
    st.stop()

# Récupérer le threadId
thread_id = st.session_state.get("thread_id")
if thread_id is None:
    st.error("Aucun thread sélectionné.")
    st.stop()

# Vérifier si le thread_id a changé

last_id = st.session_state.get("last_thread_id")
if last_id is None:
    st.session_state["last_thread_id"] = thread_id
    st.session_state.pop("messages_history", None)  # Réinitialiser l'historique
    st.rerun()
elif last_id != thread_id:
    st.session_state["last_thread_id"] = thread_id
    st.session_state.pop("messages_history", None)
    st.rerun()



st.header(f"💬 Messages du thread #{thread_id}")

# Requête pour récupérer les messages associés au thread
query_messages = '''
                 SELECT M."id", M."message", M."createdAt", U."firstName", U."lastName"
                 FROM "Messages" M
                          JOIN "MessagesThreads" MT ON M."id" = MT."messageId"
                          JOIN "Threads" T ON MT."threadId" = T."id"
                          JOIN "Users" U ON T."userId" = U."id"
                 WHERE T."id" = :threadId
                 ORDER BY M."createdAt";
                 '''

with conn.session as s:
    messages = s.execute(text(query_messages), {"threadId": thread_id}).fetchall()

# Utilisation de la nouvelle API Streamlit chat
if "messages_history" not in st.session_state:
    st.session_state.messages_history = [
        {"role": "user", "content": f"{row.firstName} {row.lastName}: {row.message}"} for row in messages
    ]

st.chat_message("system").write("Voici l'historique des messages:")

for msg in st.session_state.messages_history:
    st.chat_message(msg["role"]).write(msg["content"])

# Zone de saisie
if prompt := st.chat_input("Écrire un message..."):
    now = datetime.now()

    # Insérer le message dans Messages et récupérer son id
    insert_message_query = '''
                           INSERT INTO "Messages" ("message", "createdAt", "updatedAt")
                           VALUES (:message, :createdAt, :updatedAt)
                           RETURNING "id";
                           '''

    with conn.session as s:
        result = s.execute(text(insert_message_query), {
            "userId": user_id,
            "message": prompt.strip(),
            "createdAt": now,
            "updatedAt": now
        })
        message_id = result.scalar_one()

        # Insérer la liaison dans MessagesThreads
        s.execute(text('''
                       INSERT INTO "MessagesThreads" ("threadId", "messageId")
                       VALUES (:threadId, :messageId)
                       '''), {
                      "threadId": thread_id,
                      "messageId": message_id
                  })
        s.commit()

    # Ajouter localement
    st.session_state.messages_history.append({"role": "user", "content": f"Moi: {prompt.strip()}"})
    st.rerun()
