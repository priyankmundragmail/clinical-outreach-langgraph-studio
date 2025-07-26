from setuptools import setup, find_packages

setup(
    name="clinical-outreach-agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain>=0.1.0",
        "langgraph>=0.1.0", 
        "langchain-openai>=0.1.0",
        "langchain-core>=0.1.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.0.0",
        "rich>=13.0.0"
    ]
)