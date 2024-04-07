#include <optional>
#include <iostream>
#include <fstream>
#include <mpi.h>
#include <string>
#include <vector>
#include <sstream>
#include "logger.h"
#include "VehicleRecord.h" // Include the header where VehicleRecord is defined

// Assume the VehicleRecord struct is defined in VehicleRecord.h as previously described

std::optional<VehicleRecord> parseLineToRecord(const std::string& line) {
    std::stringstream ss(line);
    std::string item;
    std::vector<std::string> parsedLine;

    while (std::getline(ss, item, ',')) {
        parsedLine.push_back(item);
    }

    try {
        if (parsedLine.size() < 4) {
            std::cerr << "Incomplete line: " << line << std::endl;
            return std::nullopt;
        }
        int violationCode = std::stoi(parsedLine[0]);
        int vehicleYear = std::stoi(parsedLine[1]);
        std::string issueDate = parsedLine[2];
        int vehicleAge = std::stoi(parsedLine[3]);

        return VehicleRecord(violationCode, vehicleYear, issueDate, vehicleAge);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Invalid argument encountered when parsing line: " << line << " | Error: " << e.what() << std::endl;
    } catch (const std::out_of_range& e) {
        std::cerr << "Out of range error encountered when parsing line: " << line << " | Error: " << e.what() << std::endl;
    }
    return std::nullopt;
}



// New function to calculate offsets
void calculateOffsets(const std::string& filePath, std::vector<long>& offsets) {
    std::ifstream file(filePath, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Failed to open file for offset calculation.\n";
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    offsets.push_back(0);  // The first record starts at offset 0
    char c;
    while (file.get(c)) {
        if (c == '\n') {  // Assuming Unix-style line endings
            // Save the position of the start of the next line
            offsets.push_back(file.tellg());
        }
    }
    file.close();
}

void distributeRecords(const std::string& filePath, int rank, int size, std::vector<VehicleRecord>& records) {
    std::vector<long> allOffsets;
    if (rank == 0) {
        calculateOffsets(filePath, allOffsets);
    }
    
    // Broadcast the total count of offsets to all processes
    int totalCount = allOffsets.size() - 1; // Number of records is offsets count - 1
    MPI_Bcast(&totalCount, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Each process calculates its portion of the file to read
    int startIdx = rank * (totalCount / size) + std::min(rank, totalCount % size);
    int endIdx = (rank + 1) * (totalCount / size) + std::min(rank + 1, totalCount % size) - 1;

    long startOffset, endOffset;
    // Handle the distribution of start and end offsets for each process
    if (rank == 0) {
        for (int i = 0; i < size; i++) {
            if (i == 0) {
                startOffset = allOffsets[startIdx];
                endOffset = allOffsets[endIdx + 1]; // To include the last record fully
            } else {
                long offsets[2] = {allOffsets[startIdx], allOffsets[endIdx + 1]};
                MPI_Send(offsets, 2, MPI_LONG, i, 0, MPI_COMM_WORLD);
            }
        }
    } else {
        long offsets[2];
        MPI_Recv(offsets, 2, MPI_LONG, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        startOffset = offsets[0];
        endOffset = offsets[1];
    }

    std::ifstream file(filePath, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Failed to open file on process " << rank << ".\n";
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    file.seekg(startOffset);
    std::string line;
    if (startOffset != 0) {
        // Skip the first line as it may be incomplete
        std::getline(file, line);
    }
    while (file.tellg() < endOffset && std::getline(file, line)) {
        auto recordOpt = parseLineToRecord(line); // Receive optional VehicleRecord
        if (recordOpt) { // Check if there's a value
            records.push_back(*recordOpt); // Dereference to get the VehicleRecord and push it
        } else {
            // Handle the case where parsing failed, e.g., log an error or skip the line
        }
    }
    file.close();
}
