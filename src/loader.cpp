#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <chrono>
#include "logger.h"
#include <omp.h>
#include <mpi.h>

void processRecords(const std::vector<std::string>& records, int rank) {
    using namespace std::chrono;

    // Preparing for parallel execution
    #pragma omp parallel
    {
        // Each thread will have its own stringstream to accumulate its output
        std::ostringstream threadOutput;
        
        // Get the start time for the whole processing (not thread-local)
        auto processStartTime = high_resolution_clock::now();

        #pragma omp for // Distribute loop iterations across threads
        for (size_t i = 0; i < records.size(); ++i) {
            // Simulate record processing or include your processing logic here
            // This is a placeholder for the actual work done on each record

            auto currentTime = high_resolution_clock::now();
            auto elapsedMilliseconds = duration_cast<milliseconds>(currentTime - processStartTime).count();
            
            // Use threadOutput for logging to avoid critical section here
            threadOutput << elapsedMilliseconds << ",1\n"; // Assuming processing of one record at a time
        }

        // Now, critical section is used only when writing from the thread's stringstream to the file
        #pragma omp critical
        {
            std::ofstream outFile("records_timing_process_" + std::to_string(rank) + ".txt", std::ios::app);
            if (!outFile) {
                #pragma omp critical
                {
                    std::cerr << "Failed to open file for writing by thread." << std::endl;
                }
            } else {
                outFile << threadOutput.str();
            }
        }
    }
    // The rest of your function...
}
