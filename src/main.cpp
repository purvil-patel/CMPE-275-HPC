#include <mpi.h>
#include <vector>
#include <string>
#include "reader.h"
#include "loader.h"
#include "logger.h"
#include <iostream>

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    double startTime = MPI_Wtime();

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    logMessage("MPI Initialized.", rank);

    std::vector<std::string> records;
    std::string filePath = "../data/processed.csv"; 

    distributeRecords(filePath, rank, size, records);
    processRecords(records, rank);

    logMessage("Finalizing MPI.", rank);

    double endTime = MPI_Wtime();
    double executionTime = endTime - startTime;
    if (rank == 0) {
        std::cout << "Total Execution Time: " << executionTime << " seconds." << std::endl;
    }

    MPI_Finalize();

    return 0;
}
