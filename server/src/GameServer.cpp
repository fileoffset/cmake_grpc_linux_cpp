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
    m_RpcHandlerThread = std::thread([this](){ HandleRpcEvents(); });

    if (m_RpcServerThread.joinable())
        m_RpcServerThread.join();

    std::cout << "Game server stopped" << std::endl;
}

void GameServer::HandleAction(const cliser::StartGame& action, cliser::ActionReply* reply)
{

}

void GameServer::HandleAction(const cliser::GetLevels& action, cliser::ActionReply* reply)
{

}

void GameServer::HandleAction(const cliser::EndGame& action, cliser::ActionReply* reply)
{

}

void GameServer::HandleRpcEvents()
{
    void* tag;  // uniquely identifies a request.
    bool ok;

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
    
    std::cout << "Server listening on " << serverAddress << std::endl;

    // Wait for the server to shutdown. Note that some other thread must be
    // responsible for shutting down the server for this call to ever return.
    m_RpcServer->Wait();   
}

} // namespace cs {
