import openai
from typing import Dict, Tuple

class ContentEvaluatorAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
    def evaluate_content(self, content: str, criteria: Dict[str, float]) -> Tuple[float, str]:
        """
        Evaluate content based on given criteria and return a grade and feedback.
        
        Args:
            content: The content to evaluate
            criteria: Dictionary of criteria and their weights (should sum to 1.0)
        
        Returns:
            Tuple of (grade, feedback)
        """
        
        system_message = """You are a content evaluation agent. Your task is to evaluate 
        the given content based on specified criteria. Provide a detailed analysis and 
        constructive feedback."""
        
        criteria_str = "\n".join([f"- {k} (Weight: {v})" for k, v in criteria.items()])
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"""
            Content to evaluate:
            {content}
            
            Evaluation Criteria:
            {criteria_str}
            
            Please provide:
            1. A score (0-100) for each criterion
            2. Detailed feedback for improvement
            3. Overall grade (0-100)
            """}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            
            evaluation = response.choices[0].message.content
            
            # Parse the grade and feedback
            lines = evaluation.split('\n')
            grade = 0
            feedback = evaluation
            
            for line in lines:
                if "Overall grade:" in line.lower():
                    try:
                        grade = float(line.split(':')[1].strip().split('/')[0])
                    except:
                        grade = 0
            
            return grade, feedback
            
        except Exception as e:
            print(f"Error evaluating content: {e}")
            return 0, "Error during evaluation"