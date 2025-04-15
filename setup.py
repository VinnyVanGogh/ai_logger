from setuptools import setup, find_packages

setup(
    name="ai-logger",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run-example=ai_logger.src.example:cli',
        ],
    },
)