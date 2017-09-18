#include "GameServer.hpp"

#include <stdio.h>

int main(int argc, char** argv)
{
    printf("Starting game server\n");

    cs::GameServer gameServer;

    gameServer.Run();

    printf("Server shutdown\n");

    return 0;
}
