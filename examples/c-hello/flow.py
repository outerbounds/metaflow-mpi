from metaflow import FlowSpec, step, kubernetes, mpi, current

N_CPU = 8
N_NODES = 3

class MPIFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.multinode, num_parallel=N_NODES)

    @kubernetes(image="eddieob/mpi-ssh:7", cpu=N_CPU)
    @mpi
    @step
    def multinode(self):

        # Compile c program.
        current.mpi.cc(args=["-o", "mpi_hello_world_binary", "mpi_hello_world.c"])

        # Broadcast the compiled binary to all worker tasks.
        current.mpi.broadcast_file("mpi_hello_world_binary")

        # Run the program.
        current.mpi.exec(args=["-n", str(N_CPU * N_NODES), "--allow-run-as-root"], program="mpi_hello_world_binary")
        
        self.next(self.join)

    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == "__main__":
    MPIFlow()