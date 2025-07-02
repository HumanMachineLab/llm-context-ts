#!/usr/bin/env python3
"""
Example script demonstrating LLM-based text segmentation.

This script shows how to use the Determinor class to segment text
into topics using different LLM models.
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from determinor import Determinor

def main():
    """Run example text segmentation."""
    
    print("🚀 LLM-Based Text Segmentation Example")
    print("=" * 50)
    
    # Example text with multiple topics
    example_sentences = [
        "Climate change is one of the most pressing issues of our time.",
        "Rising global temperatures affect weather patterns worldwide.", 
        "Scientists agree that human activities are the primary cause.",
        "Machine learning has revolutionized many industries.",
        "Neural networks can now process complex patterns in data.",
        "Deep learning models require substantial computational resources.",
        "The stock market experienced significant volatility yesterday.",
        "Many investors are concerned about inflation rates.",
        "Economic indicators suggest a potential recession ahead."
    ]
    
    print(f"📝 Input text ({len(example_sentences)} sentences):")
    for i, sentence in enumerate(example_sentences, 1):
        print(f"  {i}. {sentence}")
    
    print("\n🤖 Running segmentation with Mistral (local)...")
    
    try:
        # Initialize determinor with default settings (Mistral via Ollama)
        determinor = Determinor()
        
        # Get segmentation predictions
        print("\nSegmentation progress: ", end="")
        predictions = determinor.query_batch_data(example_sentences)
        
        print(f"\n\n📊 Results:")
        print("Sentence | Topic Boundary | Text")
        print("-" * 80)
        
        for i, (sentence, is_boundary) in enumerate(zip(example_sentences, [True] + predictions), 1):
            boundary_marker = "🔴 NEW TOPIC" if is_boundary else "🔵 SAME TOPIC"
            print(f"{i:2d}       | {boundary_marker:12s} | {sentence}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Installed Ollama: https://ollama.ai/")
        print("   2. Pulled the Mistral model: ollama pull mistral")
        print("   3. Installed dependencies: pip install -r requirements.txt")
        return
    
    print(f"\n✅ Segmentation complete!")
    print("\n🔧 To try different models:")
    print("   - GPT-4o: Determinor(openai_4o=True)")
    print("   - DeepSeek: Determinor(deepseek=True)")
    print("   - o1-mini: Determinor(openai_o1=True)")
    
    print("\n📚 For more examples, check out the Jupyter notebooks in notebooks/")

if __name__ == "__main__":
    main() 