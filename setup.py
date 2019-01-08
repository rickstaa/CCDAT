'''Setup file used to install the CGDAT package, its dependencies and create a shortcut.'''

# import modules #
import setuptools
import re
import os

# Open Readme #
if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    # # get git version
    # git_release = re.sub('^v', '', os.popen('git describe').read().strip())
    # # The short X.Y version.
    # git_version = git_release.split("-")[0]
    git_version = r"v1.5.3"

    # Run setup function #
    setuptools.setup(
        name="cgdat",
        version=git_version,
        author="Rick Staa",
        author_email="author@example.com",
        description="A simple csv data analyse tool.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/pypa/sampleproject",
        packages=setuptools.find_packages(),
        entry_points = {
            'console_scripts': ['cgdat-gui=cgdat.start_cl:main','cgdat-shortcut=cgdat.create_shortcut_cl:main'],
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
              'pandas',
              'numpy',
              'xlsxwriter',
              'PyQt5',
        ],
        package_data = {
            'docs': ['docs/*'],
        },
        include_package_data=True,
    )
