# Business Analitycs with Machine Learning Streamlit App.
**Idea**: A recommendation system for choosing an apartment for buying or
renting. 

**Problem**: A lot of products presented - requires a lot of manual
work for the searcher. 

Automating this, will allow people to spend less time on
this task. 

**Data sources**: ss.com, city24.lv Constraints: Only Riga, a
limited amount of options Possible attributes:

**Hard filters**:
Floor, type of building, price(could have a soft limit as well), amount of
rooms etc.

**Location**:
Use Open Street Map and find the nearest facilities:
- *positives*: school, kindergarten, bus stops, parks
- *negative*: factories, busy roads
  
**Optional things**: 
- Analyze description of the ad - what is good, what is
bad (probably LLMs) 
- Analyze images: was there any repairs, is it with furniture? (YOLO finetuning) 
  
**Technical solution**:
- Hardware: DigitalOcean barebone server + Ubuntu OS
- DB: Postgres + PostGIS
- Frontend + Backend: Streamlit

**Limitations**
 - nominatim location finder should be feeded with preprocessed adresses, otherwise it may fail to find the location with abbreviations or to descriptive names 
 - scorer function is time consuming - hardly can be used for a long lists
   - workaround: cache scores in db (ad_scores)

## DigitalOcean-Docker-Streamlit App.

Simple docker streamlit template app to be run on [DigitalOcean](https://m.do.co/c/4ab923d6fdc6) app platform.

To deploy you first need to click on "Use this template" and then simply log into your Digital Ocean account and click on "Apps" -> "Launch Your App" -> "Github" and select the corresponding Github repository.

You can use my [referral link](https://m.do.co/c/4ab923d6fdc6) to get $200 worth of credit over 60 days.

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%202.svg)](https://www.digitalocean.com/?refcode=4ab923d6fdc6&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)


To run locally, try:
```
cd ../app
docker build . -t streamlit_app
docker run -p 8501:8501 streamlit_app
```
