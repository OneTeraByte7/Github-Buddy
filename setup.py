# setup.py

from setuptools import setup, find_packages

setup(
    name="github-buddy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "GitPython",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'gibu=github_buddy.main:main',
            'github-buddy=github_buddy.main:main'
        ]
    }

)
