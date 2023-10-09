import socket

try:
    import mpi4py
    from mpi4py import MPI
except ImportError:
    pass

N_CPU = 24
N_NODES = 3

if __name__ == '__main__':
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = socket.gethostbyname('localhost')

    print(f"Rank {rank} process on {ip} of {size} processes.")

    for i in range(N_CPU * N_NODES):
        if rank == 0:
            msg = "Message from control task."
            comm.send(msg, dest=i)
        elif rank == i:
            s = comm.recv()
            print("rank %d: %s" % (rank, s))