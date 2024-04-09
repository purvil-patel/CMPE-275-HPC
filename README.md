# High-Performance Computing (HPC) Project

## Overview

This project aims to demonstrate the use of high-performance computing techniques for processing large datasets. Utilizing C++, MPI (Message Passing Interface), and OpenMP, it showcases parallel computing methods to efficiently process and analyze data. The project also features a Flask-based web interface to visualize the analysis results.

## Setup

### Prerequisites

- C++ compiler with C++17 support
- MPI implementation (e.g., Open MPI)
- Python 3 with Flask and Pandas installed
- Matplotlib for Python

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/purvil-patel/CMPE-275-HPC.git
   ```

2. Navigate to the project directory:

   ```
   cd CMPE-275-HPC
   ```

3. Install the required Python packages:

   ```
   pip install flask pandas matplotlib
   ```

## How to Run

1. **Compiling the C++ Program:**

   Compile the C++ program using the following command:

   ```
   g++-13 -o my_program src/main.cpp src/reader.cpp src/loader.cpp src/logger.cpp -std=c++17 -fopenmp -I/opt/homebrew/Cellar/open-mpi/5.0.2_1/include -L/opt/homebrew/Cellar/open-mpi/5.0.2_1/lib -lmpi
   ```

2. **Running the Program:**

   Execute the program using MPI with the desired number of processes. For example, to run with 3 processes:

   ```
   mpiexec -n 3 ./my_program
   ```

3. **Visualizing the Results:**

   Start the Flask application to visualize the processing results:

   ```
   export FLASK_APP=src/ui/app.py
   flask run
   ```

   Access the web interface at `http://localhost:5000`.

## Conclusion

This project exemplifies the potential of parallel computing in handling large datasets efficiently. By leveraging MPI for distributed computing and OpenMP for shared-memory parallelism, it achieves significant performance improvements over traditional single-threaded approaches.
