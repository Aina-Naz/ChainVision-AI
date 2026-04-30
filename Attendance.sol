// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AttendanceSystem {
    
    struct Record {
        string name;
        string time;
        string lecture;
        string date;
    }

    mapping(string => Record[]) public studentRecords;

    event AttendanceMarked(string name, string time, string lecture);

    function markAttendance(string memory _name, string memory _time, string memory _lecture, string memory _date) public {
        Record memory newRecord = Record(_name, _time, _lecture, _date);
        studentRecords[_name].push(newRecord);
        
        emit AttendanceMarked(_name, _time, _lecture);
    }

    function getAttendanceCount(string memory _name) public view returns (uint) {
        return studentRecords[_name].length;
    }
}