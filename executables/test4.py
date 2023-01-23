import streamlit as st


st.header('_Fill out the form below so we know what data to grab..._')

with st.form("data_collection"):
    st.write("_Fill out the form below so we know what data to grab..._")

    # year/quarter dropdown-multiselect
    # year of payments 
    year_options = st.multiselect(
    'Select :blue[Year/s]',
    ['2023', '2022', '2021', '2020'])

    # quarter of payments 
    quarter_options = st.multiselect(
    'Select :blue[Quarter/s]',
    ['q1', 'q2', 'q3', 'q4'])


    # payment type dropdown- single
    # revenue, expenses or both
    payment_type_options = st.multiselect(
    'Select :blue[Payment Type/s]',
    ['Revenue', 'Expenses'])


    # domain dropdown-single
    # oo or 
    domain_options = st.multiselect(
    'Select :blue[Domain/s]',
    ['Distribution Partners', 'Owned and Operated'])


    # department dropdown-multiselect
    # samsung, trc, pluto, etc.
    department_options = st.multiselect(
    'Select :blue[Department/s]',
    ['Samsung', 'The Roku Channel', 'Xumo', 'LG', 'Youtube', 'Pluto'])


    # platform dropdown-multiselect
    # amagi, wurl, youtube, etc.
    platform_options = st.multiselect(
    'Select :blue[Platform/s]',
    ['Amagi', 'AWS/FreeVee', 'Giant Interactive/Tubi', 'Wurl/Sigma', 'Periscope', 'Pluto', 'Youtube'])


    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("year_options", year_options, "quarter_options", quarter_options, "payment_type_options", payment_type_options,"domain_options", domain_options,"department_options", department_options,"platform_options", platform_options
        )

st.write("Outside the form")

