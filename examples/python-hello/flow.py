from metaflow import FlowSpec, step, kubernetes, batch, mpi, current, parallel
from consts import N_CPU, N_NODES, MEMORY


class CoreweaveMPI4PyFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.multinode, num_parallel=N_NODES)

    # @kubernetes(image="eddieob/mpi-base:1", cpu=N_CPU, memory=MEMORY)
    @batch(image="eddieob/mpi-base:1", cpu=N_CPU, memory=MEMORY)
    @mpi
    @step
    def multinode(self):
        current.mpi.exec(
            args=["-n", str(N_CPU * N_NODES), "--allow-run-as-root"],
            program="python mpi_hello_world.py",
        )

        self.next(self.join)

    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    CoreweaveMPI4PyFlow()
