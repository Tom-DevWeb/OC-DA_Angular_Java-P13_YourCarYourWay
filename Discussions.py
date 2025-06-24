import streamlit as st
from datetime import datetime
from sqlalchemy import text


st.set_page_config(page_title="Fil de discussion", layout="wide")

st.header("📨 Fil de discussion")

conn = st.connection("postgresql", type="sql")


# Vérification du rôle
if "profil" not in st.session_state or "user_id" not in st.session_state:
    st.warning("⚠️ Aucun profil sélectionné. Veuillez retourner à l'accueil pour choisir un rôle.")
    st.stop()

profil = st.session_state["profil"]
user_id = st.session_state["user_id"]  # ⚠️ Utiliser l'ID connecté

st.write(f"Vous êtes connecté en tant que : **{profil}**")


# Champ de titre + bouton de création (réservé aux clients)
if profil == "Client":
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
if profil == "Service client":
    query = '''
            SELECT T."id" AS "threadId", T."title", T."createdAt", T."updatedAt", T."statusOpen", U."firstName", U."lastName"
            FROM "Threads" T
                     JOIN "Users" U ON T."userId" = U."id"
            ORDER BY T."createdAt" DESC; \
            '''
elif profil == "Client":
    query = '''
            SELECT T."id" AS "threadId", T."title", T."createdAt", T."updatedAt", T."statusOpen", U."firstName", U."lastName"
            FROM "Threads" T
                     JOIN "Users" U ON T."userId" = U."id"
            WHERE T."userId" = :userId
            ORDER BY T."createdAt" DESC; \
            '''
else:
    st.error("Profil non reconnu.")
    st.stop()

# Exécution de la requête
with conn.session as s:
    if profil == "Client":
        result = s.execute(text(query), {"userId": user_id})
    else:
        result = s.execute(text(query))
    threads = result.fetchall()

# Affichage
if not threads:
    st.info("Aucune discussion trouvée.")
else:
    st.divider()
    for row in threads:
        st.markdown(f'## 💬 {row.title}')
        if st.button("✒️ Ouvrir", key=f"thread_{row.threadId}"):
            st.session_state["thread_id"] = str(row.threadId)
            st.switch_page("Messages.py")

        created_at = row.createdAt.strftime("%d/%m/%Y à %H:%M")
        updated_at = row.updatedAt.strftime("%d/%m/%Y à %H:%M")

        statut = "Ouvert" if row.statusOpen else "Fermé"
        color = "🟢" if row.statusOpen else "🔴"
        st.write(f"{color} **Statut** : {statut}")
        st.write(f"📅 Créé le {created_at} par **{row.firstName} {row.lastName}**")
        st.markdown(f"<span style='font-size:0.85em; color:gray;'>🕓 Dernière modification : {updated_at}</span>", unsafe_allow_html=True)
        st.divider()