from setuptools import setup

setup(
    name="checkmate",
    version="1.0",
    py_modules=["main"],
    entry_points={
        'console_scripts': [
            'checkmate=main:main',
        ],
    },
    install_requires=[
        "flask",
        "httpx"
    ],
)
