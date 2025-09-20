import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Real-Time Fraud Detection System")
st.markdown("### Credit Card Transaction Analysis")

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    api_endpoint = "https://fraud-detection-api-v5cc.onrender.com"
    
    st.markdown("---")
    st.markdown("### 📊 Model Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", "99.95%")
    with col2:
        st.metric("F1-Score", "88.61%")
    
    st.markdown("---")
    st.info("💡 First prediction may take 30s as the API wakes up")

# Main interface
tab1, tab2 = st.tabs(["🔍 Make Prediction", "📚 About"])

with tab1:
    st.markdown("### Enter Transaction Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        amount = st.number_input("Amount ($)", min_value=0.0, value=149.62)
    with col2:
        time = st.number_input("Time", min_value=0.0, value=0.0)
    
    # Advanced features (collapsed by default)
    with st.expander("Advanced Features (V1-V28)"):
        st.info("For demo purposes, using default values. In production, these would be real transaction features.")
        use_default = st.checkbox("Use default values", value=True)
    
    if st.button("🔍 Analyze Transaction", type="primary", use_container_width=True):
        # Prepare transaction data
        transaction_data = {
            "Time": time,
            "Amount": amount
        }
        
        # Add V1-V28 features
        for i in range(1, 29):
            transaction_data[f'V{i}'] = 0.0  # Default values for demo
        
        with st.spinner("Analyzing transaction..."):
            try:
                response = requests.post(
                    f"{api_endpoint}/predict",
                    json=transaction_data,
                    timeout=35  # Longer timeout for cold start
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if result['prediction'] == 0:
                            st.success("✅ LEGITIMATE")
                        else:
                            st.error("🚨 FRAUD DETECTED")
                    
                    with col2:
                        # Create gauge chart
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=result['probability'] * 100,
                            title={'text': "Fraud Probability (%)"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "red" if result['probability'] > 0.5 else "green"},
                                'steps': [
                                    {'range': [0, 30], 'color': "lightgreen"},
                                    {'range': [30, 70], 'color': "yellow"},
                                    {'range': [70, 100], 'color': "lightcoral"}
                                ]
                            }
                        ))
                        fig.update_layout(height=200)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col3:
                        st.metric("Risk Level", result['risk_level'])
                        st.metric("Transaction Amount", f"${amount:,.2f}")
                    
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.warning("⏱️ API is waking up. Please try again in a moment.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Please check if it's running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    st.markdown("""
    ### About This System
    
    This fraud detection system uses machine learning to identify potentially fraudulent 
    credit card transactions in real-time.
    
    #### Features:
    - **99.95% Accuracy** on test dataset
    - **Real-time predictions** via REST API
    - **Risk scoring** (Low/Medium/High)
    - **Production monitoring** with Prometheus & Grafana
    
    #### Technology Stack:
    - **ML Model**: Random Forest Classifier
    - **API**: FastAPI deployed on Render
    - **UI**: Streamlit
    - **Monitoring**: Prometheus + Grafana (local)
    
    #### Links:
    - 📚 [API Documentation](https://fraud-detection-api-v5cc.onrender.com/docs)
    - 💻 [GitHub Repository](https://github.com/MrKunalSharma/fraud-detection-mlops)
    - 🔗 [LinkedIn](https://www.linkedin.com/in/kunal-sharma-1a8457257/)
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Kunal Sharma")
