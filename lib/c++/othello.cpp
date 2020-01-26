#include "log.hpp"
#include "client.hpp"
#include "msg.hpp"

#include <iostream>
#include <string>
#include <vector>
#include <sstream>

class othello {
public:
	othello(std::string ip, int port) 
		: client(ip, port)
		, log()
		, board(), color(), token()
	{
		log.write("Server connection success!");

		auto accept_msg = client.recv_data();
		auto codendata = parse_msg(accept_msg);
		auto code = codendata.first;
		auto data = codendata.second;

		if (code != "accept") {
			log.write("ERROR: accept msg error: " + accept_msg);
			exit(-1);
		}

		board = data["board"];
		color = data["color"];
		token = data["token"];

		log.write("Color: " + color + ", Token: " + token + ", Board: " + board);
	}

	std::pair<std::string, std::map<std::string, std::string> >
	wait_for_turn()
	{
		while (true)
		{
			auto msg = client.recv_data();
			auto codendata = parse_msg(msg);
			auto code = codendata.first;
			auto data = codendata.second;

			if (code == "turn") {
				log.write("turn: " + data["available"]);
				return std::make_pair(code, data);
			}
			else if (code == "update") {
				board = data["board"];
				log.write("update: " + board);
			}
			else if (code == "end") {
				log.write("game end: " + data["status"] + " " + data["score"]);
				log.write("final board: " + data["board"]);
				return std::make_pair(code, data);
			}
			else {
				log.write("invaild code " + code);
				exit(-1);
			}
		}
	}

	void move(std::string& cell_corr)
	{
		auto msg = gen_move_msg(cell_corr, token);
		client.send_data(msg);
	}

	std::string board, color;
private:
	Client client;
	Log log;
	std::string token;
};

void print_board(std::string board_str) {
	std::cout << "  ABCDEFGH" << std::endl;
	int i = 1;
	for (int i = 0; i < 8; ++i) {
		std::cout << i << " " << board_str.substr(i * 8, 8) << std::endl;
	}
}

int main(int argc, char** argv) {
	othello game("127.0.0.1", 6068);
	while (true) {
		auto codendata = game.wait_for_turn();
		auto code = codendata.first;
		auto data = codendata.second;

		if (code == "end") {
			print_board(data["board"]);
			std::cout << data["score"] << std::endl;
			std::cout << data["status"] << std::endl;
			break;
		}
		else if (code == "turn") {
			std::string input;
			print_board(game.board);
			std::cout << "available: " << data["available"] << std::endl;
			std::cin >> input;
			game.move(input);
		}
	}
}