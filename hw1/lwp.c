#include <stdlib.h>
#include <unistd.h>

#include "lwp.h"

schedfun lwp_scheduler = NULL;
void * lwp_StackPointer;
unsigned int nextPid = 0; // Program assigns processIDs incrementally

lwp_context lwp_table[LWP_PROC_LIMIT]; //process table
int lwp_procs = 0; // current # of lwps
int lwp_running; // current process running


/**
 * Creates a new lightweight process which calls the given function with the
 * given argument.  The new process's stack will be `stacksize` words.  The
 * LWP's process table entry will include:
 *    `pid`        a unique integer process id
 *    `stack`      a pointer to the memory region for this thread's stack
 *    `stacksize`  the size of this thread's stack in words
 *    `sp`         this thread's current stack pointer (top of stack)
 *
 * return the lightweight process id of the new thread on success
 *         (-1 if more than LWP_PROC_LIMIT threads already exist)
 *
 * (Function description taken from assignment description)
 */
int new_lwp(lwpfun function, void * argument, size_t stacksize)
{
   size_t stack_size = stacksize * sizeof(int);
   ptr_int_t * stack_pointer;
   ptr_int_t * base_pointer;

   if(lwp_procs >= LWP_PROC_LIMIT) // Limiting number of threads
   {
   	return -1;
   }

   //Set lwp_running and lwp_procs
   lwp_running = lwp_procs; 
   ++ lwp_procs;

   lwp_table[lwp_running].pid = nextPid;
   ++ nextPid;
   lwp_table[lwp_running].stack = malloc(stack_size);
   lwp_table[lwp_running].stacksize = stacksize;

   stack_pointer = lwp_table[lwp_running].stack + stack_size;
   base_pointer = stack_pointer;

	*stack_pointer = (ptr_int_t) argument;
	-- stack_pointer;

	*stack_pointer = (ptr_int_t) lwp_exit;
	-- stack_pointer;   

   *stack_pointer = (ptr_int_t) function;
   --stack_pointer;

	*stack_pointer = 0xDEADBEEF;
	base_pointer = stack_pointer;

	stack_pointer -= 7;
	*stack_pointer = (ptr_int_t) base_pointer;

	lwp_table[lwp_running].sp = stack_pointer;

   return lwp_running;


}

/**
 * Terminates the current LWP, frees its resources, and moves all the others up in the process table.  
 * If there are no other threads, calls lwp_stop();
 */
void lwp_exit()
{
	int i = 0;

	free(lwp_table[lwp_running].stack); // Frees the stack pointer for the particular process

   for(i = lwp_running + 1; i < lwp_procs; ++i) // Shifts all the processes up in the process table
   {
   	lwp_table[i - 1] = lwp_table[i];
   }
   --lwp_procs;

   if(lwp_procs == 0)
   {
   	lwp_stop(); //Stop if we have no more threads
   }
   else // Set new thread to run
   {	
   	if(lwp_scheduler)
   	{
   		lwp_running = lwp_scheduler();
   	}
   	else // Round Robin Scheduling
   	{
   		lwp_running = 0; 
   	}
   	SetSP(lwp_table[lwp_running].sp); //Set stack pointer to new process
   	RESTORE_STATE(); //Run process
   }


}

/**
 * Returns the pid of the calling LWP.  
 * Return value is undefined if not called by a LWP.
 */
int  lwp_getpid()
{
   return lwp_table[lwp_running].pid;
}

/**
 * Yields control to another LWP. 
 * Saves the current LWP's context, picks the next one, restores the thread's context, and returns.
 */
void lwp_yield()
{
   SAVE_STATE(); // Saves context

   GetSP(lwp_table[lwp_running].sp); // Saves stack pointer to current lwp

   /* Swaps lwp running */
   if(lwp_scheduler)
   {
   	lwp_running = lwp_scheduler();
   }
   else //Round Robin Scheduling
   {
   	++ lwp_running;
   	if(lwp_running >= lwp_procs) // reached the end of list of procedures
   	{
   		lwp_running = 0;
   	}
   }

   SetSP(lwp_table[lwp_running].sp);
   RESTORE_STATE();
}

/**
 * Starts the LWP System.
 * Saves the original context and stack pointer, picks an LWP, and starts it. 
 * If there are no LWPs, returns 
 */
void lwp_start()
{
	if(lwp_procs == 0) // If there are no LWPs, returns immediately
	{
		return;
	}

	SAVE_STATE(); //saves context
	GetSP(lwp_StackPointer); //saves Stack Pointer

	if(lwp_scheduler)
	{
		lwp_running = lwp_scheduler();
	}
	else //Round Robin Scheduling
	{
		lwp_running = 0;
	}
	SetSP(lwp_table[lwp_running].sp);
	RESTORE_STATE();
}

/**
 * Stops the LWP System.
 * Restores the stack pointer, and returns to that context. 
 */
void lwp_stop()
{
	SAVE_STATE(); //saves context
	SetSP(lwp_StackPointer); // restores the stack pointer
	RESTORE_STATE(); //returns
}

/* 
 * Causes LWP to use the function scheduler to choose the next process to run.
 */
void lwp_set_scheduler(schedfun sched)
{
	lwp_scheduler = sched;
}
