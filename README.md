# File Integrity Monitor (FIM) - John Yang

This is a Python script that functions as a File Integrity Monitoring (FIM) system that detects unauthorized changes to monitored files by calculating the hashes of files and checking if it changes over time. If changed, the file and event are logged for further security analysis.

## Table of Contents

1. [Intentions Behind the Project](#intentions-behind-the-project)
2. [Features](#features)
3. [How It Works](#how-it-works)
4. [Customizing Monitored Files](#customizing-monitored-files)
5. [How to Run](#how-to-run)
6. [Log Output](#log-output)
7. [Cybersecurity Insights](#cybersecurity-insights)
8. [Contact](#contact)

## Intentions Behind the Project

When I started studying basic cybersecurity concepts, especially through my CompTIA Security+ exam prep, I noticed that many host intrusion-detection systems revolve around a simple idea. They would store a trusted hash, then keep checking for changes to verify integrity. I wanted to build something from scratch that reflected this concept with my security and coding knowledge.

## Features

| Capability | Details |
|------------|---------|
| Integrity checks | Re-computes SHA-256 every 5 seconds and compares to the baseline. |
| Human-readable logging | Appends timestamps and file paths to `logs/file_changes.log`. |
| Automatic log reset | Log file is truncated at launch so each session starts clean. |
| Pathlib-powered portability | Works on Windows, macOS, Linux without edits. |
| Smooth termination by Ctrl+C | Catches `KeyboardInterrupt` to avoid an unhandled traceback. |

## How It Works

1. Log reset/creation – At startup the script clears (or creates) `logs/file_changes.log`, so each run begins with a clean slate.  
2. SHA-256 hashing – Every file listed in `monitoring_list` is read and hashed with SHA-256. If the file hasn’t been seen before in the current session, its hash is stored as the original.  
3. Integrity monitoring, Change detection – On subsequent cycles the script re-hashes each file and compares the new value to the original.  
   * If the hash is different, the script prints a message, appends a timestamped line to the log, and updates the original to the new hash.  
   * If the hash is identical, no output is produced (the file is unchanged).  
4. Checking interval – The loop pauses for five seconds (adjustable by changing `time.sleep(5)`) before repeating the process.  
5. Terminate the script – Press Ctrl+C at any time; the `KeyboardInterrupt` is caught so the program terminates without an ugly traceback.

## Customizing Monitored Files

1. Open `fim.py`.
2. Edit the `monitoring_list`(absolute paths work as well):
    * EX:

    ```python
   monitoring_list = [BASE_DIR / "monitored_file.txt", BASE_DIR / "docs" / "Example1.txt", Path("/var/www/html/index.php")]
   ```

3. Save and rerun the script. New files will automatically receive an original hash that will be stored the first time they are seen.

## How to Run

Follow these steps to launch the File-Integrity Monitor on any machine that has Python 3.8 or later.

1. Clone the repository or download the ZIP.

2. Verify the monitored files list (see above).

3. Launch a terminal in the folder /File Integrity Monitor.

4. Run python fim.py.

5. When the script starts running, the output should look something like this: ![alt text](FIM1.jpg)

6. Stop the monitor by pressing Ctrl+C. The script will register the interrupt and terminate.

7. Look inside logs/file_changes.log to review records of every change detected during the session.

## Log Output

![alt text](FIM2.jpg)

Each line records a timestamp and an absolute path, making the log easy to forward into a SIEM or parse with Splunk or an ELK stack.

## Cybersecurity Insights

* This project allowed me to firsthandedly see the importance of choosing the appropriate hashing algorithm. Going from MD5/SHA-1 to SHA-256 prevents realistic collision attacks and aligns with modern compliance guideilnes.
* Even the smallest details have tangible tradeoffs associated with them. In this case, it was detection speed vs. resource cost. Experimenting with various checking intervals (1s-60s) showed how shorter intervals reduce attacker dwell time but raise CPU usage, ultimately guiding my choice to reach a reasonable balance at a 5s default interval.
* There is a lot to think about in security. This FIM script reliably flags changes on disk but of course misses other areas such as in-memory attacks completely, reaffirming the need for layered defenses and a multifaceted approach to security.

## Contact

Email: <johnyang4406@gmail.com>, <john_s_yang@brown.edu>

LinkedIn: <https://www.linkedin.com/in/john-yang-747726292/>

