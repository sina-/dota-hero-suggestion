try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='DotaHeroSuggestion',
      version='0.1',
      description='A program that suggested counter hero picks',
      author='Sina Tamanna',
      install_requires=['scrapy',
                        'selenium'])
