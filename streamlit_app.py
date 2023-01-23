import streamlit as st
import os
import snowflake.connector
# Everything is accessible via the st.secrets dict:

st.write("DB user:", st.secrets["db_user"])
st.write("DB pw:", st.secrets["db_pw"])
st.write("DB acct:", st.secrets["db_acct"])



# Gets the version
ctx = snowflake.connector.connect(
    user=st.secrets["db_user"],
    password=st.secrets["db_pw"],
    account=st.secrets["db_acct"]
    )
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
ctx.close()