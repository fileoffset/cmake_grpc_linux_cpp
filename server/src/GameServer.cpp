#include "GameServer.hpp"
#include <iostream>

namespace cs {

GameServer::GameServer()
: m_MainThread([this](){ RunLoop(); })
{
       
}

void GameServer::RunLoop()
{
    std::cout << "Game server started" << std::endl;

    std::cout << "Game server stopped" << std::endl;
}

} // namespace cs {
