import streamlit as st
import pandas as pd
import numpy as np
import base64
import json
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Professional Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define color themes with more vibrant colors
themes = {
    "light": {
        "primary": "#4361EE",
        "secondary": "#F5F5F5",
        "text": "#333333",
        "accent": "#F72585",
        "background": "#FFFFFF",
        "card": "#F9F9F9",
        "success": "#4CAF50",
        "info": "#3A86FF",
        "warning": "#FFBE0B",
        "danger": "#FF006E"
    },
    "dark": {
        "primary": "#4CC9F0",
        "secondary": "#1E1E1E",
        "text": "#E1E1E1",
        "accent": "#F72585",
        "background": "#121212",
        "card": "#1F1F1F",
        "success": "#4CAF50",
        "info": "#3A86FF",
        "warning": "#FFBE0B",
        "danger": "#FF006E"
    }
}

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'history' not in st.session_state:
    st.session_state.history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'navigation_selection' not in st.session_state:
    st.session_state.navigation_selection = None

# Apply custom CSS based on theme
def apply_theme(theme_name):
    theme = themes[theme_name]
    
    css = f"""
    <style>
        :root {{
            --primary: {theme["primary"]};
            --secondary: {theme["secondary"]};
            --text: {theme["text"]};
            --accent: {theme["accent"]};
            --background: {theme["background"]};
            --card: {theme["card"]};
        }}
        
        .stApp {{
            background-color: var(--background);
            color: var(--text);
        }}
        
        .stButton>button {{
            background-color: var(--primary);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            background-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .card {{
            background-color: var(--card);
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        .icon-text {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .result-card {{
            background-color: var(--primary);
            color: white;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            font-size: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        
        .sidebar .sidebar-content {{
            background-color: var(--secondary);
        }}
        
        h1, h2, h3 {{
            color: var(--primary);
        }}
        
        .stSelectbox label, .stNumberInput label {{
            color: var(--text);
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .card {{
                padding: 1rem;
            }}
            
            .result-card {{
                font-size: 1.2rem;
            }}
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# Apply the current theme
apply_theme(st.session_state.theme)

# Colorful SVG icons with dynamic color based on theme
def get_colored_icon(icon_name):
    theme_colors = themes[st.session_state.theme]
    
    # Define colors for different icon types
    icon_colors = {
        "length": theme_colors["primary"],
        "weight": theme_colors["accent"],
        "temperature": theme_colors["danger"],
        "volume": theme_colors["info"],
        "area": theme_colors["success"],
        "time": theme_colors["warning"],
        "speed": theme_colors["primary"],
        "pressure": theme_colors["info"],
        "energy": theme_colors["danger"],
        "data": theme_colors["success"],
        "history": theme_colors["warning"],
        "favorites": theme_colors["accent"],
        "settings": theme_colors["primary"],
        "theme": theme_colors["info"]
    }
    
    color = icon_colors.get(icon_name, theme_colors["primary"])
    
    icons = {
        "length": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20M2 12V6M22 12V6"/></svg>""",
        "weight": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12" y2="16"/></svg>""",
        "temperature": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>""",
        "volume": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 9l10-5 10 5v6l-10 5-10-5V9z"/><path d="M12 14v4"/><path d="M2 9l10 5 10-5"/></svg>""",
        "area": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg>""",
        "time": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>""",
        "speed": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>""",
        "pressure": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M2 12h20"/><path d="M12 22a10 10 0 0 0 0-20"/></svg>""",
        "energy": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>""",
        "data": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6" y2="6"/><line x1="6" y1="18" x2="6" y2="18"/></svg>""",
        "history": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M19 9l-5 5-4-4-3 3"/></svg>""",
        "favorites": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>""",
        "settings": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>""",
        "theme": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>""",
    }
    
    return base64.b64encode(icons[icon_name].encode()).decode()

# Function to create icons with text
def icon_text(icon, text):
    return f'<div class="icon-text"><img src="data:image/svg+xml;base64,{icon}" width="24" height="24"/> {text}</div>'

# Conversion functions
def length_conversion(value, from_unit, to_unit):
    # Base unit: meters
    conversion_factors = {
        "Millimeters": 0.001,
        "Centimeters": 0.01,
        "Meters": 1.0,
        "Kilometers": 1000.0,
        "Inches": 0.0254,
        "Feet": 0.3048,
        "Yards": 0.9144,
        "Miles": 1609.34
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def weight_conversion(value, from_unit, to_unit):
    # Base unit: grams
    conversion_factors = {
        "Milligrams": 0.001,
        "Grams": 1.0,
        "Kilograms": 1000.0,
        "Metric Tons": 1000000.0,
        "Ounces": 28.3495,
        "Pounds": 453.592,
        "Stone": 6350.29,
        "US Tons": 907185.0
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def temperature_conversion(value, from_unit, to_unit):
    # Special case for temperature
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        return ((value - 32) * 5/9) + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        return ((value - 273.15) * 9/5) + 32
    else:
        return value  # Same unit

def volume_conversion(value, from_unit, to_unit):
    # Base unit: liters
    conversion_factors = {
        "Milliliters": 0.001,
        "Liters": 1.0,
        "Cubic Meters": 1000.0,
        "US Fluid Ounces": 0.0295735,
        "US Cups": 0.236588,
        "US Pints": 0.473176,
        "US Quarts": 0.946353,
        "US Gallons": 3.78541,
        "Imperial Fluid Ounces": 0.0284131,
        "Imperial Cups": 0.284131,
        "Imperial Pints": 0.568261,
        "Imperial Quarts": 1.13652,
        "Imperial Gallons": 4.54609
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def area_conversion(value, from_unit, to_unit):
    # Base unit: square meters
    conversion_factors = {
        "Square Millimeters": 0.000001,
        "Square Centimeters": 0.0001,
        "Square Meters": 1.0,
        "Square Kilometers": 1000000.0,
        "Square Inches": 0.00064516,
        "Square Feet": 0.092903,
        "Square Yards": 0.836127,
        "Acres": 4046.86,
        "Square Miles": 2589988.11,
        "Hectares": 10000.0
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def time_conversion(value, from_unit, to_unit):
    # Base unit: seconds
    conversion_factors = {
        "Nanoseconds": 1e-9,
        "Microseconds": 1e-6,
        "Milliseconds": 0.001,
        "Seconds": 1.0,
        "Minutes": 60.0,
        "Hours": 3600.0,
        "Days": 86400.0,
        "Weeks": 604800.0,
        "Months (avg)": 2629746.0,
        "Years (avg)": 31556952.0
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def speed_conversion(value, from_unit, to_unit):
    # Base unit: meters per second
    conversion_factors = {
        "Meters per second": 1.0,
        "Kilometers per hour": 0.277778,
        "Miles per hour": 0.44704,
        "Feet per second": 0.3048,
        "Knots": 0.514444
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def pressure_conversion(value, from_unit, to_unit):
    # Base unit: pascals
    conversion_factors = {
        "Pascals": 1.0,
        "Kilopascals": 1000.0,
        "Megapascals": 1000000.0,
        "Bars": 100000.0,
        "Atmospheres": 101325.0,
        "Millimeters of Mercury": 133.322,
        "Inches of Mercury": 3386.39,
        "Pounds per Square Inch": 6894.76
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def energy_conversion(value, from_unit, to_unit):
    # Base unit: joules
    conversion_factors = {
        "Joules": 1.0,
        "Kilojoules": 1000.0,
        "Calories": 4.184,
        "Kilocalories": 4184.0,
        "Watt-hours": 3600.0,
        "Kilowatt-hours": 3600000.0,
        "Electron-volts": 1.602176634e-19,
        "British Thermal Units": 1055.06,
        "US Therms": 105506000.0,
        "Foot-pounds": 1.35582
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

def data_conversion(value, from_unit, to_unit):
    # Base unit: bytes
    conversion_factors = {
        "Bits": 0.125,
        "Bytes": 1.0,
        "Kilobits": 128.0,
        "Kilobytes": 1024.0,
        "Megabits": 131072.0,
        "Megabytes": 1048576.0,
        "Gigabits": 134217728.0,
        "Gigabytes": 1073741824.0,
        "Terabits": 137438953472.0,
        "Terabytes": 1099511627776.0,
        "Petabits": 140737488355328.0,
        "Petabytes": 1125899906842624.0
    }
    
    # Convert to base unit
    base_value = value * conversion_factors[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / conversion_factors[to_unit]
    
    return result

# Function to add conversion to history
def add_to_history(category, value, from_unit, to_unit, result):
    st.session_state.history.append({
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": result
    })
    
    # Keep only the last 50 conversions
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[-50:]

# Function to add conversion to favorites - FIXED
def add_to_favorites(category, value, from_unit, to_unit, result):
    favorite = {
        "category": category,
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": result
    }
    
    # Check if already in favorites
    if not any(f["category"] == favorite["category"] and 
               f["from_unit"] == favorite["from_unit"] and 
               f["to_unit"] == favorite["to_unit"] and 
               f["value"] == favorite["value"] for f in st.session_state.favorites):
        st.session_state.favorites.append(favorite)
        return True
    return False

# Function to remove from favorites
def remove_from_favorites(index):
    if 0 <= index < len(st.session_state.favorites):
        st.session_state.favorites.pop(index)
        return True
    return False

# Function to create a card with content
def create_card(title, content):
    st.markdown(f"""
    <div class="card">
        <h3>{title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)

