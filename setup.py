import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydispo",
    version="20.10b1",
    author="Aakash Patil",
    description="A Disposable Mailbox Powered by Pure-Python",
    license="GPL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="privacy disposable-email temporary-email",
    url="https://github.com/aakash30jan/pydispo",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    platforms=['any'],
    classifiers=[
        "Programming Language :: Python ",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["pydispo = pydispo.pydispo:main"]},
)
 
