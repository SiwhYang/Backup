#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <CoreFoundation/CoreFoundation.h>
#include <chrono>
#define PORT 37716

int main(void){
    
    int server_fd, new_socket =0;
    int opt = 1;
    char buffer[1024] = {0};
    
    char message[] = {"Hi,this is server.\n"};
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    new_socket = socket(AF_INET, SOCK_STREAM, 0);
    
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));
    struct sockaddr_in address {
    .sin_family = AF_INET,
    .sin_addr.s_addr = INADDR_ANY,
    .sin_port = htons( PORT ),
    };
    int addrlen = sizeof(address);
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 10);
    std::cout << "[Server] Listening in port " << PORT << std::endl;
    
    new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
    std::cout << "[Server] Client has successfully connected." << std::endl;
    while(1){
        //recv(new_socket,buffer,sizeof(buffer),0);
        recv(new_socket,buffer,19,0);//
        //透過第3個參數決定一次要取出多少byte數的資源，如果是sizeof(buffer)就是一次拿出全部的
        
        std::cout << "[Server] recieve message :" << buffer << std::endl;
        //std::cout << "[Server] do somthing !" << std::endl;
        send(new_socket,message,sizeof(message),1);
        sleep(3);
    }

    return 0;
}

