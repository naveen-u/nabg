from setuptools import setup, version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nabg",
    version="1.0.0",
    description="A simple bullshit generator",
    py_modules=["nabg"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["click > 7.0"],
    extras_require={"dev": ["pytest>=6.2.2"]},
    url="https://github.com/naveen-u/nabg",
    author="Naveen Unnikrishnan",
    author_email="naveenunnikrishnan98@gmail.com",
)
