# #our packages:
# import streamlit as st
# import requests
# import geopandas as gpd
# from streamlit_folium import folium_static
# import leafmap.foliumap as leafmapap


# @st.cache_data()
# def load_data():
#     world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#     return world


# def get_country_details(country_name):
#     url = f"https://restcountries.com/v2/name/{country_name}"
#     response = requests.get(url)

#     if response.status_code == 404:
#         return "Sorry, no details found for this country."
#     else:
#         data = response.json()[0]
#         borders = ", ".join(data.get('borders', [])) or "None"
#         return f"""
#             {data['name']}
#             Capital: {data['capital']}
#             Population: {data['population']}
#             Region: {data['region']}
#             Subregion: {data['subregion']}
#             Languages: {", ".join([lang['name'] for lang in data['languages']])}
#             Currencies: {", ".join([cur['name'] for cur in data['currencies']])}
#             Neighbors: {borders}
#             """

# def app():
#     st.title('Geocoding App')
#     world = load_data()

#     continent = st.selectbox('Select a continent', world.continent.unique())

#     countries_in_continent = world[world.continent == continent]

#     country_name = st.text_input('Enter a country name')
#     if country_name:
#         selected_country = countries_in_continent[countries_in_continent['name'].str.lower()
#                                                   == country_name.lower()]
#         if len(selected_country) == 0:
#             st.error('No results found')
#         else:
#             st.success(f'Selected country: {country_name}')
#             country_details = get_country_details(country_name)
#             st.text_area('Country Details', country_details)
#             center_lat = selected_country.geometry.centroid.y.values[0]
#             center_lon = selected_country.geometry.centroid.x.values[0]
#             zoom_level = 5
#             m = leafmapap.Map(center=[center_lat, center_lon], zoom=zoom_level)
#             def style_function(x): return {'fillOpacity': 0.5}
#             m.add_gdf(selected_country, style_function=style_function)
#             folium_static(m)

#             # Add download button
#             geojson = selected_country.to_json()
#             file_name = f"{selected_country.iloc[0]['name']}.geojson"
#             st.download_button(
#                 label="Download GeoJSON",
#                 data=geojson,
#                 file_name=file_name,
#                 mime="application/json"
#             )


# if __name__ == '__main__':
#     app()













#our packages:
import streamlit as st
import requests
import geopandas as gpd
from streamlit_folium import folium_static
import leafmap.foliumap as leafmapap

#for enable caching(data loaded only once and subsequent calls to the function will use the cached data)
@st.cache_data()
#this is our function to load the Natural Earth dataset from GeoPandas.
def loading_our_data():
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    return world

#function to retrieve details about a country from the Rest Countries API.
def get_country_details(country_name):
    url = f"https://restcountries.com/v2/name/{country_name}"
#request library to send a get request to the API... returns a string containing details about the country.
    response = requests.get(url) 
#Handling error:
    if response.status_code == 404:
        return "No data is available for this country..try again!."
#extracts the JSON data from the response using the response.json()function 
    else:
        info = response.json()[0]
#To Know the neighbouring countries
        borders = ", ".join(info.get('borders', [])) or "None"
#informations about the country from the JSON data
        return f"""
            {info['name']}
            Capital: {info['capital']}
            Population: {info['population']}
            Region: {info['region']}
            Subregion: {info['subregion']}
            Languages: {", ".join([lang['name'] for lang in info['languages']])}
            Currencies: {", ".join([cur['name'] for cur in info['currencies']])}
            Neighbors: {borders}
            """

def app():
    st.title('Geocoding App')
    world = loading_our_data()
 #select box using Streamlit's selectbox function to choose the continent
    continent = st.selectbox('Select a continent :', world.continent.unique())
#the continent that user selected match the continent in world dataset
    countries_in_continent = world[world.continent == continent]
#choose country
    country_name = st.text_input('Enter a country name :')
    if country_name:
        selected_country = countries_in_continent[countries_in_continent['name'].str.lower() == country_name.lower()]
#handling error
        if len(selected_country) == 0:
            st.error('No Data Available!')
#text area with the name of country
        else:
            st.success(f'Selected country: {country_name}')
            country_details = get_country_details(country_name)
            st.text_area('Country Details :', country_details)
#create a map using the Leafmap library 
            center_lat = selected_country.geometry.centroid.y.values[0]
            center_lon = selected_country.geometry.centroid.x.values[0]
            zoom_level = 5
            map = leafmapap.Map(center=[center_lat, center_lon], zoom=zoom_level)
            def style_function(x): return {'fillOpacity': 0.5}
            map.add_gdf(selected_country, style_function=style_function)
            folium_static(map)

# Add download button
            geojson = selected_country.to_json()
            file_name = f"{selected_country.iloc[0]['name']}.geojson"
            st.download_button(
                label="Download GeoJSON",
                data=geojson,
                file_name=file_name,
                mime="application/json"
            )


if __name__ == '__main__':
    app()