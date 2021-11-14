from setuptools import setup

setup(
    name='xgb-pipeline',
    version='0.1',
    packages=[ ],
    url='',
    license='',
    author='aniftos',
    author_email='aniftos@google.com',
    description='',

    install_requires=[
        'xgboost==1.5.0',
        'scipy>=0.14',
        'pandas>=0.11.0',
        'numpy>=1.6.1',
        'kfp==1.8.9',
        'google-cloud-pipeline-components==0.2.0',
        'gcsfs', 'mock','coverage'],

    setup_requires=['nose>=1.0'],
    extras_require={   
        'test': ['pytest', 'mock', 'nose', 'coverage'],
    },
)