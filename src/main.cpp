#include <mpi.h>
#include <fstream>
#include <iostream>
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
    std::string filePath = "../data/NYC_Parking_violation_dataset.csv"; 

    distributeRecords(filePath, rank, size, records);
    processRecords(records, rank);

    // Ensures all processes have finished processing
    MPI_Barrier(MPI_COMM_WORLD); 

    if (rank == 0) {
        std::ofstream combinedFile("../final_data/combined_cleaned_data.csv");
        for (int i = 0; i < size; i++) {
            std::string filename = "../data/cleaned_data_rank_" + std::to_string(i) + ".csv";
            // std::string filename = "cleaned_data_process_" + std::to_string(i) + ".csv";
            std::ifstream inputFile(filename);
            if (inputFile.is_open()) {
                combinedFile << inputFile.rdbuf();
                inputFile.close();
            } else {
                logMessage("Failed to open file: " + filename + " for combining.", rank);
            }
        }
        combinedFile.close();
        logMessage("All processed data combined into a single file.", rank);
    }

    logMessage("Finalizing MPI.", rank);

    double endTime = MPI_Wtime();  // End timing
    double executionTime = endTime - startTime;
    if (rank == 0) {
        std::cout << "Total Execution Time: " << executionTime << " seconds." << std::endl;
    }

    MPI_Finalize();

    return 0;
}
