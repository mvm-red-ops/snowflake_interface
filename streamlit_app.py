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

if 'form_submitted' not in st.session_state:
    print('no form submitted')
    form.write_form(form_callback)
    st.stop()  # App won't run anything after this line

def form_query():
    full_query=''
    base_query='SELECT * FROM PAYMENTS_MASTER'
    where_options=[]
    if len(st.session_state.year_options) > 0: 
        year_options_str = ','.join(st.session_state.year_options)
        year_query = 'YEAR IN (' + year_options_str + ')'
        where_options.append(year_query)

    if len(st.session_state.quarter_options) > 0: 
        formatted=[]
        for x in st.session_state.quarter_options: 
            formatted.append("'{0}'".format(x))
        quarter_options_str = ','.join(formatted)
        quarter_query = 'QUARTER IN (' + quarter_options_str + ')'
        where_options.append(quarter_query)

    if len(st.session_state.payment_options) > 0: 
        formatted=[]
        for x in st.session_state.payment_options: 
            formatted.append("'{0}'".format(x))
        payment_options_str = ','.join(formatted)
        payment_query = 'PAYMENT IN (' + payment_options_str + ')'
        where_options.append(payment_query)

    if len(st.session_state.domain_options) > 0: 
        formatted=[]
        for x in st.session_state.domain_options: 
            formatted.append("'{0}'".format(x))
        domain_options_str = ','.join(formatted)
        domain_query = 'DOMAIN IN (' + domain_options_str + ')'
        where_options.append(domain_query)

    if len(st.session_state.department_options) > 0: 
        formatted=[]
        for x in st.session_state.department_options: 
            formatted.append("'{0}'".format(x))
        department_options_str = ','.join(formatted)
        department_query = 'DEPARTMENT IN (' + department_options_str + ')'
        where_options.append(department_query)

    if len(st.session_state.platform_options) > 0: 
        formatted = []
        for x in st.session_state.platform_options: 
            formatted.append("'{0}'".format(x))
        platform_options_str = ','.join(formatted)
        platform_query = 'PLATFORM IN (' + platform_options_str + ')'
        where_options.append(platform_query)
   
    # iterate through all options to concat the where clause
    if(len(where_options) > 0):
        full_query = base_query + ' WHERE ' + where_options[0]
        if(len(where_options) > 1): 
            counter = 1
            while counter < len(where_options):
                curr=where_options[counter]
                print(counter, curr)
                full_query = full_query + ' AND ' + curr
                counter+=1
    else: 
        return base_query

    print(full_query)

if form_submitted():
    print('form submitted')
    
    query = form_query()

    # Uses st.experimental_singleton to only run once.
    # @st.experimental_singleton
    # def init_connection():
    #     return snowflake.connector.connect(
    #         **st.secrets["snowflake"], client_session_keep_alive=True
    #     )

    # conn = init_connection()

    # # Perform query.
    # # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    # @st.experimental_memo(ttl=600)
    # def run_query(query):
    #     with conn.cursor() as cur:
    #         cur.execute("USE WAREHOUSE COMPUTE_WH")
    #         cur.execute("USE DATABASE FINANCIALS")
    #         cur.execute(query)
    #         return cur.fetchall()

    # # rows = run_query(" SELECT * from financials.public.payments_master;")


    # # # Print results.
    # # for row in rows:
    # #     st.write(f"{row[0]} has a :{row[1]}:")