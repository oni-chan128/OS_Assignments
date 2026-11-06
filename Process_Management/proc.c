#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void)
{
	pid_t pid = fork();
	
	if(pid < 0) {
		perror("fork failed");
		return 1;
	}
	
	if(pid == 0) {
		printf("Child process running, PID: %ld\n", (long)getpid());
		fflush(stdout);
		
		execlp("echo", "echo", "Child program replaced using execlp()", (char *)NULL);
		
		perror("execlp failed");
		_exit(127);
		
	}
	
	printf("Parent PID: %ld. Wait for child PID: %ld\n", (long)getpid(), (long)pid);	
	
	int status;
	pid_t result = waitpid(pid, &status, 0);
	
	if(result == -1) {
		perror("waitpid failed");
		return 1;
		
	}
	
	if (WIFEXITED(status)) {
		printf("Child terminated normaly. Exit status: %d\n", WEXITSTATUS(status));
		
	}
		
		printf("Parent process finished.\n");

		return 0;
		
	}
