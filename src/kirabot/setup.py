from setuptools import setup

setup(
    name='kirabot',
    version='1.0',
    install_requires=[
        'Skype4Py',
        'ujson',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'run-kirabot = kirabot.scripts:run'
        ]
    }
)
