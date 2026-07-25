from pathlib import Path
from curses import wrapper
import curses
import psutil


def get_all_pids():
    dir_path = Path("/proc")
    pids = []
    for x in dir_path.iterdir():
        if x.is_dir() and x.name.isdigit():
            pids.append(x.name)

    return pids
            
            
def get_total_process_count():
    dir_path = Path("/proc")
    count = 0
    try:
        for x in dir_path.iterdir():
            if x.is_dir() and x.name.isdigit():
                count += 1
        return count
    except(FileNotFoundError, PermissionError):
        return count

    
def get_pname(pid):
    try:
        with open(f"/proc/{pid}/stat",'r') as f:
            stat = f.read()
            name_start = stat.find('(')
            name_end = stat.rfind(')')
            pname = stat[name_start+1:name_end]
            return pname
    except(FileNotFoundError,ProcessLookupError,IndexError):
            return None

def get_cpu_ticks():
    try:
        process_ticks_dict = {}
        with open(f"/proc/stat") as f:
            stat_line = f.readline()

        system_ticks = stat_line.split()[1:]
        total_ticks = sum(map(int,system_ticks))

        pids = get_all_pids()
        for pid in pids:
            try:
                with open(f"/proc/{pid}/stat",'r') as g:
                    stat_content = g.read()

                bracket_end = stat_content.rfind(')')
                fields_after_name = stat_content[bracket_end+2:].split()
                utime = int(fields_after_name[11]) 
                stime = int(fields_after_name[12]) 
                process_ticks = utime + stime
                process_ticks_dict[pid] = process_ticks
            except (FileNotFoundError, ProcessLookupError, IndexError):
                continue

        return process_ticks_dict, total_ticks
    except(FileNotFoundError,ProcessLookupError,IndexError):
        return None



def get_memory_usage(pid):
    try:
        with open(f"/proc/{pid}/status", 'r') as f:
            data = f.readlines()
            memory_usage = "0"
        for line in data:
            if line.startswith("VmRSS:"):
                memory_data = line.split()
                memory_usage = memory_data[1]
                break
        return int(memory_usage)
    except(FileNotFoundError, ProcessLookupError):
        return 






def main(stdscr):
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()
    window = curses.newwin(height - 2, width - 2, 1, 1)
    pad = curses.newpad(1000, 200)
    window.keypad(True)
    scroll = 0
    previous_ticks, previous_total = get_cpu_ticks()
    cpu = {}
    while True:
        current_ticks, current_total = get_cpu_ticks()

        wheight, wwidth = stdscr.getmaxyx()
        window.clear()
        window.border()
        pad.clear()

        cpu_usage = psutil.cpu_percent(None)
        ram = psutil.virtual_memory()

        memory_percent = ram.percent
        memory_used = ram.used / (1024 ** 3)
        memory_total = ram.total / (1024 ** 3)
        window.addstr(2,5, f"CPU Usage (%): {cpu_usage}%")
        window.addstr(3,5, f"Ram Usage : {round(memory_used,3)} / {round(memory_total,3)} ({memory_percent})%")
        
        window.addstr(3,wwidth*4//5, f"Total Archive Processes: {get_total_process_count()}")
        
        window.addstr(0, wwidth//2 - 16, "Grand Line Guardian",curses.A_BOLD)
        window.addstr(5, wwidth//5 , "PID")
        window.addstr(5, wwidth*2//5,"Pname")
        window.addstr(5, wwidth*3//5 ,"CPU%")
        window.addstr(5, wwidth*4//5 ,"Memory")

        pids = get_all_pids()

        count = 3
        total_ticks_diff = current_total - previous_total
        if total_ticks_diff > 0:
            cpu.clear()

            for pid in current_ticks:
                if pid in previous_ticks:
                    process_diff = current_ticks[pid] - previous_ticks[pid]
                    cpu[pid] = (process_diff/ total_ticks_diff) * 100
        for pid in pids:
            
            name = get_pname(pid)
            
            memory = get_memory_usage(pid)

            if name is None:
                continue

            pad.addstr(count, wwidth//5, pid)
            pad.addstr(count, wwidth*2//5, name[:25])
            pad.addstr(count, wwidth*3//5, f"{round(cpu.get(pid,0.0),2)}%" if cpu is not None else "N/A")
            pad.addstr(count, wwidth*4//5, f"{memory} kB" if memory is not None else "N/A")

            count += 1


        previous_ticks = current_ticks
        previous_total = current_total    
        window.refresh()
        pad.refresh(scroll, 0,7,1,wheight - 4,wwidth - 3)

        key = window.getch()

        if key == curses.KEY_DOWN:
            scroll += 1

        elif key == curses.KEY_UP:
            scroll = max(0, scroll - 1)

        elif key == ord('q'):
            break

curses.wrapper(main)