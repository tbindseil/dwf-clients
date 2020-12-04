from setuptools import find_packages, setup

setup(
    name='dwfclients',
    packages=find_packages(include=['dwfclients', 'dwfclients.auth']),
    version='0.1.0',
    description='Clients for microservices in dwf architecture',
    author='TJ Bindseil',
    license='MIT',
    install_requires=['flask', 'requests'],
    setup_requires=['flask', 'requests', 'mock', 'pytest-runner'],
    tests_require=['flask', 'requests', 'mock', 'pytest==4.4.1'],
    test_suite='tests',
)
