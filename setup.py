from setuptools import setup, find_packages

setup(
    name="photoff",
    version="0.0.1",
    author="Beltran Offerrall",
    author_email="offerrallps4@gmail.com",
    description="A minimal CUDA-based image composition library",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "cffi",
        "Pillow"
    ],
)
