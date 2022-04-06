from setuptools import setup

setup(
	name = "EtherNeoJ", # pip install 所輸入的套件名稱，而不是 python import 使用的名稱
	version = '0.0.1', # 版本號
	description = 'Say hello!', # 套件簡述
	py_modules = ['scuEtherNeoJ'], # 須發佈的 python 模組，用於 python import 使用的名稱
	package_dir = { '' : 'src' }, # 套件來源，目前建立在 src 文件夾路徑
)