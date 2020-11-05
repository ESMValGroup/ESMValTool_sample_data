import os

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='ESMValTool sample data',
    version='0.0.1',
    description="ESMValTool sample data",
    long_description=readme + '\n\n',
    author="",
    author_email='',
    url='https://github.com/ESMValGroup/ESMValTool_sample_data',
    packages=[
        'esmvaltool_sample_data',
    ],
    include_package_data=True,
    license="",
    zip_safe=False,
    keywords='ESMValTool',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    install_requires=[
        'scitools-iris>=2.2',
    ],
    # tests_require=[
    #     'pytest',
    #     'pytest-cov',
    #     'pycodestyle',
    # ],
    extras_require={
        'develop': [
            'codespell',
            'docformatter',
            'isort',
            'pre-commit',
            'prospector[with_pyroma]!=1.1.6.3,!=1.1.6.4',
            'yamllint',
            'yapf',
        ],
    },
)
