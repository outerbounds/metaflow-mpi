### Introduction
[MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) is a standard framework for writing parallel applications. `metaflow-mpi` is an extension for Metaflow that allows you to dynamically form a multi-node MPI cluster using Metaflow to make it easier to run your MPI programs on any infrastructure.

### Features
- **Automatic SSH configuration**: Researchers and MPI program developers don't need to worry about how to form the MPI cluster. Metaflow's `@mpi` decorator will do this for you so you can assume nodes are able to pass information to each other.
- **Seamless Python interface**: Many MPI programs are written in C and Fortran, making them hard to use with Python orchestration systems. Metaflow's `@mpi` exposes a set of methods shaped like `current.mpi.<METHOD>` to make it easy to run MPI commands on your transient MPI cluster.

### Installation
Install this experimental module:
```
pip install metaflow-mpi
```

To use the MPI integration in your Metaflow steps, you will need those steps to be run in a Docker container that has an MPI implementation - we have mainly test against [OpenMPI](https://www.open-mpi.org/), which you can build as shown [here](./examples/Dockerfile).

### Getting Started
After installing the module, you can import the `mpi` decorator and annotate steps with it.
Doing this exposes four new methods on the Metaflow `current` object, which you can see described in context of the following workflow scaffolding:
```python
# flow.py
from metaflow import FlowSpec, step, batch, mpi, current

class MPI4PyFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.multinode, num_parallel=4)

    @batch(cpu=32)
    @mpi
    @step
    def multinode(self):
        # matches mpiexec command
        current.mpi.exec(
            args=["-n", "128"],
            program="python mpi_program.py",
        )
        # others: 
            # current.mpi.run: matches mpirun command
            # current.mpi.cc: matches mpicc command
            # current.mpi.broadcast_file: sends file from control to all others, such as a compiled binary.
        
        ...
    ...

if __name__ == "__main__":
    MPI4PyFlow()
```

### Examples

| Directory | MPI program description |
| :--- | ---: |
| [Hello C](examples/c-hello/README.md) | Run a hello world C program that shows how to include, compile, and run a c program on your dynamically formed MPI cluster. |  
| [Hello Python](examples/python-hello/README.md) | A hello world program using [mpi4py](https://mpi4py.readthedocs.io/en/stable/). |  
| [NumPy Array Passing](examples/numpy/README.md) | An MPI program that shows you how to broadcast, scatter, gather, and implement your own all reduce routine on NumPy arrays. |  
| [LibGrape](examples/libgrape-ldbc-graph-benchmark/README.md) | A set of workflows, each run using the [LibGrape framework](https://github.com/alibaba/libgrape-lite) from Alibaba, showing how to run highly scalable graph algorithms such as weakly connected component, pagerank, and breadth first search.|


### License
`metaflow-mpi` is distributed under the <u>Apache License</u>.