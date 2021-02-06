#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


# Hack to prevent "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when setup.py exits
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing  # NOQA
except ImportError:
    pass


install_requires = [
    "wagtail>=2.7,<2.13",
    "textract",
]

tests_require = [
    'pytest',
    'pytest-django',
    'coverage',
    'codecov',
]

setup(
    name='wagtail-textract',
    version='1.3.dev0',
    description='Allow searching for text in Documents in the Wagtail content management system',
    author='Kees Hink',
    author_email='kees@fourdigits.nl',
    url='https://github.com/fourdigits/wagtail_textract',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    license='BSD',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.1',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=install_requires,
    extras_require={
        'test': tests_require,
    },
    entry_points="""""",
    zip_safe=False,
    cmdclass={
    },
)
