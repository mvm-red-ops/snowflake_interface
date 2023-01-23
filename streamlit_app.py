import streamlit as st
import os
import snowflake.connector
# Everything is accessible via the st.secrets dict:

st.write("DB config:", **st.secrets["snowflake"])


# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()



# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute("USE WAREHOUSE COMPUTE_WH")
        cur.execute("USE DATABASE FINANCIALS")
        cur.execute(query)
        return cur.fetchall()

rows = run_query(" SELECT * from financials.public.payments_master;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")