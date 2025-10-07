from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zapprobe",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Educational web vulnerability scanner for SQL Injection and XSS detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/simple-security-scanner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
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
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "zapprobe=scanner:main",
        ],
    },
)