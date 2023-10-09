FROM python:3.11.6

# Install system dependencies for OpenSSH, OpenMPI, and some debugging utilities - could get rid of vim, wget, net-tools for production
RUN apt-get update -y && apt-get upgrade -y && apt-get install sudo vim git wget net-tools openssh-server openssh-client gcc openmpi-bin openmpi-common libopenmpi-dev libgtk2.0-dev cmake libgoogle-glog-dev -y && apt-get clean && apt-get purge

# Build OpenMPI
RUN wget https://www.open-mpi.org/software/ompi/v4.1/downloads/openmpi-4.1.1.tar.gz && tar -xvzf openmpi-4.1.1.tar.gz
RUN cd openmpi-4.1.1 && ./configure --prefix=/usr/local && make && make install
ENV PATH=”$PATH:/home/.openmpi/bin”
ENV LD_LIBRARY_PATH=”$LD_LIBRARY_PATH:/home/.openmpi/lib”

# Build libgrape
RUN git clone https://github.com/alibaba/libgrape-lite.git
RUN cd libgrape-lite && mkdir ./build && cd ./build && cmake .. && make -j
RUN cd libgrape-lite/examples/analytical_apps && cmake ../.. && make
# RUN cd libgrape-lite/examples/graph_sampler && cmake ../.. && make

# Start SSH service
RUN service ssh start

# Expose docker port 22
EXPOSE 22

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Start SSH daemon - Need to do in Metaflow, since Metaflow replaces CMD.
CMD ["/usr/sbin/sshd","-D"]