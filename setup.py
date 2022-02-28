from setuptools import setup

setup(
    name='simplesoc',
    url='https://github.com/deino475/simplesoc',
    author='Nile Dixon',
    author_email='niledixon475@gmail.com',
    packages=['simplesoc'],
    install_requires=[],
    version='0.5.0',
    license='GNU GPL-V3',
    description='A simple Python library for assigning Standard Occupational Classification (SOC) codes to job titles.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    python_requires=">=3.6"
)

