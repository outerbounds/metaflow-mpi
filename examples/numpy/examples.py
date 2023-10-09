# Examples: https://mpi4py.readthedocs.io/en/stable/tutorial.html

try:
    from mpi4py import MPI
    import numpy as np
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
except ImportError:
    pass

N_CPU = 4
N_NODES = 2

def broadcast():
    if rank == 0:
        data = np.arange(100, dtype='i')
    else:
        data = np.empty(100, dtype='i')
    comm.Bcast(data, root=0)
    for i in range(100):
        assert data[i] == i

def scatter():
    sendbuf = None
    if rank == 0:
        sendbuf = np.empty([size, 100], dtype='i')
        sendbuf.T[:,:] = range(size)
    recvbuf = np.empty(100, dtype='i')
    comm.Scatter(sendbuf, recvbuf, root=0)
    assert np.allclose(recvbuf, rank)

def gather():
    sendbuf = np.zeros(100, dtype='i') + rank
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 100], dtype='i')
    comm.Gather(sendbuf, recvbuf, root=0)
    if rank == 0:
        for i in range(size):
            assert np.allclose(recvbuf[i,:], i)


def my_add_operator(xmem, ymem, dt, src):
    x = np.frombuffer(xmem, dtype=src.dtype)
    y = np.frombuffer(ymem, dtype=src.dtype)
    z = x + y
    print("Rank %d reducing %s (%s) and %s (%s), yielding %s" % (rank, x, type(x), y, type(y), z))
    y[:] = z

def my_all_reduce():

    from functools import partial

    # Source: https://gist.github.com/mbdriscoll/44757ee6ded326695b41014a42de6e37

    # create numpy arrays to reduce
    N = N_CPU * N_NODES
    src = (np.arange(N) + rank*N).reshape(N_CPU, N_NODES)
    dst = np.zeros_like(src)

    op = MPI.Op.Create(partial(my_add_operator, src=src), commute=True)

    MPI.COMM_WORLD.Reduce(src, dst, op)

    if MPI.COMM_WORLD.rank == 0:
        print("ANSWER: %s" % dst)


if __name__ == '__main__':

    # Test 1
    broadcast()

    # Test 2
    scatter()

    # Test 3
    gather()

    # Test 4
    my_all_reduce()
