#pragma once
#include <WinSock2.h>
#include <string>

#pragma comment(lib, "ws2_32")

constexpr auto BUFFER_SIZE = 1024;

class Client {
public:

	Client(std::string server_ip, int port_number) {
		WSADATA wd;
		WSAStartup(MAKEWORD(2, 2), &wd);

		client_socket = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
		SOCKADDR_IN addr = {};
		addr.sin_family = AF_INET;
		addr.sin_port = htons(port_number);
		addr.sin_addr.s_addr = inet_addr(server_ip.c_str());

		connect(client_socket, (SOCKADDR*)&addr, sizeof addr);
	}

	~Client() {
		closesocket(client_socket);
		WSACleanup();
	}

	void send_data(std::string data) {
		send(client_socket, data.c_str(), data.size(), 0);
	}

	std::string recv_data() {
		char buffer[BUFFER_SIZE] = {};
		recv(client_socket, buffer, BUFFER_SIZE, 0);
		return std::string(buffer);
	}

private:
	SOCKET client_socket;
};