import streamlit as st
from datetime import datetime
from sqlalchemy import text


st.set_page_config(page_title="Fil de discussion", layout="wide")

st.header("📨 Fil de discussion")

conn = st.connection("postgresql", type="sql")

user_id = 2


# Vérification du rôle
if "profil" in st.session_state:
    st.write(f"Vous êtes connecté en tant que : **{st.session_state['profil']}**")
else:
    st.warning("⚠️ Aucun profil sélectionné. Veuillez retourner à l'accueil pour choisir un rôle.")
    st.stop()


# Champ de titre + bouton de création
title = st.text_input("✏️ Titre de votre discussion")
if st.button("📩 Créer une nouvelle discussion"):
    if not title.strip():
        st.warning("Veuillez saisir un titre pour la discussion.")
    else:
        now = datetime.now()
        with conn.session as s:
            s.execute(text('''
                           INSERT INTO "Threads" ("userId", "title", "createdAt", "updatedAt")
                           VALUES (:userId, :title, :createdAt, :updatedAt);
                           '''), params={
                "userId": user_id,
                "title": title.strip(),
                "createdAt": now,
                "updatedAt": now
            })
            s.commit()
        st.success("✅ Nouvelle discussion créée avec succès.")

# Requête pour lister les discussions
if st.session_state['profil'] == "Service client":
    query = '''
            SELECT T."id" AS "threadId", T."title", T."createdAt", U."firstName", U."lastName"
            FROM "Threads" T
                     JOIN "Users" U ON T."userId" = U."id"
            ORDER BY T."createdAt" DESC; \
            '''
elif st.session_state['profil'] == "Client":
    query = f'''
        SELECT T."id" AS "threadId", T."title", T."createdAt", U."firstName", U."lastName"
        FROM "Threads" T
        JOIN "Users" U ON T."userId" = U."id"
        WHERE T."userId" = {user_id}
        ORDER BY T."createdAt" DESC;
    '''
else:
    st.error("Profil non reconnu.")
    st.stop()

# Affichage
df = conn.query(query, ttl=0)

if df.empty:
    st.info("Aucune discussion trouvée.")
else:
    st.markdown("### 💬 Discussions")
    for row in df.itertuples():
        # Crée un bouton avec le titre (un seul bouton par carte)
        if st.button(f"📌 {row.title}", key=f"thread_{row.threadId}"):
            st.session_state["thread_id"] = str(row.threadId)
            st.switch_page("Messages.py")
        # Affiche les infos sous le bouton (optionnel)
        created_at = datetime.strptime(str(row.createdAt), "%Y-%m-%d %H:%M:%S.%f")
        st.write(f"Créé le {created_at.strftime('%d/%m/%Y à %H:%M')} par **{row.firstName} {row.lastName}**")
        st.divider()
