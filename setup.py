from setuptools import setup, find_namespace_packages

version = "0.0.1"

setup(
    name="metaflow-mpi",
    version=version,
    description="An EXPERIMENTAL MPI decorator for Metaflow",
    author="Eddie Mattia",
    author_email="eddie@outerbounds.com",
    packages=find_namespace_packages(include=["metaflow_extensions.*"]),
    py_modules=[
        "metaflow_extensions",
    ],
    install_requires=[
         "metaflow"
    ]
)