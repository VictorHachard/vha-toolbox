import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='toolbox',
    version='0.0.1',
    author='Victor Hachard',
    author_email='31635811+VictorHachard@users.noreply.github.com',
    description='Testing installation of Package',
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/VictorHachard/my-python-package',
    project_urls = {
        "Bug Tracker": "https://github.com/VictorHachard/my-python-package/issues"
    },
    license='MIT',
    packages=['toolbox'],
)