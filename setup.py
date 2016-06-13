try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Platofrm for minimalist simulation of dynamic transportation systems in a city. Network, drivers and clients are modelled in the simplest way in order to draw mathematical properties inherent to the matching system functionment.',
    'author': 'Alexis Pibrac',
    'url': 'None',
    'download_url': 'None',
    'author_email': 'alexis.pibrac@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['CircleNet'],
    'scripts': [],
    'name': 'CircleNet'
}

setup(**config)