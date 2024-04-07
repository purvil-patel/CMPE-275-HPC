#ifndef READER_H
#define READER_H

#include <string>
#include <vector>
#include "VehicleRecord.h" // Include the definition of VehicleRecord

void calculateOffsets(const std::string& filePath, std::vector<long>& offsets);
void distributeRecords(const std::string& filePath, int rank, int size, std::vector<VehicleRecord>& records);

#endif // READER_H
