// logger.cpp
#include "logger.h"
#include <fstream>
#include <sstream>
#include <iostream>

void logMessage(const std::string& message, int rank) {
    std::ostringstream filename;
    filename << "log_process_" << rank << ".txt";
    std::ofstream logFile(filename.str(), std::ios::app); // Append mode

    if (logFile.is_open()) {
        logFile << message << std::endl;
        logFile.close();
    } else {
        std::cerr << "Failed to open log file for process " << rank << std::endl;
    }
}
