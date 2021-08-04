import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube-data",
    version="0.1.1",
    author="Luiz P.",
    author_email="umluiz@gmail.com",
    description="Get YouTube data for analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umLu/youtube-data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="youtube data caption",
    package_dir={"": "youtubedata"},
    packages=setuptools.find_packages(where="youtubedata"),
    install_requires=["google-api-python-client",
                      "pandas",
                      "youtube_transcript_api"],
    python_requires=">=3.6",
)