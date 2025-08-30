"""
Standalone Demo - Works without any external dependencies
Perfect for hackathon presentation when dependencies fail
"""

import json
import time
import random
from datetime import datetime

# Mock data for reliable demo
DEMO_DATA = {
    "great wall china visible space": {
        "verdict": "False",
        "confidence": 0.87,
        "sources": [
            {
                "title": "NASA Debunks Great Wall Space Visibility Myth",
                "snippet": "NASA scientists confirm that the Great Wall of China cannot be seen from space with the naked eye. The myth persists despite repeated scientific corrections.",
                "link": "https://www.nasa.gov/space/great-wall-myth",
                "label": "refutes",
                "confidence": 0.92
            },
            {
                "title": "Snopes: Can You See the Great Wall From Space?",
                "snippet": "The Great Wall is not visible from space without aid. This common myth has been debunked by astronauts and space agencies worldwide.",
                "link": "https://www.snopes.com/fact-check/great-wall-space",
                "label": "refutes", 
                "confidence": 0.89
            },
            {
                "title": "Space.com: What's Actually Visible From Space",
                "snippet": "While city lights and large geographical features are visible from space, the Great Wall's width is insufficient for naked-eye visibility from orbit.",
                "link": "https://www.space.com/visible-from-space",
                "label": "refutes",
                "confidence": 0.84
            }
        ]
    },
    "water boils 100 degrees celsius": {
        "verdict": "True", 
        "confidence": 0.95,
        "sources": [
            {
                "title": "Britannica: Boiling Point of Water",
                "snippet": "Water boils at 100 degrees Celsius (212°F) at standard atmospheric pressure. This is a fundamental reference point in science.",
                "link": "https://www.britannica.com/science/boiling-point",
                "label": "supports",
                "confidence": 0.96
            },
            {
                "title": "USGS: Water Properties and Facts",
                "snippet": "At sea level, pure water reaches its boiling point at exactly 100°C. This well-established scientific fact is used worldwide.",
                "link": "https://www.usgs.gov/water-science/water-properties",
                "label": "supports",
                "confidence": 0.95
            },
            {
                "title": "Chemistry LibreTexts: Phase Changes",
                "snippet": "The boiling point of water at standard pressure is 100 degrees Celsius, a constant used in temperature calibration.",
                "link": "https://chem.libretexts.org/water-boiling",
                "label": "supports",
                "confidence": 0.94
            }
        ]
    },
    "lightning never strikes same place twice": {
        "verdict": "False",
        "confidence": 0.82,
        "sources": [
            {
                "title": "National Weather Service: Lightning Myths",
                "snippet": "Lightning can and does strike the same place multiple times. The Empire State Building is struck about 25 times per year.",
                "link": "https://www.weather.gov/safety/lightning-myths",
                "label": "refutes",
                "confidence": 0.88
            },
            {
                "title": "NOAA: Lightning Safety Facts",
                "snippet": "Contrary to popular belief, lightning frequently strikes the same location. Tall structures are repeatedly struck during storms.",
                "link": "https://www.weather.gov/lightning-facts",
                "label": "refutes",
                "confidence": 0.85
            }
        ]
    },
    "earth is flat": {
        "verdict": "False",
        "confidence": 0.99,
        "sources": [
            {
                "title": "NASA: Earth's Shape and Size",
                "snippet": "Overwhelming scientific evidence from satellite imagery, physics, and space observation confirms Earth is spherical.",
                "link": "https://www.nasa.gov/earth-shape",
                "label": "refutes",
                "confidence": 0.99
            },
            {
                "title": "Scientific American: Debunking Flat Earth",
                "snippet": "Modern science and ancient observations demonstrate Earth's spherical nature. Flat Earth claims contradict physics.",
                "link": "https://www.scientificamerican.com/earth-sphere",
                "label": "refutes",
                "confidence": 0.98
            }
        ]
    }
}

def find_matching_data(claim):
    """Find the best matching demo data for a claim."""
    claim_lower = claim.lower()
    
    best_match = None
    best_score = 0
    
    for key, data in DEMO_DATA.items():
        keywords = key.split()
        score = sum(1 for keyword in keywords if keyword in claim_lower)
        if score > best_score:
            best_score = score
            best_match = data
    
    return best_match if best_score > 0 else None

