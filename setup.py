from setuptools import setup, find_packages

setup(
    name="study-ai-agent",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.0",
        "click==8.1.7",
        "requests==2.31.0",
        "rich==13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "study=src.cli:cli",
        ],
    },
)
