"""
Configuration settings for the Fact-Checker Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Search Configuration
MAX_SEARCH_RESULTS = 6
SEARCH_TIMEOUT = 10

# Model Configuration
NLI_MODEL_NAME = "cross-encoder/nli-deberta-v3-base"
CONFIDENCE_THRESHOLD = 0.5

# Text Generation Configuration
MAX_POST_LENGTH = 600
TEMPERATURE = 0.3

# Verdict thresholds
MIN_SUPPORTS_FOR_TRUE = 2
MIN_REFUTES_FOR_FALSE = 2
MIN_MIXED_FOR_MISLEADING = 1

# UI Configuration
STREAMLIT_CONFIG = {
    "page_title": "AI Fact-Checker",
    "page_icon": "🔍",
    "layout": "wide"
}

# Sample test claims for demo - optimized for accuracy testing
SAMPLE_CLAIMS = [
    "Water boils at 100°C at sea level.",
    "Jupiter is the largest planet in our Solar System.",
    "Vaccines cause autism in children.",
    "Humans have 48 chromosomes.",
    "The Great Wall of China is visible from space.",
    "Lightning never strikes the same place twice."
]
