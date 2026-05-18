import streamlit as st
import requests

# 1. Page Configuration (Sets the browser tab title and icon)
st.set_page_config(
    page_title="MLABS GEO Audit",
    page_icon="🚀",
    layout="centered"
)

# 2. Header Section
st.title("🚀 MLABS GEO Audit Engine")
st.markdown("""
Enter your details below to generate a comprehensive **Generative Engine Optimization (GEO)** audit. 
Our AI will analyze your website and compare it against industry standards.
""")
st.divider()

# 3. The User Input Form
with st.form(key='lead_form'):
    st.subheader("Lead Information")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Jane Doe")
    with col2:
        email = st.text_input("Work Email", placeholder="jane@company.com")
        
    company_name = st.text_input("Company Name", placeholder="e.g., Apple")
    company_url = st.text_input("Company URL", placeholder="https://www.apple.com")
    
    # The submit button
    submit_button = st.form_submit_button(label="Generate My Audit", use_container_width=True)

# 4. Form Submission Logic
if submit_button:
    # Basic frontend validation
    if not name or not email or not company_name or not company_url:
        st.warning("⚠️ Please fill out all fields before submitting.")
    else:
        # Show a beautiful loading spinner while the API works
        with st.spinner(f"Scraping {company_url} and running AI analysis... This usually takes 15-30 seconds."):
            
            # The data we are sending to your FastAPI backend
            payload = {
                "name": name,
                "email": email,
                "company_name": company_name,
                "company_url": company_url
            }
            
            try:
                # Make the POST request to your local FastAPI server
                response = requests.post("https://geo-audit-platform.onrender.com", json=payload)
                
                # Check the response from the backend
                if response.status_code == 200:
                    data = response.json()
                    st.success(f" Success! {data['message']}")
                    st.balloons() # Fun Streamlit animation!
                    
                elif response.status_code == 422:
                    st.error(" Invalid data format. Please check your URL (must include http/https) and Email.")
                    
                else:
                    st.error(" Something went wrong on the server. Please try again.")
                    
            except requests.exceptions.ConnectionError:
                st.error(" Could not connect to the API. Make sure your FastAPI server is running on port 8000!")