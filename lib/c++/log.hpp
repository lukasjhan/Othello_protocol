#pragma once
#include <string>
#include <chrono>
#include <ctime>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>

class Log {
public:
	Log(bool console = true, std::string filename = "", std::string ext = ".log") 
		: console(console)
	{ 
		if (!filename.size()) {
			filename = get_current_time();
		}

		filename += ext;

		if (!std::filesystem::exists("log"))
			std::filesystem::create_directory("log");

		file.open("log/" + filename);
	}

	~Log() {
		if (file.is_open()) file.close();
	}

	void write(std::string data) {
		auto d = get_current_time();
		d = "[" + d + "] " + data + "\n";
		file.write(d.c_str(), d.size());

		if (console) std::cout << d;
	}


private:
	bool console;
	std::ofstream file;

	std::string get_current_time()
	{
		auto t = std::time(nullptr);
		auto tm = *std::localtime(&t);

		std::ostringstream oss;
		oss << std::put_time(&tm, "%a %b %d %H.%M.%S %Y");
		std::string str = oss.str();
		return str;
	}
};