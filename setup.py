import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='config_auditing',
    version='1.0',
    author='Katlin Sampson',
    author_email='kvsampso@purdue.edu',
    description='Switch config auditing and managment',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.itap.purdue.edu/ITIS-Networking/config_auditing',
    project_urls={
        'Bug Tracker': 'https://github.itap.purdue.edu/ITIS-Networking/config_auditing/issues',
    },
    license="LICENSE.md",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=['nil_lib'],
)