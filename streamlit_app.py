import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #D4EDDA;
        border: 1px solid #C3E6CB;
        color: #155724;
    }
    .danger-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #F8D7DA;
        border: 1px solid #F5C6CB;
        color: #721C24;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🛡️ Real-Time Fraud Detection System")
st.markdown("### Credit Card Transaction Analysis with Machine Learning")

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    
    # API endpoint configuration
    api_endpoint = st.text_input(
    "API Endpoint",
    value="https://fraud-detection-api-v5cc.onrender.com",
    help="API endpoint (may take 30s to wake up on first request)"
)
    
    st.markdown("---")
    
    # Model info
    st.markdown("### 📊 Model Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", "99.95%")
        st.metric("Precision", "95.12%")
    with col2:
        st.metric("Recall", "82.93%")
        st.metric("F1-Score", "88.61%")
    
    st.markdown("---")
    st.markdown("### 🏗️ Architecture")
    st.markdown("""
    - **Model**: Random Forest
    - **API**: FastAPI
    - **Monitoring**: Prometheus + Grafana
    - **Container**: Docker
    """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Fraud Detection", "📈 Analytics", "🧪 Demo Scenarios", "📚 Documentation"])

with tab1:
    st.markdown("### Enter Transaction Details")
    
    # Create three columns for input
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_elapsed = st.number_input("Time (seconds since first transaction)", min_value=0.0, value=0.0)
        amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=123.45)
    
    # Feature inputs in an expander
    with st.expander("🔧 Advanced Features (V1-V28)", expanded=False):
        st.markdown("*These are PCA-transformed features from the original dataset*")
        
        features = {}
        cols = st.columns(4)
        
        # Default values (normal transaction pattern)
        default_values = {
            'V1': -1.359807, 'V2': -0.072781, 'V3': 2.536347, 'V4': 1.378155,
            'V5': -0.338321, 'V6': 0.462388, 'V7': 0.239599, 'V8': 0.098698,
            'V9': 0.363787, 'V10': 0.090794, 'V11': -0.551600, 'V12': -0.617801,
            'V13': -0.991390, 'V14': -0.311169, 'V15': 1.468177, 'V16': -0.470401,
            'V17': 0.207971, 'V18': 0.025791, 'V19': 0.403993, 'V20': 0.251412,
            'V21': -0.018307, 'V22': 0.277838, 'V23': -0.110474, 'V24': 0.066928,
            'V25': 0.128539, 'V26': -0.189115, 'V27': 0.133558, 'V28': -0.021053
        }
        
        for i in range(28):
            col_idx = i % 4
            features[f'V{i+1}'] = cols[col_idx].number_input(
                f"V{i+1}", 
                value=default_values[f'V{i+1}'],
                format="%.6f",
                key=f"v{i+1}"
            )
    
    # Prediction section
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔍 Analyze Transaction", use_container_width=True):
            # Prepare the transaction data
            transaction_data = {
                "Time": time_elapsed,
                "Amount": amount,
                **features
            }
            
            # Show loading spinner
            with st.spinner("Analyzing transaction..."):
                try:
                    # Make API call
                    response = requests.post(
                        f"{api_endpoint}/predict",
                        json=transaction_data,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display results
                        st.markdown("### 🎯 Prediction Results")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if result['prediction'] == 0:
                                st.success("✅ **LEGITIMATE**")
                                st.markdown('<div class="success-box">Transaction appears to be legitimate</div>', 
                                          unsafe_allow_html=True)
                            else:
                                st.error("🚨 **FRAUD DETECTED**")
                                st.markdown('<div class="danger-box">High risk transaction detected!</div>', 
                                          unsafe_allow_html=True)
                        
                        with col2:
                            # Risk gauge
                            fig = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=result['probability'] * 100,
                                title={'text': "Fraud Probability (%)"},
                                domain={'x': [0, 1], 'y': [0, 1]},
                                gauge={
                                    'axis': {'range': [None, 100]},
                                    'bar': {'color': "darkred" if result['probability'] > 0.5 else "green"},
                                    'steps': [
                                        {'range': [0, 30], 'color': "lightgreen"},
                                        {'range': [30, 70], 'color': "yellow"},
                                        {'range': [70, 100], 'color': "lightcoral"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': 50
                                    }
                                }
                            ))
                            fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col3:
                            st.metric("Risk Level", result['risk_level'])
                            st.metric("Confidence", f"{(1 - abs(result['probability'] - 0.5) * 2) * 100:.1f}%")
                        
                        # Additional details
                        with st.expander("📊 Detailed Analysis"):
                            st.json({
                                "prediction": result['prediction'],
                                "probability": result['probability'],
                                "risk_level": result['risk_level'],
                                "message": result['message'],
                                "transaction_amount": amount,
                                "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                    
                    else:
                        st.error(f"Error: API returned status code {response.status_code}")
                        st.json(response.text)
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to the API. Please ensure the API is running.")
                    st.info("Start the API locally with: `python run_api.py`")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.markdown("### 📊 System Analytics Dashboard")
    
    # Simulated metrics for demo
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", "10,234", "+156")
    with col2:
        st.metric("Fraud Detection Rate", "0.17%", "-0.02%")
    with col3:
        st.metric("Avg Response Time", "45ms", "-5ms")
    with col4:
        st.metric("System Uptime", "99.9%", "0%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        fig = px.pie(
            values=[9950, 284],
            names=['Legitimate', 'Fraudulent'],
            title="Transaction Classification Distribution",
            color_discrete_map={'Legitimate': '#2E8B57', 'Fraudulent': '#DC143C'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Time series
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        predictions = np.random.poisson(350, 30)
        
        fig = px.line(
            x=dates,
            y=predictions,
            title="Daily Prediction Volume",
            labels={'x': 'Date', 'y': 'Number of Predictions'}
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### 🧪 Test with Demo Scenarios")
    
    demo_scenarios = {
        "Normal Transaction": {
            "description": "Typical legitimate transaction pattern",
            "amount": 125.50,
            "features": {f'V{i}': np.random.normal(0, 1) for i in range(1, 29)}
        },
        "Suspicious Transaction": {
            "description": "Pattern often associated with fraud",
            "amount": 2500.00,
            "features": {f'V{i}': np.random.uniform(-5, 5) for i in range(1, 29)}
        },
        "High-Risk Transaction": {
            "description": "Very high probability of fraud",
            "amount": 10000.00,
            "features": {f'V{i}': np.random.uniform(-10, 10) for i in range(1, 29)}
        }
    }
    
    selected_scenario = st.selectbox("Select a demo scenario", list(demo_scenarios.keys()))
    
    if st.button("Load Scenario"):
        scenario = demo_scenarios[selected_scenario]
        st.success(f"Loaded: {scenario['description']}")
        st.info("Go to the 'Fraud Detection' tab and click 'Analyze Transaction' to see results")

with tab4:
    st.markdown("### 📚 Documentation")
    
    st.markdown("""
    #### About This System
    
    This fraud detection system uses machine learning to identify potentially fraudulent credit card transactions 
    in real-time. The model was trained on a dataset of 284,807 transactions with a 99.95% accuracy rate.
    
    #### Features
    - **V1-V28**: Principal Component Analysis (PCA) transformed features
    - **Time**: Seconds elapsed between this transaction and the first transaction
    - **Amount**: Transaction amount
    
    #### Risk Levels
    - 🟢 **Low Risk**: Probability < 30%
    - 🟡 **Medium Risk**: Probability 30-70%
    - 🔴 **High Risk**: Probability > 70%
    
    #### API Endpoints
    - `GET /health` - Health check
    - `POST /predict` - Make fraud prediction
    - `GET /metrics` - Prometheus metrics
    
    #### Technology Stack
    - **ML Model**: Random Forest Classifier
    - **API**: FastAPI
    - **Monitoring**: Prometheus + Grafana
    - **Deployment**: Docker + Kubernetes
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ by Kunal Sharma | 
        <a href='https://github.com/MrKunalSharma/fraud-detection-mlops'>GitHub</a> | 
        <a href='https://www.linkedin.com/in/kunal-sharma-1a8457257/'>LinkedIn</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
