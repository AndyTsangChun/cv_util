import os
import platform
import setuptools

try :
	from setuptools import setup,find_packages
except ImportError:
	from distutils.core import setup,find_packages

_VERSION = '0.0.0'

cwd = os.path.dirname(os.path.abspath(__file__))

REQUIRED_PACKAGES = [
	'pyutil>=0.0.0',
    'opencv-python>=3.4.1.15',
	'opencv-contrib-python>=3.4.1.15',
	'imutils>=0.4.5',
	'numpy==1.14.2',
	'scipy>=1.0.0',
	'Pillow>=5.0.0'
]

setup(name='cvplus',
	packages=['cvplus'],
	version=_VERSION,
	description='Computer Vision Util Library',
	install_requires=REQUIRED_PACKAGES,
	classifiers=[
		'Programming Language :: Python :: 3.5',
		'Topic :: Computer Vision :: Util'
	],
	keywords='computervision util',
	url='',
	author='Andy Tsang',
	author_email='atc1992andy@gmail.com',
	license='Apache License 2.0',
	zip_safe=False)
