from setuptools import setup, find_packages

setup(
    name="campus-placement-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.17.0",
        "altair>=5.2.0",
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
)
