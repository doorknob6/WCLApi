from distutils.core import setup
setup(
  name = 'WCLApi',
  packages = ['WCLApi'],
  version = '0.3.1',
  license='MIT',
  description = 'Python tools to communicate with the Wacraftlogs website API.',
  author = 'doorknob6',
  author_email = 'joopkjongste@gmail.com',
  url = 'https://github.com/doorknob6/WCLApi',
  download_url = 'https://github.com/doorknob6/WCLApi/archive/master.tar.gz',
  keywords = ['Nexushub', 'API'],
  install_requires=['requests', 'requests-toolbelt'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
	  'Programming Language :: Python :: 3.7',
	  'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)