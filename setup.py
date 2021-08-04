from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='packagedna',
    version='0.0.1',
    packages='',
    url='https://www.elevenpaths.com',
    license='GPU',
    author='ElevenPaths',
    author_email='innovationlab@11paths.com',
    description='Tool for inspection packages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Security"
     ],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)