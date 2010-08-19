from distribute_setup import use_setuptools
use_setuptools()

import sys, os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS')).read()


version = '0.1'

install_requires = [
    'docutils==0.7',
    'django-articles',
    'argparse',
    'django'
]


setup(name='django-publish',
    version=version,
    description="cli publishing of blog articles to a django-articles blog.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='django django-articles reST publish blog',
    author='Tom Davis',
    author_email='tom@recursivedream.com',
    url='http://recursivedream.com',
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['publish=publish:main']
    }
)
