# cpu scheduling simulator

## features

- fcfs
- sjf
- rr
- process id, arrival time and burst time input
- time quantum input for round robin
- terminal gantt chart
- waiting time
- turnaround time
- average waiting time
- average turnaround time

## algorithms

### fcfs

first come first serve means processes are executed in the order they arrive

### sjf - non-preemptive

among the processes that have arrived, we select the one with shortest burst time.  
non-preemptive means once a process starts it runs until completion

### round robin

Each process gets a fixed amount of CPU time called the Time Quantum. If a process is not finished, it goes back to the end of the ready queue.

## approach

Each process is represented using a Go struct containing its ID, arrival time,burst time and scheduling results.A slice is used to store all processes. The simulator maintains a currentTime variable to represent the CPU clock.

## formulas

Turnaround Time = Completion Time - Arrival Time  
Waiting Time = Turnaround Time - Burst Time  
Average Waiting Time = Total Waiting Time / Number of Processes  
Average Turnaround Time = Total Turnaround Time / Number of Processes

## resouces used

- Go documentation: https://go.dev/doc/
- Go package documentation: fmt, bufio, and sort
- General references on CPU scheduling algorithms

## new concepts learned

Go structs,slices,loops,condtions,cpu scheduling,simulating a cpu clock,implementing a queue
