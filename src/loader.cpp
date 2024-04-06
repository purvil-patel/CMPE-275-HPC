#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include "logger.h"
#include <omp.h> // Include the OpenMP header

void processRecords(const std::vector<std::string>& records, int rank) {
    int numRecords = records.size();

    // Log the start of processing
    std::ostringstream msg;
    msg << "Starting to process records in parallel. Total records: " << numRecords;
    logMessage(msg.str(), rank);

    // The actual processing part, parallelized using OpenMP
    #pragma omp parallel for default(none) shared(records, numRecords, rank)
    for (int i = 0; i < numRecords; ++i) {
        // Each thread processes a portion of the records
        // Insert your data processing logic here
        // For demonstration, we'll just log the processing of each record by each thread (not recommended for actual logging due to high volume)
        // #pragma omp critical
        // {
        //     std::ostringstream threadMsg;
        //     threadMsg << "Thread " << omp_get_thread_num() << " processing record " << i;
        //     logMessage(threadMsg.str(), rank);
        // }
    }

    // Log the end of processing
    msg.str("");
    msg << "Finished processing records in parallel. Total records processed: " << numRecords;
    logMessage(msg.str(), rank);
}
