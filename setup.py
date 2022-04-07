from setuptools import setup

with open('README.md','r') as fh:
    long_description = fh.read()


setup(
	name = "scuEtherNeoJ", # pip install 所輸入的套件名稱，而不是 python import 使用的名稱
	version = '0.0.1', # 版本號
	description = "An Etherscan web scrapy package which contain Neo4J's connection.",
	py_modules = ['scuEtherNeoJ'], # 須發佈的 python 模組，用於 python import 使用的名稱
    package_dir = {'' : 'scuEtherNeoJ'},
    long_description = long_description,
    long_description_content_type='text/markdown',
    install_requires = ["requests>=2.23.0","pandas>=1.3","neo4j>=4.4.2"],
    classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    url = 'https://github.com/sefx5ever/SCU_EtherNeoJ.git',
    author = 'Wyne Tan',
    author_email = 'sefx5ever@gmail.com',
)