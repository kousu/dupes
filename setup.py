from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

setup(
  name='dupes',
  version='0.0.1',
  description='find duplicate files and folders',
  long_description=(here / 'README.md').read_text(encoding='utf-8'),
  long_description_content_type='text/markdown',
  author='kousu',
  author_email='nick@kousu.ca',
  license='MIT',
  py_modules=[
    'dupes',
  ],
  # if we grow, move everything under src/dupes/ and make that a real package
  # for now, py_modules is enough.
  #packages=find_packages(),
  python_requires='>=3.6,<=3.10', # TODO: actually test these
  install_requires=[
    'tqdm>=4',
  ],
  entry_points={
    'console_scripts': [
      'dupes = dupes:main',
    ],
  },
)
  
