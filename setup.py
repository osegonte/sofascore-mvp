from setuptools import setup, find_packages

setup(
    name="sofascore_cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "httpx>=0.24.0",
        "tenacity>=8.2.0",
        "click>=8.1.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "matplotlib>=3.7.0",
    ],
    entry_points={
        "console_scripts": [
            "sofascore=cli.commands:cli",
        ],
    },
    python_requires=">=3.8",
)