
def create_search_results_container(st, RESULTS_PER_PAGE, db=None):
    with st.container():
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        # Display results
        if st.session_state.search_results==None:
            #import time # simulate delay
            #time.sleep(6) 
            from SearchForm import search
            search(st, db)

        elif st.session_state.search_results:
            st.write(f"Found {len(st.session_state.search_results)} results")
            # Pagination controls
            total_pages = (len(st.session_state.search_results) + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
            
            if total_pages > 1: # Create a single row of page buttons
                #for i in range(min(total_pages, 5)):
                #todo fix spacing and button count with ...
                # maybe add previous/next buttons for easier control
                for i, col in enumerate(st.columns(total_pages)):
                    if col.button(str(i + 1), key=f"page_{i}"):
                        st.session_state.page_number = i + 1
                        st.rerun()
            
            # Calculate pagination
            start_idx = (st.session_state.page_number - 1) * RESULTS_PER_PAGE
            end_idx = start_idx + RESULTS_PER_PAGE
            page_results = st.session_state.search_results[start_idx:end_idx]
            
            # Display results
            from BaseTemplate import get_page_result_template
            for ad in page_results:
                col1, col2 = st.columns([4,1])
                with col1:
                    st.markdown(get_page_result_template(ad), unsafe_allow_html=True) 
                with col2: 
                    # Right column (View Details button)
                    st.markdown('<div class="search-result-right">', unsafe_allow_html=True)
                    if st.button("View Details", key=ad.id):
                        st.session_state.selected_ad = ad
                        st.rerun()   
            
        else:
            st.write("Found 0 results")
        
        st.markdown('</div>', unsafe_allow_html=True)