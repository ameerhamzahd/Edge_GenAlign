from setuptools import setup, find_packages

setup(
    name="GenAlign",                      # Project name
    version="1.0.0",                      # Version number
    packages=find_packages(),             # Automatically include all packages
    include_package_data=True,            # Include static/templates files
    install_requires=[                    # List of dependencies
        "flask"
    ],
    description="DNA Sequence Alignment Tool",      # Short description
    author="Ameer Hamzah Daiyan",                   # Your name
    author_email="ameerhamzah.daiyan@gmail.com",# Your email
    url="https://github.com/ameerhamzahd/Edge_GenAlign.git",    # URL of your project/repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',              # Minimum Python version
)
