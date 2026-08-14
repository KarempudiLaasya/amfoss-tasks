package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Process struct {
	ID         string
	Arrival    int
	Burst      int
	Remaining  int
	Start      int
	Completion int
	Waiting    int
	Turnaround int
}

type Segment struct {
	ID    string
	Start int
	End   int
}

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("==========================================")
	fmt.Println("     GRAND LINE CPU SCHEDULING SIMULATOR")
	fmt.Println("==========================================")

	fmt.Print("Enter number of crews/processes: ")
	n := readInt(reader)

	processes := make([]Process, n)

	for i := 0; i < n; i++ {
		fmt.Printf("\nCrew %d\n", i+1)

		fmt.Print("Process ID: ")
		id := readString(reader)

		fmt.Print("Arrival Time: ")
		arrival := readInt(reader)

		fmt.Print("Burst Time: ")
		burst := readInt(reader)

		processes[i] = Process{
			ID:        id,
			Arrival:   arrival,
			Burst:     burst,
			Remaining: burst,
			Start:     -1,
		}
	}

	fmt.Println("\nSelect Scheduling Algorithm:")
	fmt.Println("1. First Come First Serve (FCFS)")
	fmt.Println("2. Shortest Job First (SJF - Non-Preemptive)")
	fmt.Println("3. Round Robin (RR)")
	fmt.Print("Enter choice: ")

	choice := readInt(reader)

	var segments []Segment
	var quantum int

	switch choice {
	case 1:
		processes, segments = fcfs(processes)

	case 2:
		processes, segments = sjf(processes)

	case 3:
		fmt.Print("Enter Time Quantum: ")
		quantum = readInt(reader)

		if quantum <= 0 {
			fmt.Println("Time Quantum must be greater than 0.")
			return
		}

		processes, segments = roundRobin(processes, quantum)

	default:
		fmt.Println("Invalid choice.")
		return
	}

	displayGanttChart(segments)
	displayResults(processes)
}

func readInt(reader *bufio.Reader) int {
	for {
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)

		value, err := strconv.Atoi(input)
		if err == nil && value >= 0 {
			return value
		}

		fmt.Print("Enter a valid non-negative integer: ")
	}
}

func readString(reader *bufio.Reader) string {
	for {
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)

		if input != "" {
			return input
		}

		fmt.Print("Enter a valid Process ID: ")
	}
}

// ---------------------------------------------------------
// FCFS
// ---------------------------------------------------------

func fcfs(processes []Process) ([]Process, []Segment) {
	sort.Slice(processes, func(i, j int) bool {
		if processes[i].Arrival == processes[j].Arrival {
			return processes[i].ID < processes[j].ID
		}
		return processes[i].Arrival < processes[j].Arrival
	})

	currentTime := 0
	var segments []Segment

	for i := range processes {
		if currentTime < processes[i].Arrival {
			currentTime = processes[i].Arrival
		}

		processes[i].Start = currentTime

		currentTime += processes[i].Burst

		processes[i].Completion = currentTime
		processes[i].Turnaround =
			processes[i].Completion - processes[i].Arrival

		processes[i].Waiting =
			processes[i].Turnaround - processes[i].Burst

		addSegment(&segments, processes[i].ID, processes[i].Start, currentTime)
	}

	return processes, segments
}

// ---------------------------------------------------------
// SJF - Non Preemptive
// ---------------------------------------------------------

func sjf(processes []Process) ([]Process, []Segment) {
	n := len(processes)
	currentTime := 0
	completed := 0
	visited := make([]bool, n)

	var segments []Segment

	for completed < n {
		index := -1

		for i := 0; i < n; i++ {
			if !visited[i] && processes[i].Arrival <= currentTime {
				if index == -1 ||
					processes[i].Burst < processes[index].Burst ||
					(processes[i].Burst == processes[index].Burst &&
						processes[i].Arrival < processes[index].Arrival) {
					index = i
				}
			}
		}

		// CPU is idle until the next process arrives.
		if index == -1 {
			nextArrival := -1

			for i := 0; i < n; i++ {
				if !visited[i] {
					if nextArrival == -1 ||
						processes[i].Arrival < nextArrival {
						nextArrival = processes[i].Arrival
					}
				}
			}

			currentTime = nextArrival
			continue
		}

		processes[index].Start = currentTime
		currentTime += processes[index].Burst
		processes[index].Completion = currentTime

		processes[index].Turnaround =
			processes[index].Completion - processes[index].Arrival

		processes[index].Waiting =
			processes[index].Turnaround - processes[index].Burst

		visited[index] = true
		completed++

		addSegment(
			&segments,
			processes[index].ID,
			processes[index].Start,
			currentTime,
		)
	}

	return processes, segments
}

