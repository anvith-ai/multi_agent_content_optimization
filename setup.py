from setuptools import setup, find_packages

setup(
    name="content_optimization",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "pytest>=7.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A multi-agent system for content generation and optimization",
    keywords="ai, content, optimization, openai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
)