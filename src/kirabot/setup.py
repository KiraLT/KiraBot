from setuptools import setup

setup(
    name='kirabot',
    version='1.0',
    install_requires=[
        'Skype4Py',
        'ujson',
        'requests',
        'requests-futures',
        'beautifulsoup4',
        'cleverbot'
    ],
    entry_points={
        'console_scripts': [
            'run-kirabot = kirabot.scripts:run'
        ]
    }
)
