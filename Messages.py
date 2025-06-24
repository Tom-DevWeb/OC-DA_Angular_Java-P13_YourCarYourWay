import time

import streamlit as st
from datetime import datetime
from sqlalchemy import text

st.set_page_config(page_title="Messages du thread", layout="wide")

conn = st.connection("postgresql", type="sql")


# Vérification des données de session
if "profil" not in st.session_state or "user_id" not in st.session_state:
    st.warning("⚠️ Aucun profil sélectionné. Veuillez retourner à l'accueil pour choisir un rôle.")
    st.stop()

user_id = st.session_state["user_id"]
profil = st.session_state["profil"]


# Récupérer le threadId
thread_id = st.session_state.get("thread_id")
if thread_id is None:
    st.error("Aucun thread sélectionné.")
    st.stop()

# Réinitialisation de l'historique si le thread change
last_id = st.session_state.get("last_thread_id")
last_role = st.session_state.get("last_profil")
if last_id is None or last_id != thread_id or last_role != profil:
    st.session_state["last_thread_id"] = thread_id
    st.session_state["last_profil"] = profil
    st.session_state.pop("messages_history", None)
    st.rerun()

#Requête pour récupérer le statut actuel du thread
query_status = '''
               SELECT "statusOpen"
               FROM "Threads"
               WHERE "id" = :threadId \
               '''

with conn.session as s:
    result = s.execute(text(query_status), {"threadId": thread_id})
    status_row = result.fetchone()
    if status_row is None:
        st.error("Thread non trouvé.")
        st.stop()
    current_status = status_row.statusOpen

# Affichage du statut avec un indicateur visuel
status_text = "Ouvert" if current_status else "Fermé"
status_color = "🟢" if current_status else "🔴"
st.write(f"**Statut actuel :** {status_color} {status_text}")

# Bouton pour changer le statut (visible seulement pour Service client)
if profil == "Service client":
    if st.button("🔄 Changer le statut du thread"):
        new_status = not current_status
        update_query = '''
                       UPDATE "Threads"
                       SET "statusOpen" = :new_status,
                           "updatedAt" = :updated_at
                       WHERE "id" = :threadId \
                       '''
        with conn.session as s:
            s.execute(text(update_query), {
                "new_status": new_status,
                "updated_at": datetime.now(),
                "threadId": thread_id
            })
            s.commit()
        st.success(f"Le statut du thread est maintenant {'Ouvert' if new_status else 'Fermé'}.")
        time.sleep(2)
        st.rerun()

st.header(f"💬 Messages du thread #{thread_id}")
st.divider()

# Requête pour récupérer les messages associés au thread
query_messages = '''
                 SELECT M."id", M."message", M."createdAt", M."userId", U."firstName", U."lastName", R."role" as role
                 FROM "Messages" M
                          JOIN "MessagesThreads" MT ON M."id" = MT."messageId"
                          JOIN "Users" U ON M."userId" = U."id"
                          JOIN "Roles" R ON U."roleId" = R."id"
                 WHERE MT."threadId" = :threadId
                 ORDER BY M."createdAt";
                 '''

with conn.session as s:
    messages = s.execute(text(query_messages), {"threadId": thread_id}).fetchall()

# Construction de l'historique (chat format)
if "messages_history" not in st.session_state:
    history = []
    for row in messages:
        # Formatage de la date et heure
        created_at_str = row.createdAt.strftime("%d/%m/%Y %H:%M")

        # Déterminer si c'est moi qui ai envoyé le message
        if row.userId == user_id:
            sender_name = "Moi"
        else:
            sender_name = f"{row.firstName} {row.lastName}"

        # Déterminer le rôle pour l'affichage
        role = "assistant" if row.role == "customer_service" else "user"

        history.append({
            "role": role,
            "sender": sender_name,
            "message": row.message,
            "created_at_str": created_at_str
        })
    st.session_state.messages_history = history

# Affichage de l'historique
for msg in st.session_state.messages_history:
    message_container = st.chat_message(msg["role"])
    message_container.markdown(f"**{msg['sender']}** : {msg['message']}")
    message_container.markdown(f"<span style='font-size:0.75em; color:gray;'> {msg['created_at_str']} </span>", unsafe_allow_html=True)

if current_status:
    # Saisi utilisateur
    if prompt := st.chat_input("Écrire un message..."):
        now = datetime.now()

        # Insertion du message
        insert_message_query = '''
                               INSERT INTO "Messages" ("message", "createdAt", "updatedAt", "userId")
                               VALUES (:message, :createdAt, :updatedAt, :userId)
                               RETURNING "id"; \
                               '''

        with conn.session as s:
            result = s.execute(text(insert_message_query), {
                "message": prompt.strip(),
                "createdAt": now,
                "updatedAt": now,
                "userId": user_id,
            })
            message_id = result.scalar_one()

            # Lier le message au thread
            s.execute(text('''
                           INSERT INTO "MessagesThreads" ("threadId", "messageId")
                           VALUES (:threadId, :messageId)
                           '''), {
                          "threadId": thread_id,
                          "messageId": message_id
                      })

            # Mettre à jour updatedAt du thread
            s.execute(text('''
               UPDATE "Threads"
               SET "updatedAt" = :updatedAt
               WHERE "id" = :threadId
               '''), {
              "updatedAt": now,
              "threadId": thread_id
          })
            s.commit()

        # Ajouter au chat localement
        msg_role = "assistant" if profil == "Service client" else "user"
        st.session_state.messages_history.append({
            "role": msg_role,
            "sender": "Moi",
            "message": prompt.strip(),
            "created_at_str": now.strftime("%d/%m/%Y %H:%M")
        })
        st.rerun()
else:
    st.warning("⚠️ Ce thread est fermé, vous ne pouvez plus écrire de messages.")