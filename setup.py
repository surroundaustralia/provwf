from setuptools import setup, find_packages
from os import path
from io import open
from provworkflow import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='provworkflow',
    version=__version__,
    install_requires=['gitpython'],
    description='A Python library for creating Workflows containing Blocks that log their actions according to a '
                'specialisation of the PROV-O standard.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SURROUND',  # Optional
    author_email='info@surroundaustralia.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        # 'License :: OSI Approved :: MIT License', -- not licensed

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='workflow provenance semantic',
    packages=find_packages(),
    python_requires='>=3.7',
    project_urls={  # Optional
        'Source': 'https://bitbucket.org/surroundbitbucket/provworkflow/src/master/',
    }
)
