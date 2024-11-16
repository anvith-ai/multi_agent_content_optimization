import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
    PASSING_GRADE = float(os.getenv('PASSING_GRADE', 80.0))
    MAX_ITERATIONS = int(os.getenv('MAX_ITERATIONS', 3))
    
    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")