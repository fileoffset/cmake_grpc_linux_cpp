#include "GameServer.hpp"

#include <grpc++/grpc++.h>

#include <iostream>

namespace cs {

GameServer::GameServer()
{
       
}

GameServer::~GameServer()
{
    m_RpcServer->Shutdown();

    m_CompletionQueue->Shutdown();
}

void GameServer::Run()
{
    std::cout << "Game server started" << std::endl;

    m_RpcServerThread = std::thread([this](){ StartRpcServer(); });

    if (m_RpcServerThread.joinable())
        m_RpcServerThread.join();

    if (m_RpcHandlerThread.joinable())
        m_RpcHandlerThread.join();

    std::cout << "Game server stopped" << std::endl;
}

void GameServer::HandleAction(const cliser::StartGame& action, cliser::ActionReply* reply)
{
    std::cout << "ACTION: StartGame\n";

}

void GameServer::HandleAction(const cliser::GetLevels& action, cliser::ActionReply* reply)
{
    std::cout << "ACTION: GetLevels\n";
    std::cout << "ACTION:   version: " << action.client_version() << '\n';
    std::cout << "ACTION REPLY: " << reply << '\n';

    auto levelsReply = reply->mutable_get_levels_reply();

    for (int i = 0; i < 3; ++i)
    {
        levelsReply->add_levels();
        auto level = levelsReply->mutable_levels(i);
        level->set_name("Level x");
        level->set_cell_width(20);
        level->set_cell_height(20);
    }   

}

void GameServer::HandleAction(const cliser::EndGame& action, cliser::ActionReply* reply)
{
    std::cout << "ACTION: EndGame\n";
}

void GameServer::HandleRpcEvents()
{
    void* tag = nullptr;  // uniquely identifies a request.
    bool ok = false;

    // Block waiting to read the next event from the completion queue. The
    // event is uniquely identified by its tag, which in this case is the
    // memory address of a RpcRequest instance.
    // The return value of Next should always be checked. This return value
    // tells us whether there is any kind of event or cq_ is shutting down.
    while (m_CompletionQueue->Next(&tag, &ok)) 
    {
        if (ok)
        {
            static_cast<IRpcRequest*>(tag)->Process();
        }
        else
        {
            static_cast<IRpcRequest*>(tag)->Finish();
        }
    }
}

void GameServer::StartRpcServer()
{ 
    GameServerImpl service(*this);
    std::string serverAddress("0.0.0.0:50051");

    grpc::ServerBuilder builder;
    
    // Listen on the given address without any authentication mechanism.
    builder.AddListeningPort(serverAddress, grpc::InsecureServerCredentials());

    // Register "service" as the instance through which we'll communicate with
    // clients. In this case it corresponds to an *synchronous* service.
    builder.RegisterService(&service);
    
    // Finally assemble the server.
    m_RpcServer = builder.BuildAndStart();
    m_CompletionQueue = builder.AddCompletionQueue();
    
    std::cout << "Server listening on " << serverAddress << std::endl;

    // start a thread to handle polling for rpc events
    m_RpcHandlerThread = std::thread([this](){ HandleRpcEvents(); });

    // Wait for the server to shutdown. Note that some other thread must be
    // responsible for shutting down the server for this call to ever return.
    m_RpcServer->Wait();   
}

} // namespace cs {
