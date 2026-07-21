Here are the 10 top categories of **HPC-specific technical skills** (excluding general IT skills like Linux administration, networking, security, cloud computing, and container orchestration), aggregated from the job descriptions with clear, descriptive category names:

---

### 1. Job Scheduling & Workload Management
The core HPC skills for managing compute resources, queuing jobs, and enforcing resource allocation policies.

- Schedulers: Slurm, PBS Pro, IBM Spectrum LSF, Torque, Grid Engine, Altair Grid Engine, UGE
- Queue/partition management and configuration
- Scheduling policies: fair-share, backfill, priorities, reservations, QoS
- Job lifecycle management (submission, execution, teardown)
- Hooks, prolog/epilog scripts, and custom scheduler extensions
- GPU-aware scheduling and topology-aware scheduling
- Accounting and job reporting

---

### 2. Parallel Computing & Programming Models
The programming frameworks and models used to develop and run parallel applications across multiple compute nodes.

- Message Passing Interface (MPI) – OpenMPI, MPICH, MVAPICH2
- OpenMP and hybrid parallelization
- GPU programming: CUDA, HIP, OpenCL, ROCm
- Parallel algorithms and distributed computing
- Shared memory programming
- Profiling and debugging parallel applications
- Performance optimization for parallel workloads

---

### 3. High-Performance Storage & Parallel Filesystems
The specialized storage technologies designed to handle massive datasets and high-throughput I/O in HPC environments.

- Parallel file systems: Lustre, GPFS (IBM Spectrum Scale), BeeGFS, WEKA, VAST, Panasas
- Distributed storage architectures
- Storage performance tuning and I/O optimization
- Metadata servers and object storage targets
- Data movement workflows for large datasets
- Integration with schedulers and compute nodes
- Parallel I/O patterns and optimization (MPI-IO)

---

### 4. High-Speed Interconnects & Networking Fabrics
The specialized networking technologies that provide low-latency, high-bandwidth communication between compute nodes.

- InfiniBand (architecture, topology, management, tuning)
- RDMA (Remote Direct Memory Access) and RoCE (RDMA over Converged Ethernet)
- GPUDirect RDMA and GPUDirect Storage
- NCCL (NVIDIA Collective Communications Library)
- High-performance Ethernet for HPC (Spectrum-X, Slingshot)
- Fabric management (UFM, Subnet Managers)
- NVLink and NVSwitch (GPU-to-GPU interconnect)
- Network topologies (fat-tree, CLOS, non-blocking fabrics)

---

### 5. GPU & Accelerator Infrastructure
The specialized knowledge required to deploy, manage, and optimize GPU-accelerated computing resources.

- NVIDIA GPU platforms: H100, H200, B200, A100, DGX systems
- GPU drivers and firmware (NVIDIA drivers, OFED)
- CUDA toolkit, cuDNN, TensorRT
- MIG (Multi-Instance GPU) and MPS (Multi-Process Service)
- DCGM (Data Center GPU Manager)
- GPU health monitoring and performance benchmarking
- GPU virtualization (GPU passthrough, vGPU, Time-slicing)
- AMD GPU platforms and ROCm stack

---

### 6. HPC Cluster Management & Provisioning
The tools and processes used to deploy, manage, and scale HPC clusters from bare metal to production.

- Cluster management: Bright Cluster Manager, HPCM (HPE Performance Cluster Manager), NVIDIA Base Command Manager, xCAT, Warewulf
- Node provisioning and image management
- Bare-metal deployment and lifecycle management
- Cluster health monitoring and diagnostics
- Node boot workflows and PXE/netboot
- System integration with schedulers and storage
- Cluster validation and acceptance testing

---

### 7. HPC Performance Analysis & Benchmarking
The skills required to measure, analyze, and optimize application and system performance.

- Profiling tools (Nsight Systems, Nsight Compute, Intel VTune, gprof, perf)
- Benchmarking suites (HPL, MLPerf, NCCL-tests, STREAM)
- Performance bottleneck identification (compute, memory, I/O, network)
- Performance modeling and roofline analysis
- Scalability analysis and optimization
- Benchmark design and execution
- Application profiling and workload characterization

---

### 8. HPC Software Stacks & Application Support
The management and support of scientific and engineering applications and their dependencies.

- Compilers (GCC, Intel, LLVM, NVIDIA compilers)
- Software module management (Lmod, Environment Modules)
- Package management (Spack, EasyBuild)
- Scientific libraries (BLAS, LAPACK, FFTW, PETSc)
- Building and compiling HPC applications
- Application porting and optimization
- Application debugging and troubleshooting
- License server management (FlexNet)

---

### 9. HPC Containerization & Reproducibility
The container technologies and practices specifically designed for HPC environments, often focusing on security and performance.

- Container runtimes: Singularity/Apptainer, Enroot, Pyxis, Podman
- Containerized HPC workloads
- Reproducible scientific environments
- Container integration with schedulers
- GPU-accelerated containers
- Rootless containers for security
- Container image creation and optimization

---

### 10. HPC-AI Integration & MLOps
The intersection of HPC and AI/ML workflows, enabling large-scale model training and deployment on HPC infrastructure.

- Deep Learning frameworks: PyTorch, TensorFlow, JAX
- Distributed training strategies: DeepSpeed, Megatron-LM, Horovod, Ray
- MLOps platforms: MLflow, Kubeflow, ClearML
- Foundation model adaptation and fine-tuning (LoRA, parameter-efficient tuning)
- Data pipelines for AI workloads
- Integration of AI frameworks with HPC schedulers
- Large-scale model training and inference optimization
