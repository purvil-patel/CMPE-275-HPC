#ifndef VEHICLE_RECORD_H
#define VEHICLE_RECORD_H

#include <string>

struct VehicleRecord {
    int violationCode;
    int vehicleYear;
    std::string issueDate;
    int vehicleAge;

    // Default constructor
    VehicleRecord() : violationCode(0), vehicleYear(0), issueDate(""), vehicleAge(0) {}

    // Constructor for easy initialization
    VehicleRecord(int code, int year, std::string date, int age)
        : violationCode(code), vehicleYear(year), issueDate(date), vehicleAge(age) {}
};

#endif // VEHICLE_RECORD_H
