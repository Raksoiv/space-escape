import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="space-escape-raksoiv",
    version="0.2.0",
    author="Oscar Rencoret",
    author_email="o.rencoret@gmail.com",
    description="Space Escape is a 2D simple endless horizontal scrolling of a space ship avoiding asteroids made with PyGame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raksoiv/space-escape",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Arcade",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    install_requires=[
        'pygame'
    ],
    entry_points={
        "console_scripts": [
            "space-escape = space_escape.main:main",
        ],
    },
    python_requires='>=3.7',
    include_package_data=True,
)
