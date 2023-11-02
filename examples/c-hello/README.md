Run a hello world C program that shows how to include, compile, and run a c program on your dynamically formed MPI cluster.

```
python flow.py --package-suffixes=.c run
```

The above command includes the C program in the Metaflow code package.
Then it is compiled on the head node using `current.mpi.cc`, and broadcast in the `current.mpi.broadcast_file` calls, respectively. Finally, the C program is run using `current.mpi.exec`.