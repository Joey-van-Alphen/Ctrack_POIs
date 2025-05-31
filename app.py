
# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium.plugins import Draw

# Streamlit app title
st.title("Interactive Polygon Editor")

# Load the data
@st.cache_data
def load_data():
    return pd.read_excel("Ctrack_POIs.xlsx")

try:
    data = load_data()
except Exception as e:
    st.error(f"Kon bestand niet laden: {e}")
    st.stop()

# Create a base map
m = folium.Map(location=[52.0, 5.0], zoom_start=7)

# Add existing polygons to the map
for index, row in data.iterrows():
    latlon_points = row['LatLonOtherPoints'].split('|')
    coordinates = [(float(latlon_points[i+1]), float(latlon_points[i])) for i in range(0, len(latlon_points), 2)]
    folium.Polygon(
        locations=coordinates,
        color='blue',
        fill=True,
        fill_opacity=0.4,
        tooltip=row['Description']
    ).add_to(m)

# Add drawing tools
Draw(export=True).add_to(m)

# Display map
st_data = st_folium(m, width=700, height=500)

# Polygon naming
st.sidebar.header("Polygon Naming")
polygon_name = st.sidebar.text_input("Enter a name for the polygon:")

# Save drawn polygon
if st.sidebar.button("Save Polygon"):
    if 'all_drawings' in st_data and st_data['all_drawings']:
        new_polygon = st_data['all_drawings'][-1]  # Last drawn shape
        new_polygon['name'] = polygon_name

        # Save coordinates in LatLon format
        coords = new_polygon['geometry']['coordinates'][0]
        flat_coords = '|'.join([f"{pt[0]}|{pt[1]}" for pt in coords])
        df = pd.DataFrame([{
            'Description': polygon_name,
            'LatLonOtherPoints': flat_coords
        }])

        try:
            df.to_csv("Updated_Ctrack_POIs.csv", mode='a', header=False, index=False)
            st.success("Polygon saved to Updated_Ctrack_POIs.csv")
        except Exception as e:
            st.error(f"Fout bij opslaan: {e}")
    else:
        st.error("Geen polygon getekend.")
