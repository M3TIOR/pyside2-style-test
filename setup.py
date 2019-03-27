import setuptools
import pyside2_style_test as testkit

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as req:
	dependencies = req.read()

setuptools.setup(
    name="m3-pyside2-style-test",
    version=testkit.__version__,
    author=testkit.__author__,
    author_email="cplusplusook@gmail.com",
	license="MIT",
    description="A Qt-5 interactive stylesheet preview script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m3tior/pyside2-style-test",
    packages=setuptools.find_packages(),
	install_requires=dependencies,
	entry_points={
		"console_scripts": "pyside2-style-test=pyside2_style_test.cli:_main"
	},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
