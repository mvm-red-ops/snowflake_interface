import streamlit as st
import os
import snowflake.connector
import form
# Everything is accessible via the st.secrets dict:

    

# passed to streamlit form as callback
# sets state with selected values and marks form_submitted as true
def form_callback():
    st.session_state.year_options
    st.session_state.quarter_options
    st.session_state.payment_options
    st.session_state.domain_options
    st.session_state.department_options
    st.session_state.platform_options
    st.session_state.form_submitted='true'


def form_submitted():
    if(st.session_state.form_submitted=='true'):
        return 'true'
    else:
        return 'false'

if 'form_fubmitted' not in st.session_state:
    print('no form submitted')
    st.header('_Fill out the form below so we know what data to grab..._')
    form.write_form(form_callback)
    st.stop()  # App won't run anything after this line


if form_submitted():
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

    # rows = run_query(" SELECT * from financials.public.payments_master;")


    # # Print results.
    # for row in rows:
    #     st.write(f"{row[0]} has a :{row[1]}:")