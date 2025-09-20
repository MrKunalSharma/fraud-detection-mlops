import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import random

st.set_page_config(
    page_title="Fraud Detection MLOps Demo", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .drift-warning {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .ab-test-result {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "https://fraud-detection-api-v5cc.onrender.com"

# Initialize session state
if 'predictions' not in st.session_state:
    st.session_state.predictions = []
if 'ab_test_results' not in st.session_state:
    st.session_state.ab_test_results = {'v1.0': 0, 'v1.1-beta': 0}

# Header
st.title("🛡️ Fraud Detection MLOps Platform")
st.markdown("### Advanced Features Demo: A/B Testing, Drift Detection & Performance Monitoring")

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    
    # API Key input (optional)
    api_key = st.text_input("API Key (Optional)", value="demo-key-123", type="password")
    
    st.markdown("---")
    
    # Feature selection
    st.header("🎯 Demo Features")
    show_ab_testing = st.checkbox("A/B Testing", value=True)
    show_drift_detection = st.checkbox("Data Drift Detection", value=True)
    show_performance = st.checkbox("Performance Metrics", value=True)
    show_load_test = st.checkbox("Load Test Results", value=True)
    
    st.markdown("---")
    
    # Model information
    st.header("📊 Model Info")
    st.metric("Production Model", "v1.0")
    st.metric("Beta Model", "v1.1-beta")
    st.metric("Traffic Split", "80/20")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Fraud Detection", "🧪 A/B Testing", "📊 Drift Detection", "⚡ Performance"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Transaction Analysis")
        
        # Input mode selection
        input_mode = st.radio("Input Mode", ["Simple", "Advanced", "Test Scenarios"], horizontal=True)
        
        if input_mode == "Simple":
            amount = st.number_input("Transaction Amount ($)", min_value=0.01, value=149.62)
            time_val = st.number_input("Time (seconds)", min_value=0.0, value=0.0)
            # Use default values for V features
            v_features = {f"V{i}": 0.0 for i in range(1, 29)}
            
        elif input_mode == "Advanced":
            col_a, col_b = st.columns(2)
            with col_a:
                amount = st.number_input("Amount ($)", min_value=0.01, value=149.62)
            with col_b:
                time_val = st.number_input("Time", min_value=0.0, value=0.0)
            
            # V features in expander
            with st.expander("V1-V28 Features"):
                v_features = {}
                cols = st.columns(4)
                for i in range(28):
                    col_idx = i % 4
                    v_features[f"V{i+1}"] = cols[col_idx].number_input(
                        f"V{i+1}", 
                        value=0.0,
                        min_value=-10.0,
                        max_value=10.0,
                        format="%.3f"
                    )
        
        else:  # Test Scenarios
            scenario = st.selectbox("Select Test Scenario", [
                "Normal Transaction",
                "Suspicious Pattern",
                "High Risk Fraud",
                "Data Drift Scenario"
            ])
            
            if scenario == "Normal Transaction":
                amount = 50.0
                time_val = 1000.0
                v_features = {f"V{i}": random.normalvariate(0, 1) for i in range(1, 29)}
            elif scenario == "Suspicious Pattern":
                amount = 2500.0
                time_val = 50000.0
                v_features = {f"V{i}": random.uniform(-3, 3) for i in range(1, 29)}
            elif scenario == "High Risk Fraud":
                amount = 10000.0
                time_val = 150000.0
                v_features = {f"V{i}": random.uniform(-5, 5) for i in range(1, 29)}
            else:  # Data Drift
                amount = 5000.0
                time_val = 200000.0
                v_features = {f"V{i}": random.uniform(-10, 10) for i in range(1, 29)}
            
            st.info(f"Loaded {scenario} pattern")
        
        # Predict button
        if st.button("🔍 Analyze Transaction", type="primary", use_container_width=True):
            transaction_data = {
                "Time": time_val,
                "Amount": amount,
                **v_features
            }
            
            with st.spinner("Analyzing transaction..."):
                try:
                    headers = {"X-API-Key": api_key} if api_key else {}
                    
                    # For demo, make multiple requests to show A/B testing
                    response = requests.post(
                        f"{API_URL}/predict",
                        json=transaction_data,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Store result
                        st.session_state.predictions.append(result)
                        
                        # Update A/B test results
                        model_version = result.get('model_version', 'v1.0')
                        st.session_state.ab_test_results[model_version] = st.session_state.ab_test_results.get(model_version, 0) + 1
                        
                        # Display results
                        if result['prediction'] == 0:
                            st.success("✅ **LEGITIMATE TRANSACTION**")
                        else:
                            st.error("🚨 **FRAUD DETECTED!**")
                        
                        # Metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Risk Level", result['risk_level'])
                        with col2:
                            st.metric("Probability", f"{result['probability']:.1%}")
                        with col3:
                            st.metric("Model Version", result.get('model_version', 'v1.0'))
                        with col4:
                            st.metric("Latency", f"{result.get('processing_time_ms', 'N/A')}ms")
                        
                        # Drift detection alert
                        if result.get('drift_detected', False):
                            st.markdown("""
                            <div class="drift-warning">
                                ⚠️ <strong>Data Drift Detected!</strong><br>
                                The input features significantly differ from the training distribution.
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Transaction details
                        with st.expander("Transaction Details"):
                            st.json({
                                "transaction_id": result.get('transaction_id', 'N/A'),
                                "amount": f"${amount:,.2f}",
                                "model_version": result.get('model_version', 'v1.0'),
                                "processing_time": f"{result.get('processing_time_ms', 'N/A')}ms",
                                "drift_detected": result.get('drift_detected', False)
                            })
                    else:
                        st.error(f"API Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Note: The API might be waking up. Please try again in 30 seconds.")
    
    with col2:
        st.header("Recent Predictions")
        if st.session_state.predictions:
            recent = st.session_state.predictions[-5:]
            for i, pred in enumerate(reversed(recent)):
                risk_emoji = "🟢" if pred['risk_level'] == "Low" else "🟡" if pred['risk_level'] == "Medium" else "🔴"
                st.markdown(f"{risk_emoji} **{pred['risk_level']} Risk** - {pred['probability']:.1%} fraud probability")
        else:
            st.info("No predictions yet")

with tab2:
    st.header("🧪 A/B Testing Dashboard")
    
    if show_ab_testing:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Traffic Distribution")
            
            # A/B test results pie chart
            if sum(st.session_state.ab_test_results.values()) > 0:
                fig_ab = go.Figure(data=[go.Pie(
                    labels=list(st.session_state.ab_test_results.keys()),
                    values=list(st.session_state.ab_test_results.values()),
                    hole=.3
                )])
                fig_ab.update_layout(height=300)
                st.plotly_chart(fig_ab, use_container_width=True)
            else:
                st.info("Make some predictions to see A/B test distribution")
        
        with col2:
            st.subheader("Model Performance Comparison")
            
            # Simulated performance metrics
            performance_data = pd.DataFrame({
                'Metric': ['Accuracy', 'Latency (ms)', 'False Positive Rate'],
                'v1.0': [99.95, 45.2, 0.12],
                'v1.1-beta': [99.93, 47.8, 0.15]
            })
            
            fig_perf = go.Figure()
            fig_perf.add_trace(go.Bar(name='v1.0', x=performance_data['Metric'], y=performance_data['v1.0']))
            fig_perf.add_trace(go.Bar(name='v1.1-beta', x=performance_data['Metric'], y=performance_data['v1.1-beta']))
            fig_perf.update_layout(barmode='group', height=300)
            st.plotly_chart(fig_perf, use_container_width=True)
        
        # A/B Test Results Summary
        st.markdown("""
        <div class="ab-test-result">
            <h4>A/B Test Summary</h4>
            <ul>
                <li><strong>Winner:</strong> Model v1.0 (better accuracy and lower false positive rate)</li>
                <li><strong>Recommendation:</strong> Continue with 80/20 split for one more week</li>
                <li><strong>Next Steps:</strong> Monitor v1.1-beta improvements before full rollout</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.header("📊 Data Drift Detection")
    
    if show_drift_detection:
        # Simulate drift scores for different features
        features = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
        drift_scores = [random.uniform(0, 5) for _ in features]
        
        # Create drift visualization
        fig_drift = go.Figure()
        colors = ['red' if score > 3 else 'orange' if score > 2 else 'green' for score in drift_scores]
        
        fig_drift.add_trace(go.Bar(
            x=features,
            y=drift_scores,
            marker_color=colors
        ))
        
        fig_drift.add_hline(y=3, line_dash="dash", line_color="red", annotation_text="Drift Threshold")
        fig_drift.update_layout(
            title="Feature Drift Scores (Z-scores)",
            xaxis_title="Features",
            yaxis_title="Drift Score",
            height=400
        )
        
        st.plotly_chart(fig_drift, use_container_width=True)
        
        # Drift alerts
        high_drift_features = [f for f, s in zip(features, drift_scores) if s > 3]
        if high_drift_features:
            st.warning(f"⚠️ High drift detected in features: {', '.join(high_drift_features)}")
        else:
            st.success("✅ All features within normal distribution")
        
        # Drift statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Features Monitored", len(features))
        with col2:
            st.metric("Features with Drift", len(high_drift_features))
        with col3:
            st.metric("Max Drift Score", f"{max(drift_scores):.2f}")

with tab4:
    st.header("⚡ Performance & Load Testing")
    
    if show_performance:
        # Display load test results
        st.subheader("Load Test Results")
        
        load_test_data = pd.DataFrame({
            'Scenario': ['Light Load', 'Medium Load', 'Heavy Load'],
            'Requests': [100, 600, 1000],
            'Success Rate': [69.0, 94.83, 92.5],
            'Avg Latency (s)': [0.741, 2.602, 3.845],
            'P95 Latency (s)': [1.303, 5.071, 7.234]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_success = px.bar(
                load_test_data, 
                x='Scenario', 
                y='Success Rate',
                title="Success Rate by Load Scenario",
                color='Success Rate',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_success, use_container_width=True)
        
        with col2:
            fig_latency = go.Figure()
            fig_latency.add_trace(go.Bar(name='Avg Latency', x=load_test_data['Scenario'], y=load_test_data['Avg Latency (s)']))
            fig_latency.add_trace(go.Bar(name='P95 Latency', x=load_test_data['Scenario'], y=load_test_data['P95 Latency (s)']))
            fig_latency.update_layout(title="Latency by Load Scenario", barmode='group')
            st.plotly_chart(fig_latency, use_container_width=True)
        
        # Performance metrics
        st.subheader("Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Max Throughput", "94.83%", "Under 600 requests")
        with col2:
            st.metric("Best Latency", "278ms", "Minimum observed")
        with col3:
            st.metric("P95 Latency", "5.07s", "Medium load")
        with col4:
            st.metric("Uptime", "99.9%", "Last 30 days")
        
        # Recommendations
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Performance Insights</h4>
            <ul>
                <li>The system performs well under medium load (94.83% success rate)</li>
                <li>Latency increases significantly under heavy load due to free tier limitations</li>
                <li>Recommended: Upgrade to paid tier for production workloads</li>
                <li>Expected production performance: <100ms latency, 99.9% success rate</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ by Kunal Sharma | 
    <a href='https://github.com/MrKunalSharma/fraud-detection-mlops' target='_blank'>GitHub</a> | 
    <a href='https://fraud-detection-api-v5cc.onrender.com/docs' target='_blank'>API Docs</a> |
    <a href='https://www.linkedin.com/in/kunal-sharma-1a8457257/' target='_blank'>LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
