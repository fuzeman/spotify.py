from spotify import __version__

from setuptools import setup, find_packages
import os

# Read requirements (for the 'install_requires' parameter)
base_path = os.path.dirname(os.path.abspath(__file__))
requirements = open(os.path.join(base_path, 'requirements.txt'))

setup(
    name='spotify.py',
    version=__version__,
    url='https://github.com/fuzeman/spotify.py',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='Python library to communicate with the Spotify WebSocket API',
    packages=find_packages(exclude=['tests', 'tests.*']),
    platforms='any',

    install_requires=[r.strip() for r in requirements.readlines()],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
