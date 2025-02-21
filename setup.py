from setuptools import setup, find_packages

setup(
    name="photoff",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cffi>=1.17.1",
    ],
    author="Beltran offerrall",
    author_email="offerrallps4@gmail.com",
    description="A minimal CUDA-based image composition library",
    python_requires=">=3.7",
)