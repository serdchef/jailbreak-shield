"""
setup.py

Package configuration for pip installation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jailbreak-shield",
    version="0.1.0",
    author="Ali Serdar Çarlı",
    author_email="a.serdcarl@gmail.com",
    description="Open-source prompt injection defense for Claude AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serdchef/jailbreak-shield",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.39.0",
        "pandas>=2.1.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "demo": [
            "streamlit>=1.29.0",
            "plotly>=5.18.0",
        ],
    },
)
