#include <mpi.h>
#include <vector>
#include <string>
#include "reader.h"
#include "loader.h"
#include "logger.h"
#include "VehicleRecord.h"

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    logMessage("MPI Initialized.", rank);

    std::vector<VehicleRecord> records; // Correctly declared as a vector of VehicleRecord
    std::string filePath = "/Users/spartan/Documents/SJSU/Sem2/CMPE-275/Mini2/Final_code/CMPE-275-HPC/data/processed.csv"; 

    distributeRecords(filePath, rank, size, records); // Now correctly matches the updated signature
    processRecords(records, rank); // Also matches the updated signature

    logMessage("Finalizing MPI.", rank);

    MPI_Finalize();

    return 0;
}
