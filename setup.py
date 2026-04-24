from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zapprobe",
    version="0.3.0",
    author="badyus",
    author_email="your.email@example.com",
    description="Educational web vulnerability scanner for SQL Injection and XSS detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/zapprobe",
    packages=find_packages(),
    # scanner.py ve cli_runner.py top-level modules
    py_modules=["scanner", "cli_runner"],
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
        "urllib3>=2.0.7",
    ],
    extras_require={
        'gui': ['PySimpleGUI>=4.60.0'],
    },
    entry_points={
        "console_scripts": [
            "zapprobe=cli_runner:main",
        ],
    },
)

