from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="pyjest",
        version="0.0.1",
        author="Hakan Ozler",
        author_email="ozler.hakan@gmail.com",
        description="ipyton magic tool to send HTTP requests in a cell of notebooks",
        long_description=long_description,
        long_description_content_type="text/plain; charset=UTF-8",
        url="https://github.com/ozlerhakan/jest",
        project_urls={
            "Bug Tracker": "https://github.com/ozlerhakan/jest/issues",
        },
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages=find_packages(where='src'),
        package_dir={'': 'src'},
        python_requires=">=3.7",
        keywords=['python', 'magic tool', 'jupyter', 'notebook', 'jest'],
        install_requires=[
            'requests==2.27.1',
            'ipython==7.31.1',
            'tqdm==4.62.3'
        ],
        platforms=["linux", "unix"]
    )
