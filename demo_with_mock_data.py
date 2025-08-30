"""
Demo version with mock data for testing when APIs are unavailable
"""

import json
import time
from typing import List, Dict

# Mock search results for testing
MOCK_SEARCH_RESULTS = {
    "great wall china visible space": [
        {
            "title": "Can You See the Great Wall of China From Space? | Snopes.com",
            "snippet": "The Great Wall of China is not visible from space with the naked eye. This is a common myth that has been debunked by astronauts and scientists. The wall is too narrow to be seen from orbital altitudes without aid.",
            "link": "https://www.snopes.com/fact-check/great-wall-of-china-from-space/"
        },
        {
            "title": "Great Wall of China visibility from space - NASA",
            "snippet": "NASA confirms that the Great Wall of China is not visible from space with the naked eye. Astronauts need telescopic lenses to see human-made structures. This myth has been repeatedly debunked.",
            "link": "https://www.nasa.gov/feature/goddard/2019/great-wall-china-space"
        },
        {
            "title": "Myths About the Great Wall - History Channel",
            "snippet": "The claim that the Great Wall is the only human-made object visible from space is false. The wall's narrow width makes it impossible to see without magnification from orbital distances.",
            "link": "https://www.history.com/topics/ancient-china/great-wall-of-china"
        }
    ],
    "water boils 100 degrees celsius": [
        {
            "title": "Boiling Point of Water - Chemistry Encyclopedia",
            "snippet": "Water boils at 100 degrees Celsius (212 degrees Fahrenheit) at standard atmospheric pressure (1 atmosphere). This is a fundamental property of water used as a reference point.",
            "link": "https://www.britannica.com/science/boiling-point"
        },
        {
            "title": "Why Does Water Boil at 100°C? - Science Explained",
            "snippet": "At sea level and standard pressure, water reaches its boiling point at exactly 100°C. This temperature is constant and well-established in scientific literature.",
            "link": "https://www.thoughtco.com/why-water-boils-at-100-degrees-celsius-607470"
        },
        {
            "title": "Water Properties - USGS Water Science School",
            "snippet": "The boiling point of pure water at standard atmospheric pressure is 100 degrees Celsius or 212 degrees Fahrenheit. This is a reliable scientific fact.",
            "link": "https://www.usgs.gov/special-topics/water-science-school/science/water-properties"
        }
    ]
}

def mock_search_claim(claim: str, max_results: int = 6) -> List[Dict]:
    """Mock search function that returns predefined results."""
    print(f"🔍 Searching for: {claim}")
    
    # Simple keyword matching for demo
    claim_lower = claim.lower()
    
    if "great wall" in claim_lower and "space" in claim_lower:
        results = MOCK_SEARCH_RESULTS["great wall china visible space"]
    elif "water" in claim_lower and "100" in claim_lower:
        results = MOCK_SEARCH_RESULTS["water boils 100 degrees celsius"]
    else:
        # Generic results for other claims
        results = [
            {
                "title": f"Search result for: {claim}",
                "snippet": f"This is a mock search result for the claim '{claim}'. In a real implementation, this would contain actual web content.",
                "link": "https://example.com/mock-result"
            }
        ]
    
    print(f"✅ Found {len(results)} mock results")
    return results[:max_results]

def mock_gemini_analysis(claim: str, sources: List[Dict]) -> Dict:
    """Mock Gemini analysis that provides realistic responses."""
    print(f"🧠 Analyzing with mock AI: {claim}")
    
    # Simulate AI analysis based on content
    claim_lower = claim.lower()
    
    if "great wall" in claim_lower and "space" in claim_lower:
        # This claim is typically false
        analysis = {
            "source_1": {"label": "REFUTES", "confidence": 0.9, "reasoning": "Explicitly states the myth is debunked"},
            "source_2": {"label": "REFUTES", "confidence": 0.95, "reasoning": "NASA confirmation that it's not visible"},
            "source_3": {"label": "REFUTES", "confidence": 0.85, "reasoning": "Historical source confirms it's false"}
        }
    elif "water" in claim_lower and "100" in claim_lower:
        # This claim is typically true
        analysis = {
            "source_1": {"label": "SUPPORTS", "confidence": 0.95, "reasoning": "Scientific encyclopedia confirms the fact"},
            "source_2": {"label": "SUPPORTS", "confidence": 0.9, "reasoning": "Educational source explains the science"},
            "source_3": {"label": "SUPPORTS", "confidence": 0.95, "reasoning": "USGS official data confirms"}
        }
    else:
        # Generic uncertain analysis
        analysis = {
            "source_1": {"label": "UNCLEAR", "confidence": 0.6, "reasoning": "Insufficient information to determine"}
        }
    
    return analysis

