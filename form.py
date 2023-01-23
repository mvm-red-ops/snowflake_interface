import streamlit as st

def write_form(callback):

    with st.form("data_collection"):
        st.write("_Fill out the form below so we know what data to grab..._")

        # year/quarter dropdown-multiselect
        # year of payments 
        year_options = st.multiselect( 'Select :blue[Year/s]', ['2023', '2022', '2021', '2020'], key="year_options")

        # quarter of payments 
        quarter_options = st.multiselect( 'Select :blue[Quarter/s]', ['q1', 'q2', 'q3', 'q4'], key="quarter_options")


        # payment type dropdown- single
        # revenue, expenses or both
        payment_type_options = st.multiselect( 'Select :blue[Payment Type/s]', ['Revenue', 'Expenses'], key="payment_options")


        # domain dropdown-single
        # oo or 
        domain_options = st.multiselect( 'Select :blue[Domain/s]', ['Distribution Partners', 'Owned and Operated'], key="domain_options")


        # department dropdown-multiselect
        # samsung, trc, pluto, etc.
        department_options = st.multiselect(
        'Select :blue[Department/s]',
        ['Samsung', 'The Roku Channel', 'Xumo', 'LG', 'Youtube', 'Pluto'], key="department_options")


        # platform dropdown-multiselect
        # amagi, wurl, youtube, etc.
        platform_options = st.multiselect(
        'Select :blue[Platform/s]',
        ['Amagi', 'AWS/FreeVee', 'Giant Interactive/Tubi', 'Wurl/Sigma', 'Periscope', 'Pluto', 'Youtube'], key="platform_options")


        # Every form must have a submit button.
        submit_button = st.form_submit_button(label='Submit', on_click=callback)

   
