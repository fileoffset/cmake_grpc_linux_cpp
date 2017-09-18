#pragma once

#include <thread>

namespace cs {

class GameServer
{
public:
    GameServer();

    bool Run() { if (m_MainThread.joinable()) m_MainThread.join(); }

private:
    void RunLoop();

private:
    bool m_IsRunning;
    bool m_IsShuttingDown;

    std::thread m_MainThread;
    std::thread m_BackgroundThread;
};

} // namespace cs {
