"""
Pomodoro Timer - Command Line (Windows-friendly)
Usage examples:
  py pomodoro.py
  py pomodoro.py -w 30 -s 5 -l 15 -c 6
  py pomodoro.py --no-beep
"""
import argparse
import datetime as dt
import sys
import time
import os

def beep(times=2, no_beep=False):
    if no_beep:
        return
    try:
        import winsound 
        for _ in range(times):
            winsound.Beep(880, 300)
            time.sleep(0.1)
            winsound.Beep(660, 300)
    except Exception:
        for _ in range(times):
            print('\a', end='', flush=True)
            time.sleep(0.3)

def log_event(phase, minutes):
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pomodoro_log.csv")
    except NameError:
        path = "pomodoro_log.csv"
    line = f"{dt.datetime.now().isoformat(timespec='seconds')},{phase},{minutes}\n"
    try:
        new_file = not os.path.exists(path)
        with open(path, "a", encoding="utf-8") as f:
            if new_file:
                f.write("timestamp,phase,minutes\n")
            f.write(line)
    except Exception:
        pass 

def fmt_mmss(seconds: int) -> str:
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"

def countdown(total_seconds: int, label: str):
    start = time.time()
    try:
        for remaining in range(total_seconds, -1, -1)
            bar_len = 28
            done = int(bar_len * (total_seconds - remaining) / max(total_seconds, 1))
            bar = "█" * done + "-" * (bar_len - done)
            print(f"\r{label} |{bar}| {fmt_mmss(remaining)} remaining", end="", flush=True)
            time.sleep(1)
        print()  
    except KeyboardInterrupt:
        print("\n  Stopped by user.")
        raise

def run(work: int, short: int, long: int, cycles: int, no_beep: bool):
    print(" Pomodoro Timer")
    print(f"Work: {work}m | Short break: {short}m | Long break: {long}m | Cycles: {cycles}")
    try:
        for i in range(1, cycles + 1):
            print(f"\n  Pomodoro {i}/{cycles}")
            countdown(work * 60, "Work     ")
            log_event("work", work)
            beep(no_beep=no_beep)
            if i == cycles:
                break
            if i % 4 == 0:
                print(" Long break")
                countdown(long * 60, "LongBreak")
                log_event("long_break", long)
                beep(no_beep=no_beep)
            else:
                print("Short break")
                countdown(short * 60, "ShortBrk ")
                log_event("short_break", short)
                beep(no_beep=no_beep)
        print("\n All cycles complete. Great job!")
        beep(times=3, no_beep=no_beep)
    except KeyboardInterrupt:
        print("Session ended early. Progress saved to pomodoro_log.csv (if writable).")

def main():
    parser = argparse.ArgumentParser(description="Command-line Pomodoro timer")
    parser.add_argument("-w", "--work", type=int, default=25, help="work minutes (default: 25)")
    parser.add_argument("-s", "--short", type=int, default=5, help="short break minutes (default: 5)")
    parser.add_argument("-l", "--long", type=int, default=15, help="long break minutes (default: 15)")
    parser.add_argument("-c", "--cycles", type=int, default=4, help="number of pomodoro cycles (default: 4)")
    parser.add_argument("--no-beep", action="store_true", help="disable sound beeps")
    args = parser.parse_args()
    if min(args.work, args.short, args.long, args.cycles) < 0:
        print("Durations and cycles must be non-negative integers.", file=sys.stderr)
        sys.exit(1)
    run(args.work, args.short, args.long, args.cycles, args.no_beep)

if __name__ == "__main__":
    main()
