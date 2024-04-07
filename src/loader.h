#ifndef LOADER_H
#define LOADER_H

#include <vector>
#include "VehicleRecord.h" // Ensure VehicleRecord is included

void processRecords(const std::vector<VehicleRecord>& records, int rank);

#endif // LOADER_H
