def get_property_details_template(ad):
    return f"""
    <div class='content'>
        <div style='display: grid; grid-template-columns: 2fr 1fr; gap: 20px;'>
            <div>
                <!-- h2 style='color: #262730;'>Location</h2 -->
                <p><strong>District:</strong> {ad.district}</p>
                <p><strong>Street:</strong> {ad.street}</p>                
                <!-- h2 style='color: #262730;'>Property Details</h2 -->
                <p><strong>Area:</strong> {ad.area_m2}m²</p>
                <p><strong>Rooms:</strong> {ad.nr_of_rooms}</p>
                <p><strong>Floor:</strong> {ad.floor}/{ad.floor_max}</p>
                <p><strong>Series:</strong> {ad.series}</p>
                <p><strong>Building Type:</strong> {ad.building_type}</p>
                <p><strong>Extra:</strong> {ad.extra}</p>
            </div>
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px;'>
                <!-- h2 style='color: #262730;'>Price Information</h2 -->
                <p><strong>Price:</strong> €{ad.price:,.2f}</p>
                <p><strong>Price per m²:</strong> €{ad.price_m2:,.2f}</p>
                <p><strong>Source:</strong> <a href='{ad.site}' target='_blank'>{ad.site_id}</a></p>
                <!--p><strong>Site ID:</strong> {ad.site_id}</p -->
            </div>
        </div>
        <div class="img_preview" align="center">
            <div class="div_img_scroll" align="center">
                <img src="https://i.ss.com/hd-image/?img=RR5pTURxj4bfJCPGb3twfd6DedV0pFF8VRATtnjWVzBchxDUMSUbajfyRoIj8SjP&amp;key=Bkzj%252BiHYZpPLnf2JL3tbWuKMfbv4hWiNCKUGvfMT1oo%252ByA0Mn15jPiVE9Rny0O6QkWVw2sZkBH2ns4GUMjtR4HYMtipz7KU1V1GuHWJ4foQj9dh%252FMaiGk%252FrytyooEF%252By" height="683px" border="0"/>
            </div>
        </div>
        <div>
            <p>{ad.description}</p>
        </div>
    </div>
    """

from BaseTemplate import get_base_page_template
def show_details_page2(st):
    ad = st.session_state.selected_ad
    
    if st.button("← Back to Search"):
        st.session_state.selected_ad = None
        st.rerun()

    st.markdown(get_base_page_template("title", get_property_details_template(ad)), unsafe_allow_html=True)
    

def show_details_page(st):
    ad = st.session_state.selected_ad
    
    if st.button("← Back to Search"):
        st.session_state.selected_ad = None
        st.rerun()
    
    # Header
    st.markdown(f"<div class='property-header'><h1>Property in {ad.district}</h1></div>", unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='property-section'>", unsafe_allow_html=True)
        st.markdown("### Location")
        st.write(f"**District:** {ad.district}")
        st.write(f"**Street:** {ad.street}")
        
        st.markdown("### Property Details")
        st.write(f"**Area:** {ad.area_m2}m²")
        st.write(f"**Rooms:** {ad.nr_of_rooms}")
        st.write(f"**Floor:** {ad.floor}/{ad.floor_max}")
        st.write(f"**Series:** {ad.series}")
        st.write(f"**Building Type:** {ad.building_type}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='property-section price-box'>", unsafe_allow_html=True)
        st.markdown("### Price Information")
        st.write(f"**Price:** €{ad.price:,.2f}")
        st.write(f"**Price per m²:** €{ad.price_m2:,.2f}")
        st.write(f"**Source:** {ad.site}")
        st.write(f"**Site ID:** {ad.site_id}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional information
    if ad.extra:
        st.markdown("<div class='property-section'>", unsafe_allow_html=True)
        st.markdown("### Additional Information")
        st.write(ad.extra)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if ad.description:
        st.markdown("<div class='property-section'>", unsafe_allow_html=True)
        st.markdown("### Description")
        st.write(ad.description)
        st.markdown('</div>', unsafe_allow_html=True)
