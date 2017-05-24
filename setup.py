from distutils.core import setup

setup(
    name='boulder-chat',
    version='0.1dev',
    packages=['boulder_chat',],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'pytest',
        'cryptography',
        'pika',
    ],
)
