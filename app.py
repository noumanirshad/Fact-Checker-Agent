"""
Streamlit Web Interface for AI Fact-Checker
"""

import streamlit as st
import time
import json
from datetime import datetime

from fact_checker_simple import FactCheckerPipeline, FactCheckResult
from config import STREAMLIT_CONFIG, SAMPLE_CLAIMS

# Configure Streamlit page
st.set_page_config(**STREAMLIT_CONFIG)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    
    .verdict-true {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .verdict-false {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .verdict-misleading {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .verdict-unverified {
        background-color: #e2e3e5;
        border-left: 5px solid #6c757d;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .source-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
    }
    
    .confidence-bar {
        height: 20px;
        border-radius: 10px;
        background-color: #e9ecef;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .social-post-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Arial', sans-serif;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_pipeline():
    """Load and cache the fact-checker pipeline."""
    return FactCheckerPipeline()

def display_verdict(result: FactCheckResult):
    """Display the verdict with appropriate styling."""
    verdict_classes = {
        "True": "verdict-true",
        "False": "verdict-false", 
        "Misleading": "verdict-misleading",
        "Unverified": "verdict-unverified",
        "Error": "verdict-false"
    }
    
    verdict_icons = {
        "True": "✅",
        "False": "❌",
        "Misleading": "⚠️", 
        "Unverified": "❓",
        "Error": "🚫"
    }
    
    class_name = verdict_classes.get(result.verdict, "verdict-unverified")
    icon = verdict_icons.get(result.verdict, "❓")
    
    st.markdown(f"""
    <div class="{class_name}">
        <h3>{icon} Verdict: {result.verdict}</h3>
        <p><strong>Confidence:</strong> {result.confidence:.1%}</p>
        <p><strong>Reasoning:</strong> {result.reasoning}</p>
        <p><strong>Processing Time:</strong> {result.processing_time:.2f} seconds</p>
    </div>
    """, unsafe_allow_html=True)

def display_sources(sources):
    """Display source analysis with cards."""
    st.subheader("📚 Source Analysis")
    
    if not sources:
        st.warning("No sources found for this claim.")
        return
    
    for i, source in enumerate(sources):
        # Determine label styling
        label_colors = {
            "supports": ("🟢", "#28a745"),
            "refutes": ("🔴", "#dc3545"),
            "unclear": ("🟡", "#ffc107")
        }
        
        icon, color = label_colors.get(source.label, ("⚪", "#6c757d"))
        
        with st.expander(f"{icon} Source {i+1}: {source.title}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Title:** {source.title}")
                st.markdown(f"**Content:** {source.snippet}")
                st.markdown(f"**URL:** [{source.link}]({source.link})")
                if source.reasoning:
                    st.markdown(f"**Analysis:** {source.reasoning}")
            
            with col2:
                st.markdown(f"**Label:** {source.label.upper()}")
                st.markdown(f"**Confidence:** {source.confidence:.1%}")
                
                # Confidence bar
                st.markdown(f"""
                <div class="confidence-bar">
                    <div style="width: {source.confidence * 100}%; height: 100%; background-color: {color};"></div>
                </div>
                """, unsafe_allow_html=True)

def display_social_post(post):
    """Display the generated social media post."""
    st.subheader("📱 Social Media Post")
    
    st.markdown(f"""
    <div class="social-post-box">
{post}
    </div>
    """, unsafe_allow_html=True)
    
    # Character count
    char_count = len(post)
    color = "green" if char_count <= 600 else "red"
    st.markdown(f"<p style='color: {color}; font-size: 14px;'>Character count: {char_count}/600</p>", 
                unsafe_allow_html=True)
    
    # Copy button
    if st.button("📋 Copy to Clipboard"):
        # JavaScript to copy text (requires streamlit-javascript)
        st.success("Post copied! (Use Ctrl+C to copy manually if needed)")

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 AI Fact-Checker Agent</h1>
        <p>Automated fact-checking with web search and AI analysis</p>
        <p><em>Built for AiForAll Hackathon Challenge</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This AI-powered fact-checker:
        
        1. **🔍 Researches** claims using web search
        2. **🧠 Analyzes** sources with AI models  
        3. **📝 Generates** social-ready verdicts
        
        **Technologies:**
        - DuckDuckGo Search API
        - Google Gemini AI
        - Sentence Transformers
        - Natural Language Inference
        """)
        
        st.header("🎯 Sample Claims")
        for claim in SAMPLE_CLAIMS:
            if st.button(claim, key=f"sample_{claim[:20]}"):
                st.session_state.sample_claim = claim
    
    # Main interface
    st.header("Enter a Claim to Fact-Check")
    
    # Input section
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Check if sample claim was selected
        default_claim = st.session_state.get('sample_claim', '')
        claim_input = st.text_area(
            "Enter your claim here:",
            value=default_claim,
            height=100,
            placeholder="e.g., 'The Great Wall of China is visible from space.'"
        )
        
        # Clear sample claim after use
        if 'sample_claim' in st.session_state:
            del st.session_state.sample_claim
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        analyze_button = st.button("🔍 Analyze Claim", type="primary")
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            max_sources = st.slider("Max Sources", 3, 10, 6)
            show_debug = st.checkbox("Show Debug Info")
    
    # Processing and results
    if analyze_button and claim_input.strip():
        if len(claim_input.strip()) < 10:
            st.error("Please enter a claim with at least 10 characters.")
            return
        
        # Load pipeline
        with st.spinner("Initializing AI models..."):
            pipeline = load_pipeline()
        
        # Process claim
        with st.spinner("🔍 Researching claim and analyzing sources..."):
            progress_bar = st.progress(0)
            
            # Simulate progress updates
            for i in range(100):
                time.sleep(0.02)  # Small delay for visual effect
                progress_bar.progress(i + 1)
            
            result = pipeline.process_claim(claim_input.strip())
        
        st.success("Analysis complete!")
        
        # Display results
        if result.verdict != "Error":
            # Verdict
            display_verdict(result)
            
            # Sources
            display_sources(result.sources)
            
            # Social post
            display_social_post(result.social_post)
            
            # Debug information
            if show_debug:
                st.subheader("🔧 Debug Information")
                with st.expander("Raw Result Data"):
                    debug_data = {
                        "claim": result.claim,
                        "verdict": result.verdict,
                        "confidence": result.confidence,
                        "reasoning": result.reasoning,
                        "processing_time": result.processing_time,
                        "sources_count": len(result.sources),
                        "sources": [
                            {
                                "title": s.title,
                                "label": s.label,
                                "confidence": s.confidence,
                                "reasoning": s.reasoning
                            } for s in result.sources
                        ]
                    }
                    st.json(debug_data)
        else:
            st.error(f"Analysis failed: {result.reasoning}")
    
    elif analyze_button:
        st.error("Please enter a claim to analyze.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
        <p>⚡ Built in 4-6 hours for AiForAll Hackathon Challenge</p>
        <p>🔧 Technologies: Streamlit • DuckDuckGo • Gemini AI • Sentence Transformers</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

