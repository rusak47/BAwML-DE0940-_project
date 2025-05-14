from datetime import datetime
from Range import Range

def create_search_form(st, db):
    with st.container():
        with st.sidebar.form("search_form"):
            # Search bar for general text search
            search_text = st.text_input("Search", st.session_state.search_text)

            # District search
            district = st.text_input("District")

            # Building type and series
            # Get building types from database
            # Initialize cache in session state if not exists
            if 'cache_building_types' not in st.session_state:
                st.session_state.cache_building_types = None
                st.session_state.cache_series = None
                st.session_state.last_cache_time = None

            # Check if cache needs refresh (every x hours)
            cache_expired = (
                st.session_state.last_cache_time is None or
                (datetime.now() - st.session_state.last_cache_time).total_seconds() > 1*60*60
            )

            if cache_expired or st.session_state.cache_building_types is None:
                with db:
                    st.session_state.cache_building_types = [""] + db.getBuildingTypeUnique()
                    st.session_state.cache_series = [""] + db.getBuildingSeriesUnique()
                    st.session_state.last_cache_time = datetime.now()

            building_type = st.selectbox("Building Type", st.session_state.cache_building_types)
            series = st.selectbox("Series", st.session_state.cache_series)

            # Create a container for number inputs
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    min_rooms = st.number_input("Min Rooms", min_value=0)
                    min_price = st.number_input("Min Price (€)", min_value=0)
                    min_area = st.number_input("Min Area (m²)", min_value=0)
                with col2:
                    max_rooms = st.number_input("Max Rooms", min_value=0)
                    max_price = st.number_input("Max Price (€)", min_value=0)
                    max_area = st.number_input("Max Area (m²)", min_value=0)

            submitted = st.form_submit_button("Search")

            if submitted or (search_text and not st.session_state.query_params_processed):                
                st.session_state.query_params_processed = True
                search(st, db, search_text, district, building_type, series, min_rooms, max_rooms, min_price, max_price, min_area, max_area)

def search(st, db, search_text=None, district=None, building_type=None, series=None, min_rooms=None, max_rooms=None, min_price=None, max_price=None, min_area=None, max_area=None):
    st.session_state.is_loading = True
    filters = {}

    if search_text:
        filters["search_text"] = search_text.lower()

    if district:
        filters["district"] = district.lower()

    if building_type and building_type != "":
        filters["building_type"] = building_type
    if series and series != "":
        filters["series"] = series

    if min_rooms or max_rooms:
        filters["nr_of_rooms"] = Range("nr_of_rooms", min_rooms if min_rooms else None,
                                        max_rooms if max_rooms else None)
    if min_price or max_price:
        filters["price"] = Range("price", min_price if min_price else None,
                                max_price if max_price else None)
    if min_area or max_area:
        filters["area_m2"] = Range("area_m2", min_area if min_area else None,
                                    max_area if max_area else None)

    st.session_state.page_number = 1 # Reset pagination
    with st.spinner('Loading...  Please be patient.'):
        with db:
            # First fetch all ads without calculating scores
            st.session_state.search_results = db.search_ads(filters, calculate_scores=False)

            # Now calculate scores for all ads in a separate step
            # This prevents rollbacks during page rendering
            if st.session_state.search_results:
                # Use the configuration values from config.yaml
                st.session_state.search_results = db.calculate_scores_for_ads(
                    st.session_state.search_results
                    # No need to specify max_scored_items and score_threshold
                    # as they will use the values from config.yaml
                )

        # kep outside of db context to avoid unintended transaction rollback
        st.session_state.is_loading = False
        st.rerun()
