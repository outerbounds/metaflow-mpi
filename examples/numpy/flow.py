from metaflow import FlowSpec, step, kubernetes, mpi, current, conda
from examples import N_CPU, N_NODES

class NumpyArrayPassFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.multinode, num_parallel=N_NODES)

    @conda(python="3.11", libraries={"mpi4py": "3.1.4", "numpy": "1.26.0"})
    @kubernetes(image="eddieob/mpi-ssh:7", cpu=N_CPU)
    @mpi
    @step
    def multinode(self):
        current.mpi.exec(args=["-n", str(N_CPU * N_NODES)], program="python examples.py")
        self.next(self.join)

    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == "__main__":
    NumpyArrayPassFlow()