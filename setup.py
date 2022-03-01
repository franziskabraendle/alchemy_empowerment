import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
   name='empowerment-exploration',
   version='0.1dev',
   author='Franziska Brändle & Lena Stocks',
   author_email='franziska.braendle@tuebingen.mpg.de',
   description='Exploration as Empowerment in Little Alchemy 2',
   long_description=long_description,
   long_description_content_type='text/markdown',
   url='https://github.com/franziskabraendle/empowerment',
   packages=setuptools.find_packages(), 
   include_package_data=True,
   classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='littlealchemy2 exploration empowerment cognitivescience research',
    project_urls={
        'CPI Lab': 'http://cpilab.org/'
    },
    python_requires='>=3',
    # py_modules=["six"], # single-file Python modules that aren’t part of a package
    # install_requires=['peppercorn'], # used to specify what dependencies a project minimally needs to run
)
