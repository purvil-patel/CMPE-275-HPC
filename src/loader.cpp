#include "VehicleRecord.h"
#include "logger.h"
#include <omp.h>
#include <vector>
#include <iostream>
#include <map>          // Include for std::map
#include <sstream>      // Include for std::ostringstream

void processRecords(const std::vector<VehicleRecord>& records, int rank) {
    std::ostringstream msg;
    msg << "Starting to process records. Total records: " << records.size();
    logMessage(msg.str(), rank);

    // Initialize a local map for each thread to avoid the need for critical sections
    std::vector<std::map<int, int>> localMaps(omp_get_max_threads());

    #pragma omp parallel for
    for (size_t i = 0; i < records.size(); ++i) {
        int age = records[i].vehicleAge;
        int threadNum = omp_get_thread_num();
        localMaps[threadNum][age]++;
    }

    // Combine local maps into a single map
    std::map<int, int> violationsByAge;
    for (auto& localMap : localMaps) {
        for (auto& entry : localMap) {
            violationsByAge[entry.first] += entry.second;
        }
    }

    msg.str("");
    msg << "Finished processing records. Total records processed: " << records.size();
    logMessage(msg.str(), rank);

    for (const auto& pair : violationsByAge) {
        std::ostringstream ageMsg;
        ageMsg << "Vehicle Age: " << pair.first << ", Violations: " << pair.second;
        logMessage(ageMsg.str(), rank);
    }
}
