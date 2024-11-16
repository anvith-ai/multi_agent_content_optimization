# main.py
from content_optimization.utils.config import Config
from content_optimization.system.optimizer import ContentOptimizationSystem

def main():
    # Validate configuration
    Config.validate()
    
    # Initialize the system
    system = ContentOptimizationSystem(
        api_key=Config.OPENAI_API_KEY,
        passing_grade=Config.PASSING_GRADE,
        max_iterations=Config.MAX_ITERATIONS
    )
    
    # Define evaluation criteria
    criteria = {
        "Clarity": 0.3,
        "Accuracy": 0.3,
        "Relevance": 0.2,
        "Engagement": 0.2
    }
    
    # Example prompt
    prompt = """Write a brief explanation of machine learning for beginners."""
    
    # Run the optimization process
    final_content, final_grade, final_feedback, iterations = system.optimize_content(
        prompt=prompt,
        criteria=criteria
    )
    
    print("\n=== Final Optimized Content ===")
    print(final_content)

if __name__ == "__main__":
    main()