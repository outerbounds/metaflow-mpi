from metaflow import FlowSpec, step, kubernetes, mpi, current, Parameter

N_CPU = 8
N_NODES = 2


class Pagerank(FlowSpec):
    max_rounds = Parameter(
        "pr_mr",
        help="Maximum number of rounds to run the pagerank algorithm for.",
        default="10",
    )

    damping_factor = Parameter(
        "pr_d", help="Damping factor for pagerank algorithm.", default="0.85"
    )

    @step
    def start(self):
        self.next(self.multinode, num_parallel=N_NODES)

    @kubernetes(image="eddieob/libgrape:2", cpu=N_CPU)
    @mpi
    @step
    def multinode(self):
        import os

        libgrape_path = "/libgrape-lite"
        examples_path = "%s/examples/analytical_apps" % libgrape_path
        os.chdir(examples_path)

        dataset_path = "%s/dataset" % libgrape_path

        current.mpi.exec(
            args=[
                "-n",
                str(N_CPU * N_NODES),
                "--allow-run-as-root",
                "--hostfile",
                "/metaflow/hostfile.txt",
            ],
            program="./run_app",  # Precompiled (in docker build) program
            program_args=[
                "--application",
                "pagerank",  # Application - counting the number and quality of links to a page
                "--vfile",
                "%s/p2p-31.v" % dataset_path,  # Vertex data
                "--efile",
                "%s/p2p-31.e" % dataset_path,  # Edge data
                "--pr_mr",
                self.max_rounds,
                "--pr_d",
                self.damping_factor,
                "--out_prefix",
                "./output_pagerank",
            ],
        )

        self.next(self.join)

    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    Pagerank()
