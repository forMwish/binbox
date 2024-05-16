#include <stdio.h>
#include <time.h>
#include <pthread.h>

void *printStdin(void *arg) {
    char buffer[256];
    while(1){
        while (fgets(buffer, sizeof(buffer), stdin) != NULL) {
            printf("in: %s", buffer);
        }
    }
    return NULL;
}

void printf_time(){
    time_t t;
    struct tm *info;
    char buffer[80];

    static int count_ = 0;
    time(&t);
    info = localtime(&t);

    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", info);
    printf("%s %d\n", buffer, count_++);
    // fflush(stdout);
}

int main(){
    static int count = 0;

    pthread_t tid;
    pthread_create(&tid, NULL, printStdin, NULL);

    while(1){
        printf_time();
        usleep(1000*1000);
        if (count++ > 10){
            break;
        }
    }
    pthread_cancel(tid);
    
    printf("break\n");
    sleep(2);
    printf("over\n");
    
    return 0;
}