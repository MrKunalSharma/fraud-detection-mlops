import streamlit as st
import requests
import json

st.set_page_config(page_title="Fraud Detection Demo", page_icon="🛡️", layout="wide")

st.title("🛡️ Real-Time Fraud Detection System")
st.markdown("### Live Demo - Credit Card Transaction Analysis")

# API endpoint
API_URL = "https://fraud-detection-api-v5cc.onrender.com"

# Create columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Enter Transaction Details")
    amount = st.number_input("Transaction Amount ($)", min_value=0.01, value=149.62, step=0.01)
    
    # Simple preset scenarios
    st.markdown("#### Quick Test Scenarios")
    if st.button("💳 Normal Transaction ()"):
        amount = 50.0
    if st.button("⚠️ Suspicious Transaction ()"):
        amount = 2500.0
    if st.button("🚨 High Risk Transaction ()"):
        amount = 10000.0

with col2:
    st.markdown("#### Model Performance")
    st.metric("Accuracy", "99.95%")
    st.metric("F1-Score", "88.61%")
    st.info("💡 First prediction may take 30s (API waking up)")

# Prediction button
if st.button("🔍 Analyze Transaction", type="primary", use_container_width=True):
    # Create transaction data
    transaction_data = {
        "Time": 0.0,
        "Amount": float(amount),
        **{f"V{i}": 0.0 for i in range(1, 29)}
    }
    
    with st.spinner("Analyzing transaction..."):
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=transaction_data,
                timeout=40
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                if result['prediction'] == 0:
                    st.success(f"✅ **LEGITIMATE TRANSACTION**")
                    st.balloons()
                else:
                    st.error(f"🚨 **FRAUD DETECTED!**")
                
                # Show details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Risk Level", result['risk_level'])
                with col2:
                    st.metric("Fraud Probability", f"{result['probability']:.1%}")
                with col3:
                    st.metric("Amount", f"")
                
                # Details expander
                with st.expander("View Full Response"):
                    st.json(result)
                    
            else:
                st.error(f"API Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.warning("⏱️ The API is starting up. Please wait 30 seconds and try again.")
            st.info("This happens when the free server needs to wake up.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
**Links:** 
[📚 API Documentation](https://fraud-detection-api-v5cc.onrender.com/docs) | 
[💻 GitHub](https://github.com/MrKunalSharma/fraud-detection-mlops) | 
[👤 LinkedIn](https://www.linkedin.com/in/kunal-sharma-1a8457257/)
""")
