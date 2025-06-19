import streamlit as st

st.header("Fil de discussion")
st.write("Liste des discussions en cours:")

conn = st.connection("postgresql", type="sql")

if st.button("Charger les données"):
    df = conn.query('SELECT * FROM "Users";', ttl=300)
    st.dataframe(df)

