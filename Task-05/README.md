# Grand Line Guardian

this project is a terminal-based process monitor written in Python. The idea is similar to `htop`, where we can see what processes are running and how much CPU and memory they are using.

## Features

The program displays the PID, process name, CPU usage, memory usage, and the total number of active processes. The information keeps updating every 0.5 seconds.

## Approach

I used Linux's `/proc` virtual filesystem to get the process information.Then i went through the entries in `/proc` and picked the ones with numeric names since they represent process IDs. For each process, `/proc/<PID>/comm` gives the process name, `/proc/<PID>/status` gives information about the process including VmRSS for memory usage, and `/proc/<PID>/stat` gives the CPU time information. `/proc/stat` is used to get the total CPU time of the system.

For CPU usage, I took two readings 0.5 seconds apart. I find how much the CPU time of a process increased and compare it with how much the total CPU time increased during the same interval. This gives the CPU usage percentage.

The information of each process is stored as a tuple inside a list. The terminal is then cleared before every update so that the old output does not keep piling up.

## Technologies Used

I used Python 3 and the Linux `/proc` filesystem. The program only uses Python's built-in `os` and `time` modules, so there are no external dependencies.

## Resources Used

I used the Linux `proc(5)` and `proc_pid_stat(5)` documentation and the Python documentation. I also explored the `/proc` filesystem directly in my Linux VM while working on the project.

## Concepts Learned

Through this task,i learned how Linux processes and PIDs work, how the `/proc` virtual filesystem provides process information, how CPU usage can be calculated from CPU-time differences, how `VmRSS` is used to get memory usage, and how a basic real-time process monitor works.

## Project Structure

The project contains `src/main.py` for the main program, `requirements.txt` for dependencies,and `README.md` for the documentation.

## Running the Application

The programme was run on Linux because it uses the `/proc` filesystem. used following command to run 
it

```bash
python3 src/main.py
