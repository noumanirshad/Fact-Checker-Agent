"""
Quick test to verify the fact-checker pipeline works
"""

from fact_checker_simple import FactCheckerPipeline

def test_pipeline():
    print("🧪 Testing Fact-Checker Pipeline")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = FactCheckerPipeline()
    
    # Test claim
    claim = "The Great Wall of China is visible from space"
    print(f"Testing claim: {claim}")
    
    # Process claim
    result = pipeline.process_claim(claim)
    
    # Display results
    print(f"\n📊 Results:")
    print(f"   Verdict: {result.verdict}")
    print(f"   Confidence: {result.confidence:.1%}")
    print(f"   Reasoning: {result.reasoning}")
    print(f"   Processing Time: {result.processing_time:.2f}s")
    print(f"   Sources: {len(result.sources)}")
    
    print(f"\n📱 Social Post:")
    print("-" * 40)
    print(result.social_post)
    print("-" * 40)
    
    print("\n✅ Pipeline test completed successfully!")

if __name__ == "__main__":
    test_pipeline()