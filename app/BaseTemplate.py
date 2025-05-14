def base_page_style_extended():
    return f"""
        <style>
            .main {{
                background-color: #f0f2f6;
                width: 100%;
                max-width: none;
            }}
            p {{
                text-align:justify;
            }}
            img {{
                width: 100%;
                //height: 100%;
                object-fit: cover;
                display: block;
            }}

            .div_img_preview {{
                position: relative;
                display: block;
                width: 911px;
                max-width: 100%;
                overflow: hidden;
                border: 1px solid rgb(204, 204, 204);
                cursor: pointer; margin: -1px;
                height: 512px;
            }}

            .div_img_scroll {{
                position: relative;
                display: block;
                z-index: 2;
                height: 512px;
                overflow: hidden scroll;
                width: 512px;
            }}

            .stApp {{
                max-width: none;
                margin: 0;
                padding: 20px;
            }}

            [data-testid="stMain"] {{
                margin-left: 0 !important;
                width: 100% !important;
            }}

            .search-result {{
                background-color: white !important;
                padding: 15px !important;
                border-radius: 10px !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                margin-bottom: 15px !important;
                width: 100% !important;
            }}
            .search-result-columns {{
                display: flex !important;
                gap: 20px !important;
                width: 100% !important;
            }}
            .search-result-preview {{
                min-width: 0 !important;
                width:90px;
                height:68px;
            }}
            .search-result-left {{
                flex: 3 !important;
                min-width: 0 !important;
            }}
            .search-result-middle {{
                flex: 2 !important;
                min-width: 0 !important;
            }}
            .search-result-right {{
                flex: 1 !important;
                min-width: 0 !important;
            }}

            /* Center spinner */
            .stSpinner {{
                position: fixed !important;
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, -50%) !important;
                z-index: 999991 !important;
                background-color: rgba(157, 157, 157, 0.76) !important;
                padding: 45% !important;
                border-radius: 10px !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                width: 100%;
                height: 100%;
                min-width: max-content !important;
            }}
            .stSpinner > div {{
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                gap: 10px !important;
            }}

            /* override thin main container to fill full page width */
            /*[data-testid=stMainBlockContainer] {{
                max-width:80%;
            }}*/
        </style>
    """

def base_page_style():
    return f"""
        <style>
            .header {{
                background-color: #262730;
                color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
            }}
            .content {{
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .back-button {{
                background-color: #262730;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 20px;
            }}
            .back-button:hover {{
                background-color: #3a3b45;
            }}
        </style>
    """

def get_base_page_template(title, content):
    return f"""
        <div class="container">
            <div class="header">
                <h1>{title}</h1>
            </div>{content}</div>
    """

def get_page_result_template(ad):
    # Safely format the score if available
    score_display = "<p></p>"
    try:
        if hasattr(ad, 'score') and ad.score is not None:
            score_display = f'<span style="color: green; font-weight: bold;">Score: {ad.score:.2f}</span>'
    except Exception:
        # If there's any error with the score, just don't display it
        pass

    return f"""
        <div class="search-result">
            <div class="search-result-columns">
                <div class="search-result-preview">
                    <img src="https://i.ss.com/gallery/7/1349/337075/67414858.th2.jpg" alt="" class="isfoto foto_list">
                </div>
                <!-- Left column (Location and details) -->
                <div class="search-result-left">
                    <p><strong>{ad.district}, {ad.street}</strong></p>
                    <p>{ad.area_m2} m² • {ad.nr_of_rooms} • {ad.floor}/{ad.floor_max}</p>
                    {score_display}
                </div>
                <!-- Middle column (Price) -->
                <div class="search-result-middle">
                    <p><strong>€ {ad.price}</strong></p>
                    <p>€ {ad.price_m2:.2f}/m²</p>
                </div>
                <!-- Right column (View Details button) -- >
                <div class="search-result-right">
                    <button class="view-details-button">View Details</button>
                </div-->
            </div>
        </div>
    """