rom setuptools import setup

setup(
    name='xgb pipeline example',
    version='0.1',
    packages=[],
    url='',
    license='',
    author='aniftos',
    author_email='aniftos@google.com',
    description='',

    install_requires=[
        'kfp==1.8.9',
        
    ],
    
    extras_require={   
        'run': ['google-cloud-pipeline-components==0.2.0'],
    },
)