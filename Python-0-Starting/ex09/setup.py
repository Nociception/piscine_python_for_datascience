# file run when `python setup.py install`

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="ft_package",
        version="0.0.1",
        author="eagle",
        author_email="eagle@42.fr",
        description="A sample test package",
        # long_description=open("README.md").read(),
        # long_description_content_type="text/markdown",
        license="MIT",
        url="https://github.com/eagle/ft_package",
        packages=find_packages(),
        python_requires=">=3.6",
        project_urls={}
        # include_package_data=True,
        # package_data={"": [".txt", "*.md"]},
        # classifiers=[
        #     "Programming Language :: Python :: 3",
        #     "License :: OSI Approved :: MIT License",
        #     "Operating System :: OS Independent"
        # ],
    )
