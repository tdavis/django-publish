import sys, os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS')).read()

version = '1.0.3'

install_requires = [
    'docutils==0.7',
    'argparse',
]

setup(name='django-publish',
    version=version,
    description="cli publishing of blog articles to a django-articles blog.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Topic :: Text Processing :: Markup'
    ],
    keywords='django django-articles reST publish blog',
    author='Tom Davis',
    author_email='tom@recursivedream.com',
    url='http://docs.recursivedream.com/django-publish/',
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

