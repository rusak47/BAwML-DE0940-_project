from datetime import datetime
import streamlit as st
import psycopg2
from psycopg2 import Error
from streamlit.components.v1 import html
from DatabaseConnector import DatabaseConnector
from Range import Range

# Add custom CSS
from BaseTemplate import base_page_style_extended
st.markdown(base_page_style_extended(), unsafe_allow_html=True)

# Initialize session state for pagination if not exists
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'selected_ad' not in st.session_state:
    st.session_state.selected_ad = None
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

RESULTS_PER_PAGE = 6


def show_search_page():
    # Add widgets to sidebar
    st.sidebar.title('Search')
    st.sidebar.header('Filters')
    
    # Create separate rows for search form and results
    # Search form row
    from SearchForm import create_search_form
    create_search_form(st, DatabaseConnector()) 
    
    # Results row
    from SearchResultsContainer import create_search_results_container
    create_search_results_container(st, RESULTS_PER_PAGE, DatabaseConnector())

from DetailsPage import show_details_page2

# Main app logic
with st.spinner('Loading... Please be patient.'):
    if st.session_state.selected_ad is None:
        show_search_page()
    else:
        show_details_page2(st)
