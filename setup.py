from setuptools import setup, find_packages

setup(
    name = "simweb",
    version = "0.1.0",
    author = "Alan Shi",
    author_email = "alan@sinosims.com",

    packages = find_packages(),
    include_package_data = True,

    url = "http://www.sinosims.com",
    description = "Simhub Web Service",
    
    install_requires = ["Flask", "redis", "sqlalchemy"],
)
