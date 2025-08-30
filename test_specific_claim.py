"""
Test specific claims to verify pipeline accuracy
"""

from fact_checker_simple import FactCheckerPipeline

def test_specific_claims():
    pipeline = FactCheckerPipeline()
    
    test_claims = [
        "Water boils at 100°C at sea level",
        "Jupiter is the largest planet in our Solar System",
        "Vaccines cause autism in children",
        "Humans have 48 chromosomes"
    ]
    
    for claim in test_claims:
        print(f"\n{'='*60}")
        print(f"Testing: {claim}")
        print('='*60)
        
        result = pipeline.process_claim(claim)
        
        print(f"Verdict: {result.verdict}")
        print(f"Confidence: {result.confidence:.1%}")
        print(f"Reasoning: {result.reasoning}")
        print(f"Sources: {len(result.sources)}")
        
        # Show source breakdown
        for i, source in enumerate(result.sources):
            print(f"  {i+1}. {source.label.upper()} ({source.confidence:.0%}) - {source.title}")

if __name__ == "__main__":
    test_specific_claims()