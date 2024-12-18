import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px

def _hide_header():
    """Hide header of streamlit."""
    st.markdown(
        """
    <style>
    [data-testid="stHeader"]{
        display: none;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )



def get_img_histogram(img):
    img_gray = img.convert('L')
    img_flatten = np.array(img_gray).flatten()
    histogram = px.histogram(img_flatten, nbins=50, range_x=[0, 256], title='Histogram of Grayscale Image')
    histogram.update_layout(
        xaxis_title='Pixel Intensity',
        yaxis_title='Frequency',
        bargap=0.1
    )
    return histogram

def simple_thresholding(img, threshold):
    return

# Sidebar
def build_sidebar():
    sidebar_inputs = {}
    show_histogram = False
    # Load Image
    st.sidebar.subheader("Image loader")
    uploaded_img = st.sidebar.file_uploader("Choose an image")

    if uploaded_img is not None:
        try:
            img = Image.open(uploaded_img)
            st.session_state["img"] = img
        except IOError:
            st.error("El archivo subido no es una imagen válida.")
    else:
        st.session_state["img"] = None
    
    st.sidebar.divider()

    # Image Histogram
    if st.session_state["img"] is not None:
        st.sidebar.subheader("Image Histogram")
        show_histogram = st.sidebar.toggle("Show Histogram")

    # Sidebar Inputs
    sidebar_inputs = {
        "show_histogram": show_histogram,
    }

    return sidebar_inputs

# Main Page
def build_main_page(sidebar_inputs: dict[str, bool]) -> None:
    # Show Image
    cont1 = st.container()
    cont2 = st.container()

    col1_title, col2_title = cont1.columns(2)

    col1, col2 = cont2.columns(2)
    if st.session_state["img"] is not None:
        col1_title.subheader("Raw Image")
        col1.image(
            st.session_state["img"], 
            caption="Uploaded Image", 
            use_container_width=False,
            width=400
        )
    if sidebar_inputs["show_histogram"]:
        col2_title.subheader("Histogram")
        if st.session_state["img"] is not None:
            histogram = get_img_histogram(st.session_state["img"])
            col2.plotly_chart(histogram)
        else:
            col2.error("Please upload an image to show the histogram.")  

    st.divider()

#########################################################################

st.set_page_config(
    page_title="Komorebi AI - Consulta de Interacciones",
    layout="wide",
    page_icon="./src/streamlit_dashboard_interactions/assets/apple-touch-icon.png",
)

_hide_header()

if "img" not in st.session_state:
    st.session_state["img"] = None

# Show Sidebar
sidebar_inputs = build_sidebar()

# Show Main Page
build_main_page(sidebar_inputs)

# streamlit run test.py --server.address localhost --server.port 8502 --browser.gatherUsageStats false  # noqa: E501