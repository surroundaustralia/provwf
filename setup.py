from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='provworkflow',  # Required
    version='0.5',  # Required
    description='This is a Python library for creating workflows of methods that log their actions according '
                'to the PROV-O standard.',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    # url='https://github.com/pypa/sampleproject',  # Optional
    author='SURROUND',  # Optional
    author_email='info@surroundaustralia.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        # 'License :: OSI Approved :: MIT License', -- not licensed

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='workflow provenance semantic',  # Optional
    packages=find_packages(),  # Required
    python_requires='>=3.6',
    project_urls={  # Optional
        'Source': 'https://bitbucket.org/surroundbitbucket/provworkflow/src/master/',
    }
)
