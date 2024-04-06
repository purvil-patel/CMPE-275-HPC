// main.cpp
#include <mpi.h>
#include <vector>
#include <string>
#include "reader.h"
#include "loader.h"
#include "logger.h"

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    logMessage("MPI Initialized.", rank);

    std::vector<std::string> records;
    std::string filePath = "/Users/spartan/Documents/SJSU/Sem2/CMPE-275/Mini2/Final_code/CMPE-275-HPC/data/processed.csv"; 

    distributeRecords(filePath, rank, size, records);
    processRecords(records, rank);

    logMessage("Finalizing MPI.", rank);

    MPI_Finalize();

    return 0;
}
