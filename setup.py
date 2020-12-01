from setuptools import find_packages, setup
setup(
    name='dwfclients',
    packages=find_packages(include=['dwfclients']),
    version='0.1.0',
    description='Clients for microservices in dwf architecture',
    author='TJ Bindseil',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',

)
