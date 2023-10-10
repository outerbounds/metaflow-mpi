FROM python:3.11.6

# Install system dependencies for OpenSSH, OpenMPI, and some debugging utilities - could get rid of vim, wget, net-tools for production
RUN apt-get update -y && apt-get upgrade -y && apt-get install sudo vim wget net-tools openssh-server openssh-client gcc openmpi-bin openmpi-common libopenmpi-dev libgtk2.0-dev -y && apt-get clean && apt-get purge

# Build OpenMPI
RUN wget https://www.open-mpi.org/software/ompi/v4.1/downloads/openmpi-4.1.1.tar.gz && tar -xvzf openmpi-4.1.1.tar.gz
RUN cd openmpi-4.1.1 && ./configure --prefix=/usr/local && make && make install
ENV PATH=”$PATH:/home/.openmpi/bin”
ENV LD_LIBRARY_PATH=”$LD_LIBRARY_PATH:/home/.openmpi/lib”
RUN sudo ldconfig

# Start SSH service
RUN service ssh start

# Install mpi4py
RUN pip install --user -U setuptools \
    && pip install --user https://github.com/mpi4py/mpi4py/releases/download/3.1.4/mpi4py-3.1.4.tar.gz

# Expose docker port 22
EXPOSE 22

# Start SSH daemon - Need to do in Metaflow, since Metaflow replaces CMD.
CMD ["/usr/sbin/sshd","-D"]