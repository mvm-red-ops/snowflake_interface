import streamlit as st
import snowflake.connector
import form
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


# Everything is accessible via the st.secrets dict:

    
def init_state(): 
    st.session_state['year_options']=''
    st.session_state['quarter_options']=''
    st.session_state['payment_options']=''
    st.session_state['domain_options']=''
    st.session_state['department_options']=''
    st.session_state['platform_options']=''
    st.session_state['query_formed']=''
    st.session_state['query_status']=''
    st.session_state['connection_status']=''
    st.session_state['rows']=['']
    st.session_state['form_submitted']='false'
    st.session_state['full_query']='false'


# passed to streamlit form as callback
# sets state with selected values and marks form_submitted as true
def form_callback():
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

def form_query(callback):
    full_query=''
    base_query='SELECT label, year, quarter, year_month_day, department, title, type, channel, domain, amount, invoice_number, journal_entry FROM PAYMENTS_MASTER'
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
        payment_query = 'LABEL IN (' + payment_options_str + ')'
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
        print(full_query) 
        callback()
        return full_query

    else: 
        return base_query

def query_callback():
    print('in query ')
    st.session_state.query_status='query_formed'
    return
        
if form_submitted():
    print('form submitted')
    query = form_query(query_callback)
    print('full query:')
    st.session_state.full_query=query
    print(st.session_state.full_query)



if 'connection_formed' not in st.session_state:
    # Uses st.experimental_singleton to only run once.
    print('forming connection')
    @st.experimental_singleton
    def init_connection():
        return snowflake.connector.connect(
            **st.secrets["snowflake"], client_session_keep_alive=True
        )
    conn = init_connection() 
    st.session_state.connection_status='connection_formed'
    print('connection formed')


# # Perform query.
# # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute("USE WAREHOUSE COMPUTE_WH")
        cur.execute("USE DATABASE FINANCIALS")
        cur.execute(query)
        rows= cur.fetchall()
        while not rows:
            pass
        print('rows collected and saved to state:')
        st.session_state['rows']=rows



if 'full_query' in st.session_state and 'connection_status' in st.session_state:
    print('context for running query')
    run_query(st.session_state.full_query)

    # st.write(rows)
  



if 'rows' in st.session_state:
    # Print results.
    df = pd.DataFrame(
        st.session_state.rows,
        columns=('label', 'year', 'quarter', 'year_month_day', 'department', 'title', 'type', 'channel', 'domain', 'amount', 'invoice_number', 'journal_entry' )
    )
    # data=st.session_state.rows
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()


    grid_response = AgGrid(
        df,
        columns=('label', 'year', 'quarter', 'year_month_day', 'department', 'title', 'type', 'channel', 'domain', 'amount', 'invoice_number', 'journal_entry' ),
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=True,
        height=350, 
        width='100%',
        reload_data=True
    )
    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df = pd.DataFrame(selected)