def generate_social_post(claim, verdict, confidence, sources):
    """Generate a social media post."""
    verdict_emojis = {
        "True": "✅",
        "False": "❌",
        "Misleading": "⚠️", 
        "Unverified": "❓"
    }
    
    emoji = verdict_emojis.get(verdict, "🔍")
    citation = sources[0]["link"] if sources else "Multiple sources"
    
    if verdict == "True":
        post = f"{emoji} VERIFIED: {verdict} ({confidence:.0%} confidence)\n\nClaim: \"{claim[:80]}{'...' if len(claim) > 80 else ''}\"\n\nEvidence confirms this is accurate.\nSource: {citation}"
    elif verdict == "False":
        post = f"{emoji} DEBUNKED: {verdict} ({confidence:.0%} confidence)\n\nClaim: \"{claim[:80]}{'...' if len(claim) > 80 else ''}\"\n\nEvidence shows this is false.\nSource: {citation}"
    else:
        post = f"{emoji} {verdict.upper()}: {verdict} ({confidence:.0%} confidence)\n\nClaim: \"{claim[:80]}{'...' if len(claim) > 80 else ''}\"\n\nEvidence is mixed or unclear.\nSource: {citation}"
    
    post += "\n\n[Demo Mode]\n#FactCheck #AI"
    
    return post[:600]

def fact_check_claim(claim):
    """Process a claim and return results."""
    print(f"\n{'='*60}")
    print(f"🔍 AI FACT-CHECKER DEMO")
    print(f"{'='*60}")
    print(f"Claim: {claim}")
    print(f"{'='*60}")
    
    # Simulate processing time
    print("🔍 Searching for sources...")
    time.sleep(1)
    print("🧠 Analyzing evidence...")
    time.sleep(1)
    print("📝 Generating verdict...")
    time.sleep(0.5)
    
    # Get demo data
    data = find_matching_data(claim)
    
    if data:
        verdict = data["verdict"]
        confidence = data["confidence"]
        sources = data["sources"]
        reasoning = f"Based on {len(sources)} sources: analysis shows consistent {verdict.lower()} evidence"
    else:
        # Generic response for unknown claims
        verdict = "Unverified"
        confidence = 0.50
        sources = [{
            "title": f"General Search Result for: {claim[:50]}...",
            "snippet": "Insufficient specific information found to make a determination about this claim.",
            "link": "https://example.com/general-search",
            "label": "unclear",
            "confidence": 0.50
        }]
        reasoning = "Insufficient evidence found for this specific claim"
    
    # Generate social post
    social_post = generate_social_post(claim, verdict, confidence, sources)
    
    # Display results
    print(f"\n📊 ANALYSIS COMPLETE")
    print(f"   Verdict: {verdict}")
    print(f"   Confidence: {confidence:.0%}")
    print(f"   Reasoning: {reasoning}")
    print(f"   Sources Analyzed: {len(sources)}")
    
    print(f"\n📚 SOURCE BREAKDOWN:")
    for i, source in enumerate(sources):
        label = source["label"].upper()
        conf = source["confidence"]
        print(f"   {i+1}. {label} ({conf:.2f}) - {source['title']}")
        print(f"      Content: {source['snippet'][:80]}...")
        print(f"      URL: {source['link']}")
        print()
    
    print(f"📱 SOCIAL MEDIA POST:")
    print("─" * 50)
    print(social_post)
    print("─" * 50)
    print(f"Characters: {len(social_post)}/600")
    
    return {
        "claim": claim,
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "sources": sources,
        "social_post": social_post
    }

def interactive_demo():
    """Run interactive demo."""
    print("🤖 AI FACT-CHECKER AGENT - STANDALONE DEMO")
    print("=" * 60)
    print("This demo works without any external dependencies!")
    print("Perfect for hackathon presentations.")
    print("=" * 60)
    
    sample_claims = [
        "The Great Wall of China is visible from space",
        "Water boils at 100 degrees Celsius at sea level",
        "Lightning never strikes the same place twice",
        "The Earth is flat"
    ]
    
    while True:
        print(f"\n📋 Choose an option:")
        print("1. 🧪 Test Sample Claims")
        print("2. 🔍 Enter Custom Claim")
        print("3. 🎬 Quick Demo (all samples)")
        print("4. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print(f"\n🎯 Sample Claims:")
            for i, claim in enumerate(sample_claims):
                print(f"   {i+1}. {claim}")
            
            try:
                selection = int(input(f"\nChoose a claim (1-{len(sample_claims)}): ")) - 1
                if 0 <= selection < len(sample_claims):
                    fact_check_claim(sample_claims[selection])
                else:
                    print("❌ Invalid selection.")
            except ValueError:
                print("❌ Please enter a valid number.")
                
        elif choice == "2":
            custom_claim = input("\n🔍 Enter your claim: ").strip()
            if custom_claim:
                fact_check_claim(custom_claim)
            else:
                print("❌ Please enter a valid claim.")
                
        elif choice == "3":
            print(f"\n🎬 QUICK DEMO - Testing all sample claims")
            for i, claim in enumerate(sample_claims):
                print(f"\n🧪 Demo {i+1}/{len(sample_claims)}")
                fact_check_claim(claim)
                if i < len(sample_claims) - 1:
                    input("\nPress Enter to continue...")
            
            print(f"\n✅ Quick demo completed!")
            
        elif choice == "4":
            print("👋 Thank you for trying the AI Fact-Checker!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main function."""
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print(f"\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 This demonstrates error handling in the system!")

if __name__ == "__main__":
    main()
