from setuptools import setup

setup(
        name='PyConEs',
        version='1.0',
        long_description=__doc__,
        packages=['pycones'],
        include_package_data=True,
        zip_safe=False,
        install_requires=['Flask']
)

