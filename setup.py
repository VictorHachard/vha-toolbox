import pathlib

import setuptools

long_description = (pathlib.Path(__file__).parent.resolve() / 'README.md').read_text(encoding='utf-8')

setuptools.setup(
    name='vha-toolbox',
    version='0.0.1',
    author='Victor Hachard',
    author_email='31635811+VictorHachard@users.noreply.github.com',
    description='My personal Python toolbox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/VictorHachard/my-python-package',
    project_urls = {
        "Bug Tracker": "https://github.com/VictorHachard/my-python-package/issues"
    },
    license='MIT',
    packages=['vha_toolbox'],
)