// ---------------------------------------------------------
// Round Robin
// ---------------------------------------------------------

func roundRobin(processes []Process, quantum int) ([]Process, []Segment) {
	sort.Slice(processes, func(i, j int) bool {
		if processes[i].Arrival == processes[j].Arrival {
			return processes[i].ID < processes[j].ID
		}
		return processes[i].Arrival < processes[j].Arrival
	})

	n := len(processes)
	currentTime := 0
	completed := 0
	nextProcess := 0

	queue := []int{}
	inQueue := make([]bool, n)

	var segments []Segment

	for completed < n {

		// If queue is empty, move time to next arriving process.
		if len(queue) == 0 {
			if nextProcess < n && currentTime < processes[nextProcess].Arrival {
				currentTime = processes[nextProcess].Arrival
			}

			for nextProcess < n &&
				processes[nextProcess].Arrival <= currentTime {

				queue = append(queue, nextProcess)
				inQueue[nextProcess] = true
				nextProcess++
			}
		}

		if len(queue) == 0 {
			continue
		}

		index := queue[0]
		queue = queue[1:]
		inQueue[index] = false

		if processes[index].Start == -1 {
			processes[index].Start = currentTime
		}

		executionTime := quantum

		if processes[index].Remaining < executionTime {
			executionTime = processes[index].Remaining
		}

		start := currentTime
		currentTime += executionTime
		processes[index].Remaining -= executionTime

		addSegment(
			&segments,
			processes[index].ID,
			start,
			currentTime,
		)

		// Add newly arrived processes.
		for nextProcess < n &&
			processes[nextProcess].Arrival <= currentTime {

			if !inQueue[nextProcess] &&
				processes[nextProcess].Remaining > 0 {

				queue = append(queue, nextProcess)
				inQueue[nextProcess] = true
			}

			nextProcess++
		}

		if processes[index].Remaining > 0 {
			queue = append(queue, index)
			inQueue[index] = true
		} else {
			processes[index].Completion = currentTime

			processes[index].Turnaround =
				processes[index].Completion - processes[index].Arrival

			processes[index].Waiting =
				processes[index].Turnaround - processes[index].Burst

			completed++
		}
	}

	return processes, segments
}

// ---------------------------------------------------------
// Gantt Chart Helpers
// ---------------------------------------------------------

func addSegment(segments *[]Segment, id string, start, end int) {
	// Merge consecutive executions of the same process.
	if len(*segments) > 0 {
		last := &(*segments)[len(*segments)-1]

		if last.ID == id && last.End == start {
			last.End = end
			return
		}
	}

	*segments = append(*segments, Segment{
		ID:    id,
		Start: start,
		End:   end,
	})
}

func displayGanttChart(segments []Segment) {
	fmt.Println("\n================ GANTT CHART ================")

	if len(segments) == 0 {
		return
	}

	fmt.Print("|")

	for _, segment := range segments {
		fmt.Printf("  %s  |", segment.ID)
	}

	fmt.Println()

	fmt.Printf("%d", segments[0].Start)

	for _, segment := range segments {
		fmt.Printf("%8d", segment.End)
	}

	fmt.Println("\n==============================================")
}

// ---------------------------------------------------------
// Results
// ---------------------------------------------------------

func displayResults(processes []Process) {
	var totalWaiting int
	var totalTurnaround int

	fmt.Println("\n================ RESULTS =====================")
	fmt.Printf("%-10s %-10s %-10s %-12s %-12s %-12s\n",
		"Process",
		"Arrival",
		"Burst",
		"Completion",
		"Waiting",
		"Turnaround",
	)

	fmt.Println(strings.Repeat("-", 70))

	// Display processes by Process ID order.
	display := make([]Process, len(processes))
	copy(display, processes)

	sort.Slice(display, func(i, j int) bool {
		return display[i].ID < display[j].ID
	})

	for _, p := range display {
		fmt.Printf("%-10s %-10d %-10d %-12d %-12d %-12d\n",
			p.ID,
			p.Arrival,
			p.Burst,
			p.Completion,
			p.Waiting,
			p.Turnaround,
		)

		totalWaiting += p.Waiting
		totalTurnaround += p.Turnaround
	}

	n := float64(len(processes))

	fmt.Println(strings.Repeat("-", 70))
	fmt.Printf("Average Waiting Time    : %.2f\n",
		float64(totalWaiting)/n)

	fmt.Printf("Average Turnaround Time : %.2f\n",
		float64(totalTurnaround)/n)

	fmt.Println("==============================================")
}