# Function to display the result
def display_result(value, from_unit, to_unit, result):
    st.markdown(f"""
    <div class="result-card">
        {value} {from_unit} = {result:.8g} {to_unit}
    </div>
    """, unsafe_allow_html=True)

# Function to create a visualization for the conversion
def create_visualization(category, value, from_unit, to_unit, result):
    if category == "Length":
        fig = px.bar(
            x=[from_unit, to_unit],
            y=[value, result],
            labels={"x": "Unit", "y": "Value"},
            title=f"Length Conversion: {value} {from_unit} to {to_unit}",
            color_discrete_sequence=[themes[st.session_state.theme]["primary"], themes[st.session_state.theme]["accent"]]
        )
        return fig
    
    elif category == "Weight":
        fig = px.bar(
            x=[from_unit, to_unit],
            y=[value, result],
            labels={"x": "Unit", "y": "Value"},
            title=f"Weight Conversion: {value} {from_unit} to {to_unit}",
            color_discrete_sequence=[themes[st.session_state.theme]["primary"], themes[st.session_state.theme]["accent"]]
        )
        return fig
    
    elif category == "Temperature":
        # For temperature, use a gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result,
            title={"text": f"Temperature: {value} {from_unit} to {to_unit}"},
            gauge={
                "axis": {"range": [None, max(value, result) * 1.2]},
                "bar": {"color": themes[st.session_state.theme]["primary"]},
                "steps": [
                    {"range": [0, result], "color": themes[st.session_state.theme]["accent"]}
                ]
            }
        ))
        return fig
    
    elif category in ["Volume", "Area", "Time", "Speed", "Pressure", "Energy", "Data"]:
        # For other categories, use a simple comparison chart
        fig = px.bar(
            x=[from_unit, to_unit],
            y=[value, result],
            labels={"x": "Unit", "y": "Value"},
            title=f"{category} Conversion: {value} {from_unit} to {to_unit}",
            color_discrete_sequence=[themes[st.session_state.theme]["primary"], themes[st.session_state.theme]["accent"]]
        )
        
        # Use log scale for large differences
        if max(value, result) / min(value, result) > 1000:
            fig.update_layout(yaxis_type="log")
            
        return fig
    
    return None

