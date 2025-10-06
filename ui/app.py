import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import json

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RadProgressor",
    page_icon="🫁",
    layout="wide"
)

st.title("🫁 RadProgressor - Radiology Progression Lite")

with st.sidebar:
    st.header("Upload Study")
    
    patient_id = st.text_input("Patient ID", value="DEMO001")
    study_date = st.date_input("Study Date", value=datetime.now())
    study_date_str = study_date.strftime("%Y-%m-%d")
    
    uploaded_file = st.file_uploader(
        "Upload Chest X-ray", 
        type=['png', 'jpg', 'jpeg', 'dcm'],
        help="Upload DICOM or PNG/JPG chest X-ray image"
    )
    
    report_text = st.text_area(
        "Radiology Report (Optional)",
        placeholder="Paste radiology report text here...",
        height=100
    )
    
    analyze_button = st.button("🔍 Analyze Study", type="primary")

if analyze_button and uploaded_file:
    with st.spinner("Analyzing study..."):
        try:
            files = {"image": uploaded_file}
            data = {
                "patient_id": patient_id,
                "study_date": study_date_str,
                "report": report_text
            }
            
            response = requests.post(f"{API_BASE_URL}/api/analyze", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                st.success("Analysis completed!")
                st.session_state['last_analysis'] = result
            else:
                st.error(f"Analysis failed: {response.text}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if 'last_analysis' in st.session_state:
    result = st.session_state['last_analysis']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔬 Computer Vision Results")
        
        cv_result = result['cv_result']
        labels_df = pd.DataFrame([
            {"Label": label, "Probability": f"{prob:.3f}"}
            for label, prob in cv_result['labels'].items()
        ])
        st.dataframe(labels_df, use_container_width=True)
        
        severity_score = cv_result['severity_score']
        st.metric("Severity Score", f"{severity_score:.3f}")
        
        fig = px.bar(
            x=list(cv_result['labels'].keys()),
            y=list(cv_result['labels'].values()),
            title="Label Probabilities"
        )
        fig.update_layout(xaxis_title="Labels", yaxis_title="Probability")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📝 NLP Analysis")
        
        nlp_result = result['nlp_result']
        
        change_color = {
            "improved": "🟢",
            "stable": "🟡", 
            "worsened": "🔴"
        }
        
        change = nlp_result['change']
        st.metric(
            "Change Status", 
            f"{change_color.get(change, '⚪')} {change.title()}"
        )
        
        if nlp_result['sections']['findings']:
            st.subheader("Extracted Findings")
            st.text(nlp_result['sections']['findings'])
        
        if nlp_result['sections']['impression']:
            st.subheader("Extracted Impression")
            st.text(nlp_result['sections']['impression'])

    st.subheader("📈 Progression Analysis")
    
    progression_result = result['progression_result']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Progression Score", f"{progression_result['progression_score']:.3f}")
    
    with col2:
        st.metric("Trend Direction", progression_result['trend_direction'].title())
    
    with col3:
        st.metric("Last Delta", f"{progression_result['last_delta']:.3f}")

    st.subheader("🤖 AI Summaries")
    
    genai_result = result['genai_result']
    
    tab1, tab2 = st.tabs(["Clinical Summary", "Patient Summary"])
    
    with tab1:
        st.text_area(
            "Clinical Summary",
            value=genai_result['clinician_summary'],
            height=150,
            disabled=True
        )
    
    with tab2:
        st.text_area(
            "Patient Summary", 
            value=genai_result['patient_summary'],
            height=150,
            disabled=True
        )

st.divider()

if st.button("📊 View Patient Timeline"):
    if patient_id:
        try:
            response = requests.get(f"{API_BASE_URL}/api/patient/{patient_id}/timeline")
            if response.status_code == 200:
                timeline_data = response.json()
                timeline = timeline_data['timeline']
                
                if timeline:
                    df = pd.DataFrame(timeline)
                    df['date'] = pd.to_datetime(df['date'])
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['progression_score'],
                        mode='lines+markers',
                        name='Progression Score',
                        line=dict(color='blue', width=3)
                    ))
                    
                    fig.update_layout(
                        title=f"Progression Timeline - Patient {patient_id}",
                        xaxis_title="Date",
                        yaxis_title="Progression Score",
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("Timeline Data")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No timeline data available for this patient.")
            else:
                st.error(f"Failed to fetch timeline: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()

st.markdown("""
**⚠️ Disclaimer:** This tool is for research and educational purposes only. 
It does not provide medical advice, diagnosis, or treatment recommendations. 
Always consult with qualified healthcare professionals for medical decisions.
""")