def mock_fact_checker_pipeline(claim: str) -> Dict:
    """Complete mock pipeline for demonstration."""
    start_time = time.time()
    
    print(f"\n{'='*60}")
    print(f"🤖 MOCK FACT-CHECKER PIPELINE")
    print(f"{'='*60}")
    print(f"Claim: {claim}")
    print(f"{'='*60}")
    
    # Step 1: Search
    sources = mock_search_claim(claim)
    
    # Step 2: AI Analysis
    if sources:
        analysis = mock_gemini_analysis(claim, sources)
        
        # Update sources with analysis
        for i, source in enumerate(sources):
            source_key = f"source_{i+1}"
            if source_key in analysis:
                source.update(analysis[source_key])
            else:
                source.update({
                    "label": "unclear",
                    "confidence": 0.5,
                    "reasoning": "No analysis available"
                })
    
    # Step 3: Aggregate verdict
    supports = sum(1 for s in sources if s.get("label", "").lower() == "supports")
    refutes = sum(1 for s in sources if s.get("label", "").lower() == "refutes")
    unclear = len(sources) - supports - refutes
    
    if supports >= 2 and refutes == 0:
        verdict = "True"
        confidence = 0.85 + (supports / len(sources)) * 0.1
    elif refutes >= 2 and supports == 0:
        verdict = "False"  
        confidence = 0.85 + (refutes / len(sources)) * 0.1
    elif supports >= 1 and refutes >= 1:
        verdict = "Misleading"
        confidence = 0.70
    else:
        verdict = "Unverified"
        confidence = 0.50
    
    reasoning = f"Based on {len(sources)} sources: {supports} support, {refutes} refute, {unclear} unclear"
    
    # Step 4: Generate social post
    citation = sources[0]["link"] if sources else "Multiple sources"
    
    social_post = (
        f"🔍 FACT-CHECK: {verdict} ({confidence:.0%} confidence)\n\n"
        f"Claim: \"{claim[:100]}{'...' if len(claim) > 100 else ''}\"\n\n"
        f"Analysis: {reasoning}\n"
        f"Source: {citation}\n\n"
        "#FactCheck #AI #Verification"
    )
    
    if len(social_post) > 600:
        social_post = social_post[:597] + "..."
    
    processing_time = time.time() - start_time
    
    # Display results
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   Verdict: {verdict}")
    print(f"   Confidence: {confidence:.1%}")
    print(f"   Reasoning: {reasoning}")
    print(f"   Processing Time: {processing_time:.2f}s")
    
    print(f"\n📚 SOURCE BREAKDOWN:")
    for i, source in enumerate(sources):
        label = source.get("label", "unclear").upper()
        conf = source.get("confidence", 0.5)
        print(f"   {i+1}. {label} ({conf:.2f}) - {source['title']}")
        print(f"      Reasoning: {source.get('reasoning', 'N/A')}")
    
    print(f"\n📱 SOCIAL MEDIA POST:")
    print("-" * 50)
    print(social_post)
    print("-" * 50)
    print(f"Characters: {len(social_post)}/600")
    
    return {
        "claim": claim,
        "sources": sources,
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "social_post": social_post,
        "processing_time": processing_time
    }

def demo_test_cases():
    """Run demo with predefined test cases."""
    test_claims = [
        "The Great Wall of China is visible from space with the naked eye",
        "Water boils at 100 degrees Celsius at sea level",
        "Lightning never strikes the same place twice"
    ]
    
    print("🎬 FACT-CHECKER DEMO - Mock Data Version")
    print("=" * 70)
    print("This demo uses mock data to showcase the pipeline functionality")
    print("when external APIs are unavailable or rate-limited.")
    print("=" * 70)
    
    results = []
    
    for i, claim in enumerate(test_claims):
        print(f"\n🧪 TEST CASE {i+1}/{len(test_claims)}")
        result = mock_fact_checker_pipeline(claim)
        results.append(result)
        
        if i < len(test_claims) - 1:
            input("\nPress Enter to continue to next test case...")
    
    # Summary
    print(f"\n{'='*70}")
    print("📈 DEMO SUMMARY")
    print('='*70)
    
    total_time = sum(r["processing_time"] for r in results)
    print(f"Total Tests: {len(results)}")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Average Time: {total_time/len(results):.2f}s per claim")
    
    verdict_counts = {}
    for result in results:
        verdict = result["verdict"]
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
    
    print(f"\nVerdict Distribution:")
    for verdict, count in verdict_counts.items():
        print(f"   {verdict}: {count}")
    
    print(f"\n✅ Demo completed successfully!")
    print("💡 This demonstrates the full pipeline workflow.")
    print("🔗 In production, replace mock functions with real API calls.")

if __name__ == "__main__":
    demo_test_cases()