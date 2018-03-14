from setuptools import setup

setup(
    name='fext',
    version='0.1',
    description='Frame Extraction Utility',
    url='http://github.com/theseanything/fext',
    author='Sean Rankine',
    author_email='srdeveloper@icloud.com',
    license='MIT',
    packages=['fext'],
    package_dir={
        'fext': 'fext'
    },
    py_modules=['fext'],
    entry_points={
        'console_scripts': [
            'fext = fext.cli:main'
        ]
    },
    zip_safe=False,
    keywords="fext",
    install_requires=[
        "click==6.6"
    ]
)
