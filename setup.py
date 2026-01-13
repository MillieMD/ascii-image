from setuptools import setup

setup(
    name = 'ascii-image',
    version = '0.1.0',
    packages = ['asciiimage'],
    entry_points = {
        'console_scripts': [
            'ascii-image = asciiimage.__main__:main'
        ]
    })