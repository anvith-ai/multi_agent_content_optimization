import openai
from typing import Optional

class ContentGeneratorAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
    def generate_content(
        self, 
        prompt: str, 
        context: str = "", 
        previous_feedback: str = ""
    ) -> str:
        """Generate content based on prompt, context, and previous feedback."""
        
        system_message = """You are a content creation agent. Your task is to generate 
        high-quality content based on the given prompt. If provided, incorporate the feedback 
        from previous iterations to improve the content."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"""
            Prompt: {prompt}
            Context: {context}
            Previous Feedback: {previous_feedback}
            
            Please generate appropriate content based on the above information.
            """}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""