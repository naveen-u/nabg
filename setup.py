from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nabg",
    version="1.0.1",
    description="A customizable bullshit generator based on Seb Pearce's 'New-Age Bullshit Generator'",
    py_modules=["nabg", "patterns", "vocabulary"],
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
    entry_points={
        "console_scripts": [
            "nabg=nabg:main",
        ]
    },
)
