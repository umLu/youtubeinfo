import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtubeinfo",
    version="0.1.4",
    author="Luiz P.",
    author_email="umluiz@gmail.com",
    description="Get YouTube data for analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umLu/youtubeinfo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="youtube data caption",
    packages=setuptools.find_packages(),
    install_requires=["google-api-python-client",
                      "pandas",
                      "youtube_transcript_api"],
    python_requires=">=3.6",
)
