from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

PACKAGES = [
    'esmvaltool_sample_data',
]

setup(
    name='ESMValTool sample data',
    version='0.0.1',
    description="ESMValTool sample data",
    long_description=readme + '\n\n',
    author="Stef Smeets, Bouwe Andela",
    url='https://github.com/ESMValGroup/ESMValTool_sample_data',
    packages=PACKAGES,
    include_package_data=True,
    license="Apache 2.0; CC BY-SA 4.0",
    zip_safe=False,
    keywords='ESMValTool',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'License :: Other/Proprietary License'
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Hydrology',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    test_suite='tests',
    install_requires=[
        'scitools-iris>=2.2',
    ],
    extras_require={
        'develop': [
            'codespell',
            'docformatter',
            'esgf-pyclient',
            'isort',
            'myproxyclient',
            'pre-commit',
            'prospector[with_pyroma]!=1.1.6.3,!=1.1.6.4',
            'yamllint',
            'yapf',
        ],
    },
)