# Main app
def main():
    # Sidebar
    with st.sidebar:
        st.title("Unit Converter")
        
        # Theme toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("Theme")
        with col2:
            if st.button("🌓"):
                st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
                st.rerun()
        
        # Navigation with colorful icons
        selected = option_menu(
            "Navigation",
            [
                "Length", "Weight", "Temperature", "Volume", 
                "Area", "Time", "Speed", "Pressure", 
                "Energy", "Data", "History", "Favorites", "Settings"
            ],
            icons=[
                "rulers", "weight", "thermometer", "droplet", 
                "square", "clock", "speedometer", "gauge", 
                "lightning", "hdd", "clock-history", "star", "gear"
            ],
            menu_icon="convert",
            default_index=0,
            styles={
                "icon": {"color": themes[st.session_state.theme]["primary"]},
                "nav-link-selected": {"background-color": themes[st.session_state.theme]["primary"]}
            }
        )
        
        # Check if we need to override the selection from favorites
        if st.session_state.navigation_selection is not None:
            selected = st.session_state.navigation_selection
            st.session_state.navigation_selection = None
    
    # Main content
    if selected in ["Length", "Weight", "Temperature", "Volume", "Area", "Time", "Speed", "Pressure", "Energy", "Data"]:
        st.title(f"{selected} Conversion")
        
        # Input section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<h3>From</h3>", unsafe_allow_html=True)
            
            # Different units based on the selected category
            if selected == "Length":
                units = ["Millimeters", "Centimeters", "Meters", "Kilometers", "Inches", "Feet", "Yards", "Miles"]
                from_unit = st.selectbox("From Unit", units, key="from_length")
                value = st.number_input("Value", value=1.0, key="value_length")
            
            elif selected == "Weight":
                units = ["Milligrams", "Grams", "Kilograms", "Metric Tons", "Ounces", "Pounds", "Stone", "US Tons"]
                from_unit = st.selectbox("From Unit", units, key="from_weight")
                value = st.number_input("Value", value=1.0, key="value_weight")
            
            elif selected == "Temperature":
                units = ["Celsius", "Fahrenheit", "Kelvin"]
                from_unit = st.selectbox("From Unit", units, key="from_temp")
                value = st.number_input("Value", value=0.0, key="value_temp")
            
            elif selected == "Volume":
                units = ["Milliliters", "Liters", "Cubic Meters", "US Fluid Ounces", "US Cups", "US Pints", "US Quarts", "US Gallons", "Imperial Fluid Ounces", "Imperial Cups", "Imperial Pints", "Imperial Quarts", "Imperial Gallons"]
                from_unit = st.selectbox("From Unit", units, key="from_volume")
                value = st.number_input("Value", value=1.0, key="value_volume")
            
            elif selected == "Area":
                units = ["Square Millimeters", "Square Centimeters", "Square Meters", "Square Kilometers", "Square Inches", "Square Feet", "Square Yards", "Acres", "Square Miles", "Hectares"]
                from_unit = st.selectbox("From Unit", units, key="from_area")
                value = st.number_input("Value", value=1.0, key="value_area")
            
            elif selected == "Time":
                units = ["Nanoseconds", "Microseconds", "Milliseconds", "Seconds", "Minutes", "Hours", "Days", "Weeks", "Months (avg)", "Years (avg)"]
                from_unit = st.selectbox("From Unit", units, key="from_time")
                value = st.number_input("Value", value=1.0, key="value_time")
            
            elif selected == "Speed":
                units = ["Meters per second", "Kilometers per hour", "Miles per hour", "Feet per second", "Knots"]
                from_unit = st.selectbox("From Unit", units, key="from_speed")
                value = st.number_input("Value", value=1.0, key="value_speed")
            
            elif selected == "Pressure":
                units = ["Pascals", "Kilopascals", "Megapascals", "Bars", "Atmospheres", "Millimeters of Mercury", "Inches of Mercury", "Pounds per Square Inch"]
                from_unit = st.selectbox("From Unit", units, key="from_pressure")
                value = st.number_input("Value", value=1.0, key="value_pressure")
            
            elif selected == "Energy":
                units = ["Joules", "Kilojoules", "Calories", "Kilocalories", "Watt-hours", "Kilowatt-hours", "Electron-volts", "British Thermal Units", "US Therms", "Foot-pounds"]
                from_unit = st.selectbox("From Unit", units, key="from_energy")
                value = st.number_input("Value", value=1.0, key="value_energy")
            
            elif selected == "Data":
                units = ["Bits", "Bytes", "Kilobits", "Kilobytes", "Megabits", "Megabytes", "Gigabits", "Gigabytes", "Terabits", "Terabytes", "Petabits", "Petabytes"]
                from_unit = st.selectbox("From Unit", units, key="from_data")
                value = st.number_input("Value", value=1.0, key="value_data")
        
        with col2:
            st.markdown(f"<h3>To</h3>", unsafe_allow_html=True)
            
            # Different units based on the selected category
            if selected == "Length":
                to_unit = st.selectbox("To Unit", units, index=2, key="to_length")
            elif selected == "Weight":
                to_unit = st.selectbox("To Unit", units, index=2, key="to_weight")
            elif selected == "Temperature":
                to_unit = st.selectbox("To Unit", units, index=1, key="to_temp")
            elif selected == "Volume":
                to_unit = st.selectbox("To Unit", units, index=1, key="to_volume")
            elif selected == "Area":
                to_unit = st.selectbox("To Unit", units, index=2, key="to_area")
            elif selected == "Time":
                to_unit = st.selectbox("To Unit", units, index=3, key="to_time")
            elif selected == "Speed":
                to_unit = st.selectbox("To Unit", units, index=1, key="to_speed")
            elif selected == "Pressure":
                to_unit = st.selectbox("To Unit", units, index=4, key="to_pressure")
            elif selected == "Energy":
                to_unit = st.selectbox("To Unit", units, index=2, key="to_energy")
            elif selected == "Data":
                to_unit = st.selectbox("To Unit", units, index=3, key="to_data")
        
        # Convert button
        if st.button("Convert", key=f"convert_{selected.lower()}"):
            # Perform conversion based on the selected category
            if selected == "Length":
                result = length_conversion(value, from_unit, to_unit)
            elif selected == "Weight":
                result = weight_conversion(value, from_unit, to_unit)
            elif selected == "Temperature":
                result = temperature_conversion(value, from_unit, to_unit)
            elif selected == "Volume":
                result = volume_conversion(value, from_unit, to_unit)
            elif selected == "Area":
                result = area_conversion(value, from_unit, to_unit)
            elif selected == "Time":
                result = time_conversion(value, from_unit, to_unit)
            elif selected == "Speed":
                result = speed_conversion(value, from_unit, to_unit)
            elif selected == "Pressure":
                result = pressure_conversion(value, from_unit, to_unit)
            elif selected == "Energy":
                result = energy_conversion(value, from_unit, to_unit)
            elif selected == "Data":
                result = data_conversion(value, from_unit, to_unit)
            
            # Display result
            display_result(value, from_unit, to_unit, result)
            
            # Add to history
            add_to_history(selected, value, from_unit, to_unit, result)
            
            # Create visualization
            fig = create_visualization(selected, value, from_unit, to_unit, result)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Add to favorites button - FIXED
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Add to Favorites", key=f"add_fav_{selected.lower()}"):
                    if add_to_favorites(selected, value, from_unit, to_unit, result):
                        st.success("Added to favorites!")
                    else:
                        st.info("This conversion is already in your favorites!")
        
        # Formula explanation
        with st.expander("Formula Explanation"):
            if selected == "Length":
                st.write("Length conversion is based on the meter as the base unit.")
                st.write("1 meter = 1000 millimeters = 100 centimeters = 0.001 kilometers")
                st.write("1 meter = 39.3701 inches = 3.28084 feet = 1.09361 yards = 0.000621371 miles")
            
            elif selected == "Weight":
                st.write("Weight conversion is based on the gram as the base unit.")
                st.write("1 kilogram = 1000 grams = 1,000,000 milligrams = 0.001 metric tons")
                st.write("1 kilogram = 35.274 ounces = 2.20462 pounds = 0.157473 stone = 0.00110231 US tons")
            
            elif selected == "Temperature":
                st.write("Temperature conversion formulas:")
                st.write("Celsius to Fahrenheit: °F = (°C × 9/5) + 32")
                st.write("Celsius to Kelvin: K = °C + 273.15")
                st.write("Fahrenheit to Celsius: °C = (°F - 32) × 5/9")
                st.write("Fahrenheit to Kelvin: K = (°F - 32) × 5/9 + 273.15")
                st.write("Kelvin to Celsius: °C = K - 273.15")
                st.write("Kelvin to Fahrenheit: °F = (K - 273.15) × 9/5 + 32")
            
            elif selected == "Volume":
                st.write("Volume conversion is based on the liter as the base unit.")
                st.write("1 liter = 1000 milliliters = 0.001 cubic meters")
                st.write("1 liter = 33.814 US fluid ounces = 4.22675 US cups = 2.11338 US pints = 1.05669 US quarts = 0.264172 US gallons")
                st.write("1 liter = 35.1951 Imperial fluid ounces = 3.51951 Imperial cups = 1.75975 Imperial pints = 0.879877 Imperial quarts = 0.219969 Imperial gallons")
            
            elif selected == "Area":
                st.write("Area conversion is based on the square meter as the base unit.")
                st.write("1 square meter = 1,000,000 square millimeters = 10,000 square centimeters = 0.000001 square kilometers")
                st.write("1 square meter = 1550 square inches = 10.7639 square feet = 1.19599 square yards = 0.000247105 acres = 3.86102e-7 square miles = 0.0001 hectares")
            
            elif selected == "Time":
                st.write("Time conversion is based on the second as the base unit.")
                st.write("1 second = 1,000,000,000 nanoseconds = 1,000,000 microseconds = 1,000 milliseconds")
                st.write("1 minute = 60 seconds")
                st.write("1 hour = 60 minutes = 3,600 seconds")
                st.write("1 day = 24 hours = 1,440 minutes = 86,400 seconds")
                st.write("1 week = 7 days = 168 hours = 10,080 minutes = 604,800 seconds")
                st.write("1 month (average) = 30.44 days = 730.5 hours = 43,830 minutes = 2,629,746 seconds")
                st.write("1 year (average) = 365.24 days = 8,765.76 hours = 525,946 minutes = 31,556,952 seconds")
            
            elif selected == "Speed":
                st.write("Speed conversion is based on meters per second as the base unit.")
                st.write("1 meter per second = 3.6 kilometers per hour = 2.23694 miles per hour = 3.28084 feet per second = 1.94384 knots")
            
            elif selected == "Pressure":
                st.write("Pressure conversion is based on the pascal as the base unit.")
                st.write("1 bar = 100,000 pascals = 100 kilopascals = 0.1 megapascals")
                st.write("1 atmosphere = 101,325 pascals = 101.325 kilopascals = 0.101325 megapascals = 1.01325 bars")
                st.write("1 atmosphere = 760 millimeters of mercury = 29.9213 inches of mercury = 14.6959 pounds per square inch")
            
            elif selected == "Energy":
                st.write("Energy conversion is based on the joule as the base unit.")
                st.write("1 kilojoule = 1,000 joules")
                st.write("1 calorie = 4.184 joules")
                st.write("1 kilocalorie = 4,184 joules = 4.184 kilojoules")
                st.write("1 watt-hour = 3,600 joules = 3.6 kilojoules")
                st.write("1 kilowatt-hour = 3,600,000 joules = 3,600 kilojoules = 860.421 kilocalories")
                st.write("1 British thermal unit = 1,055.06 joules = 1.05506 kilojoules = 0.252164 kilocalories")
            
            elif selected == "Data":
                st.write("Data conversion is based on the byte as the base unit.")
                st.write("1 byte = 8 bits")
                st.write("1 kilobyte = 1,024 bytes = 8,192 bits")
                st.write("1 megabyte = 1,048,576 bytes = 8,388,608 bits = 1,024 kilobytes")
                st.write("1 gigabyte = 1,073,741,824 bytes = 8,589,934,592 bits = 1,048,576 kilobytes = 1,024 megabytes")
                st.write("1 terabyte = 1,099,511,627,776 bytes = 8,796,093,022,208 bits = 1,073,741,824 kilobytes = 1,048,576 megabytes = 1,024 gigabytes")
    
    # History page
    elif selected == "History":
        st.title("Conversion History")
        
        if not st.session_state.history:
            st.info("No conversion history yet. Try converting some units first!")
        else:
            # Create a DataFrame from the history
            history_df = pd.DataFrame(st.session_state.history)
            
            # Display the history
            st.dataframe(history_df, use_container_width=True)
            
            # Clear history button
            if st.button("Clear History"):
                st.session_state.history = []
                st.success("History cleared!")
                st.rerun()
            
            # Visualize history
            if len(st.session_state.history) > 1:
                st.subheader("Conversion Categories")
                
                # Count the categories
                category_counts = history_df["category"].value_counts().reset_index()
                category_counts.columns = ["Category", "Count"]
                
                # Create a pie chart
                fig = px.pie(
                    category_counts,
                    values="Count",
                    names="Category",
                    title="Conversion Categories Distribution",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Favorites page - FIXED
    elif selected == "Favorites":
        st.title("Favorite Conversions")
        
        if not st.session_state.favorites:
            st.info("No favorite conversions yet. Add some from the conversion pages!")
        else:
            # Display each favorite conversion
            for i, favorite in enumerate(st.session_state.favorites):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{favorite['category']}**: {favorite['value']} {favorite['from_unit']} = {favorite['result']:.8g} {favorite['to_unit']}")
                
                with col2:
                    # Use this favorite button
                    if st.button("Use", key=f"use_fav_{i}"):
                        # Set session state variables for the conversion page
                        category = favorite['category'].lower()
                        st.session_state[f"from_{category}"] = favorite['from_unit']
                        st.session_state[f"to_{category}"] = favorite['to_unit']
                        st.session_state[f"value_{category}"] = favorite['value']
                        # Navigate to the appropriate conversion page
                        st.session_state.navigation_selection = favorite['category']
                        st.rerun()
                
                with col3:
                    # Remove from favorites button
                    if st.button("Remove", key=f"remove_fav_{i}"):
                        if remove_from_favorites(i):
                            st.success("Removed from favorites!")
                            st.rerun()
                
                st.markdown("---")
            
            # Clear all favorites button
            if st.button("Clear All Favorites"):
                st.session_state.favorites = []
                st.success("All favorites cleared!")
                st.rerun()
    
    # Settings page
    elif selected == "Settings":
        st.title("Settings")
        
        # Theme settings
        st.subheader("Theme")
        theme_option = st.radio(
            "Select Theme",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "light" else 1
        )
        
        if theme_option == "Light" and st.session_state.theme != "light":
            st.session_state.theme = "light"
            st.rerun()
        elif theme_option == "Dark" and st.session_state.theme != "dark":
            st.session_state.theme = "dark"
            st.rerun()
        
        # Decimal places
        st.subheader("Decimal Places")
        decimal_places = st.slider("Number of decimal places to display", 0, 10, 8)
        
        # Export/Import data
        st.subheader("Export/Import Data")
        
        # Export
        if st.button("Export Settings and Favorites"):
            export_data = {
                "theme": st.session_state.theme,
                "favorites": st.session_state.favorites,
                "decimal_places": decimal_places
            }
            
            # Convert to JSON
            json_data = json.dumps(export_data)
            
            # Create a download link
            b64 = base64.b64encode(json_data.encode()).decode()
            href = f'<a href="data:application/json;base64,{b64}" download="unit_converter_settings.json">Download Settings</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        # Import
        st.subheader("Import Settings")
        uploaded_file = st.file_uploader("Upload settings file", type=["json"])
        
        if uploaded_file is not None:
            try:
                import_data = json.load(uploaded_file)
                
                # Update session state
                if "theme" in import_data:
                    st.session_state.theme = import_data["theme"]
                
                if "favorites" in import_data:
                    st.session_state.favorites = import_data["favorites"]
                
                st.success("Settings imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing settings: {e}")
        
        # About section
        st.subheader("About")
        st.write("Professional Unit Converter App")
        st.write("Version 1.0")
        st.write("Created by FARWA KANWAL ❤ with Streamlit")

# Run the app
if __name__ == "__main__":
    main()