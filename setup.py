import sys

from setuptools import setup, find_packages

setup(
    name='stormssh',
    version='0.7.0',
    packages=find_packages(),
    package_data={'storm': ['templates/*.html', 'static/css/*.css',
                            'static/css/themes/storm/*.css', 'static/css/themes/storm/img/*.png',
                            'static/js/*.js', 'static/js/core/*.js', 'static/favicon.ico']},
    include_package_data=True,
    url='https://github.com/DonKannalie/storm',
    license='MIT',
    author='Emre Yilmaz',
    author_email='ohnemir@gmx.de',
    description='Management commands to ssh config files.',
    entry_points={
        'console_scripts': [
            'storm = storm.__main__:main',
        ],
    },
    install_requires=list(filter(None, [
        "paramiko",
        "termcolor",
        "flask",
        "argparse" if sys.version_info[:2] < (2, 7) else None,
        "six",
        "iterfzf"
    ])),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Systems Administration',
    ]
)

# import sys
# from storm import __version__
#
# from setuptools import setup, find_packages
#
# setup(
#     name='stormssh',
#     version=__version__,
#     packages=find_packages(),
#     package_data={'storm': ['templates/*.html', 'static/css/*.css',
#                             'static/css/themes/storm/*.css', 'static/css/themes/storm/img/*.png',
#                             'static/js/*.js', 'static/js/core/*.js', 'static/favicon.ico']},
#     include_package_data=True,
#     url='https://github.com/DonKannalie/storm',
#     license='MIT',
#     author='Jonas Kahlen',
#     author_email='ohnemir@gmx.de',
#     description='Management commands to ssh config files.',
#     entry_points={
#         'console_scripts': [
#             'storm = storm.__main__:main',
#         ],
#     },
#     install_requires=list(filter(None, [
#         "paramiko",
#         "termcolor",
#         "flask",
#         "colorama",
#         "argparse" if sys.version_info[:2] < (2, 7) else None,
#         "six",
#         "iterfzf"
#     ])),
#     classifiers=[
#         'Development Status :: 5 - Production/Stable',
#         'Intended Audience :: Developers',
#         'Intended Audience :: System Administrators',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 2',
#         'Programming Language :: Python :: 2.7',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.2',
#         'Programming Language :: Python :: 3.3',
#         'Programming Language :: Python :: 3.4',
#         'License :: OSI Approved :: MIT License',
#         'Topic :: System :: Systems Administration',
#     ]
# )
