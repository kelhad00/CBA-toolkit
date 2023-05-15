from setuptools import setup, find_packages

# Lecture des dépendances depuis le fichier requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='CBA-TOOLKIT',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
)