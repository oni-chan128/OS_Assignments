
/* ASSIGNMENT 2 - QUESTION 2
 *   INTERPROCESS COMMUNICATION USING PIPES */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
	
	int parent_to_child[2];
	int child_to_parent[2];
	
	char message[] = "Hello from the parent process!";
	char received[100];
	char reply[] = "Message received by the child!";
	
	// Create two pipes
	if (pipe(parent_to_child) == -1 ||
		pipe(child_to_parent) == -1) {
		
		perror("Pipe creation failed");
	return 1;
		}
		
		// Create a child process
		pid_t pid = fork();
		
		if (pid == -1) {
			perror("Process creation failed");
			return 1;
		}
		
		// CHILD PROCESS
		if (pid == 0) {
			
			// Child does not send through the first pipe
			close(parent_to_child[1]);
			
			// Child does not receive through the second pipe
			close(child_to_parent[0]);
			
			// Receive message from parent
			int bytes = read(parent_to_child[0],
							 received, sizeof(received) - 1);
			
			if (bytes == -1) {
				perror("Child read failed");
				exit(1);
			}
			
			received[bytes] = '\0';
			
			printf("Child received: %s\n", received);
			
			// Send reply to parent
			if (write(child_to_parent[1],
				reply, strlen(reply)) == -1) {
				
				perror("Child write failed");
			exit(1);
				}
				
				// Close pipes
				close(parent_to_child[0]);
				close(child_to_parent[1]);
				
				exit(0);
		}
		
		// PARENT PROCESS
		
		// Parent does not receive through the first pipe
		close(parent_to_child[0]);
		
		// Parent does not send through the second pipe
		close(child_to_parent[1]);
		
		// Send message to child
		printf("Parent sending: %s\n", message);
		
		if (write(parent_to_child[1],
			message, strlen(message)) == -1) {
			
			perror("Parent write failed");
		return 1;
			}
			
			// Close the first pipe after sending
			close(parent_to_child[1]);
			
			// Receive reply from child
			int bytes = read(child_to_parent[0],
							 received, sizeof(received) - 1);
			
			if (bytes == -1) {
				perror("Parent read failed");
				return 1;
			}
			
			received[bytes] = '\0';
			
			printf("Parent received: %s\n", received);
			
			// Close the second pipe
			close(child_to_parent[0]);
			
			// Wait for the child process to finish
			wait(NULL);
			
			printf("Communication completed successfully.\n");
			
			return 0;
}
