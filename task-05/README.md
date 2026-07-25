In this task, we were supposed to build a terminal-based system monitoring tool that constantly keeps track of the running processes in the system.

It should keep track of:

- Process ID (PID)
- Process Name
- CPU Usage
- Memory Usage
- Total Active Process Count

While learning about the topic, I found that most of the required information is available in the `/proc` directory as plain text.

I found this resource really useful for understanding what I was dealing with and where I could get all the information I needed:

[https://www.tecmint.com/exploring-proc-file-system-in-linux/](https://www.tecmint.com/exploring-proc-file-system-in-linux/)

The required information was available in the following locations:

- Process ID: `/proc` (count the number of process ID directories in `/proc` to get the total active process count)
- Process Name: `/proc/[pid]/stat`
- Process CPU Ticks: `/proc/[pid]/stat`
- Total CPU Ticks: `/proc/stat`
- Memory Usage: `/proc/[pid]/status`

I then started coding the Python program to get all the required data from the `/proc` directory. The process IDs were simply present as directory names. I used the `pathlib` module to get the names of all the directories whose names consisted only of digits.

Then I made the function for getting the total process count.

After that, I made the `get_pname()` function. I read `/proc/[pid]/stat` to get the process name, which is stored inside parentheses.

Next, I made the `get_cpu_ticks()` function and the `get_cpu_usage()` function. The `get_cpu_ticks()` function initially got the CPU ticks for a particular process from `/proc/[pid]/stat` and the total CPU ticks from `/proc/stat`. My initial idea was to record both values, wait for a few milliseconds using `time.sleep()`, and then calculate the CPU usage percentage.

However, this caused a major issue. Everything took a long time to load, and the interface later became very laggy. I then removed the `get_cpu_usage()` function and modified `get_cpu_ticks()` so that it simply returns all the CPU ticks stored in a dictionary with their respective PIDs. Inside the main loop, I keep track of the previous and current snapshots of CPU ticks and calculate the CPU usage percentage by comparing the differences between them. This removed the delay and made the interface much smoother.

Finally, I built the `get_memory_usage()` function, which reads `/proc/[pid]/status` and extracts the `VmRSS` value, which represents the memory currently being used by the process.

While i was looking for ways to calculate the total cpu usage percentage i came across the psutil module which has functions that calculate total cpu usage and ram usage.

https://www.geeksforgeeks.org/python/how-to-get-current-cpu-and-ram-usage-in-python/

Then i started learning the curses module in python. I watch a youtube course which introduced me to all the main functions for creating terminal ui.

https://youtu.be/VzhZ1nTeAsA?si=fh4Z3D2ObnPHUGJr

New functions i learned:

`curses.curs_set(0)`: Hides the terminal cursor.
`stdscr.getmaxyx()`: Gets the current terminal height and width.
`curses.newwin()`: Creates a new window for the UI.
`curses.newpad()`: Creates a scrollable pad larger than the terminal.
`window.clear()`: Clears the contents of the window.
`pad.clear()`: Clears the contents of the pad.
`window.border()`: Draws a border around the window.
`window.addstr()`: Prints text at a specified position in the window.
`pad.addstr()`: Prints text inside the pad.
`window.refresh()`: Refreshes the window on the screen.
`pad.refresh()`: Displays a selected portion of the pad (used for scrolling).
`window.keypad(True)`: Enables special keyboard keys like arrow keys.
`window.getch()`: Reads keyboard input from the user.
`curses.KEY_UP`: Detects the Up Arrow key.
`curses.KEY_DOWN`: Detects the Down Arrow key.
`curses.A_BOLD`:Displays text in bold.
`curses.wrapper(main)`: Initializes and restores the terminal automatically.

These are some other resources that i referred:
- https://docs.python.org/3/howto/curses.html
- https://medium.com/@mike-dresser/curses-and-other-dirty-words-996a24df7c1f
- https://docs.python.org/3/library/pathlib.html
