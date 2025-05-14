from datetime import datetime
import streamlit as st
import psycopg2
from psycopg2 import Error
from streamlit.components.v1 import html
from Searcher import Searcher
from Range import Range

# Add custom CSS
from BaseTemplate import base_page_style_extended
st.markdown(base_page_style_extended(), unsafe_allow_html=True)

# Initialize session state for pagination if not exists
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if 'search_text' not in st.session_state:
    st.session_state.search_text = ""
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'selected_ad' not in st.session_state:
    st.session_state.selected_ad = None
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

RESULTS_PER_PAGE = 6

# Initialize session state for query parameters
if 'query_params_processed' not in st.session_state:
    st.session_state.query_params_processed = False

# Function to process URL query parameters
def get_query_params():
    if not st.session_state.query_params_processed:
        query_params = st.query_params
        if 'q' in query_params and query_params['q']:
            search_query = query_params['q']
            st.session_state.search_text = search_query
            
            return search_query
            
    return ""

def show_search_page():
    # Add widgets to sidebar
    st.sidebar.title('Search')
    st.sidebar.header('Filters')

    # Create separate rows for search form and results
    # Search form row
    from SearchForm import create_search_form
    create_search_form(st, Searcher())

    # Results row
    from SearchResultsContainer import create_search_results_container
    create_search_results_container(st, RESULTS_PER_PAGE, Searcher())

from DetailsPage import show_details_page2

# Main app logic
with st.spinner('Loading... Please be patient.'):
    if st.session_state.selected_ad is None:
        get_query_params()
        show_search_page()
    else:
        show_details_page2(st)
