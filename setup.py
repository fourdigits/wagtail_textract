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
    "wagtail>=2,<2.1",
    "textract",
]

tests_require = [
    'pytest',
    'pytest-django',
]

setup(
    name='wagtail-textract',
    version='0.1-alpha',
    description='Allow searching for text in Documents in the Wagtail content management system',
    author='Kees Hink',
    author_email='kees@fourdigits.nl',
    url='https://github.com/fourdigits/wagtail-textract',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    license='BSD',
    long_description=open('README.md', 'r').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
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
