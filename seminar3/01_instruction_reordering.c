// This file implements peterson's solution using pthread library.

// author: Tomáš Vavro
// email: xvavro@stuba.sk
// license: MIT

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

char flag[] = {0, 0};
int turn = 0;

void * process_0(void * data) {
	for (int i = 0; i < 4; ++i) {
		flag[0] = 1;
		turn = 1;
		while (flag[1] == 1 && turn == 1) {}
		printf("process 0 executes its critical section!\n");
		flag[0] = 0;
	}
	return NULL;
}


void * process_1(void * data) {
	for (int i = 0; i < 4; ++i) {
               	flag[1] = 1;
               	turn = 0;
               	while (flag[0] == 1 && turn == 0) {}
               	printf("process	1 executes its critical	section!\n");
               	flag[1] = 0;
        }
	return NULL;
}


int main(int argc, char ** argv) {
	pthread_t t1, t2;
	int t1_ret, t2_ret;
	t1_ret = pthread_create(&t1, NULL, process_0, NULL);
	t2_ret = pthread_create(&t2, NULL, process_1, NULL);
	pthread_join(t1, NULL);
	pthread_join(t2, NULL);
	return 0;
}
