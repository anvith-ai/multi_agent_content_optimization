# Multi-Agent Content Optimization System
A multi-agent system that generates and optimizes content using OpenAI's API. The system consists of a content generation agent and an evaluation agent that work together to produce high-quality content through an iterative improvement process.

## Project Structure
```
multi_agent_content_optimization/
├── README.md
├── requirements.txt
├── setup.py
├── .env
├── .gitignore
├── main.py
├── content_optimization/
   ├── __init__.py
   ├── agents/
   │   ├── __init__.py
   │   ├── generator.py
   │   └── evaluator.py
   ├── system/
   │   ├── __init__.py
   │   └── optimizer.py
   └── utils/
       ├── __init__.py
       └── config.py

```

## Installation & Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. update `.env` with your OpenAI API key
6. Run the example: `python main.py`

## Requirements
- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt

## License
MIT License