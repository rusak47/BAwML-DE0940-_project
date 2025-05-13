
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
                # Create columns for pagination: first, prev button, page numbers, next, last button
                first_col, prev_col, *page_cols, next_col, last_col = st.columns([1, 1] + [1] * 11 + [1, 1])

                # First page button
                if first_col.button("« ", key="first_button", disabled=(st.session_state.page_number <= 1)):
                    st.session_state.page_number = 1
                    st.rerun()

                # Previous button
                if prev_col.button("‹ ", key="prev_button", disabled=(st.session_state.page_number <= 1)):
                    st.session_state.page_number = max(1, st.session_state.page_number - 1)
                    st.rerun()

                # Calculate which page numbers to show
                current_page = st.session_state.page_number

                # Determine the range of page numbers to display
                if total_pages <= 11:
                    # If we have 11 or fewer pages, show all of them
                    start_page = 1
                    end_page = total_pages
                else:
                    # We need to show a window of pages around the current page
                    # Show 5 pages before and 5 pages after the current page when possible
                    start_page = max(1, current_page - 5)
                    end_page = min(total_pages, start_page + 10)

                    # Adjust if we're near the end
                    if end_page == total_pages:
                        start_page = max(1, end_page - 10)

                # Page number buttons
                page_numbers = list(range(start_page, end_page + 1))
                for i, page_num in enumerate(page_numbers):
                    if i < len(page_cols):
                        if page_cols[i].button(str(page_num), key=f"page_{page_num}",
                                        disabled=(page_num == current_page)):
                            st.session_state.page_number = page_num
                            st.rerun()

                # Next button
                if next_col.button(" ›", key="next_button", disabled=(st.session_state.page_number >= total_pages)):
                    st.session_state.page_number = min(total_pages, st.session_state.page_number + 1)
                    st.rerun()

                # Last page button
                if last_col.button(" »", key="last_button", disabled=(st.session_state.page_number >= total_pages)):
                    st.session_state.page_number = total_pages
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