#pragma once

#include "game.grpc.pb.h"

#include <grpc++/grpc++.h>

#include <thread>

namespace cs {

class GameServerImpl;
 
class IActionHandler
{
public:
    virtual ~IActionHandler() = default;

    virtual void HandleAction(const cliser::StartGame& action, cliser::ActionReply* reply) = 0;
    virtual void HandleAction(const cliser::GetLevels& action, cliser::ActionReply* reply) = 0;
    virtual void HandleAction(const cliser::EndGame& action, cliser::ActionReply* reply) = 0;
};
   
class IRpcRequest
{
public:
    virtual void Process() = 0;
    virtual void Finish() = 0;
};

class RpcRequest : public IRpcRequest
{
public:
    RpcRequest();

    void Process() override;
    void Finish() override;

private:
    grpc::ServerContext m_Ctx;

    cliser::Action m_Request;
    cliser::ActionReply m_Reply;

    grpc::ServerAsyncResponseWriter<cliser::ActionReply> m_Responder;
};

class GameServer : private IActionHandler
{
    friend GameServerImpl;

public:
    GameServer();
    ~GameServer();

    void Run();

private:
    void HandleAction(const cliser::StartGame& action, cliser::ActionReply* reply) override;
    void HandleAction(const cliser::GetLevels& action, cliser::ActionReply* reply) override;
    void HandleAction(const cliser::EndGame& action, cliser::ActionReply* reply) override;

    void HandleRpcEvents();

    void StartRpcServer();
    
private:
    bool m_IsRunning;
    bool m_IsShuttingDown;

    std::thread m_RpcServerThread;
    std::thread m_RpcHandlerThread;

    std::unique_ptr<grpc::Server> m_RpcServer;
    std::unique_ptr<grpc::ServerCompletionQueue> m_CompletionQueue;
};

class GameServerImpl final : public cliser::GameService::Service
{
public:
    GameServerImpl(IActionHandler& actionHandler)
    : m_ActionHandler(actionHandler)
    {

    }

private:
    grpc::Status DoAction(
        grpc::ServerContext* context, 
        const cliser::Action* request, 
        cliser::ActionReply* reply) override 
    {
        std::cout << "RECV: Action\n";

        switch (request->messages_case())
        {
            case cliser::Action::kStartGame:
                m_ActionHandler.HandleAction(request->start_game(), reply); break;
            case cliser::Action::kGetLevels:
                m_ActionHandler.HandleAction(request->get_levels(), reply); break;
            case cliser::Action::kEndGame:
                m_ActionHandler.HandleAction(request->end_game(), reply); break;
            case cliser::Action::MESSAGES_NOT_SET:
                return grpc::Status::CANCELLED;

        }

        return grpc::Status::OK;
    }

private:
    IActionHandler& m_ActionHandler;
};

} // namespace cs {
