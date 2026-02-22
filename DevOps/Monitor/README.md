# Server Stats (DevOps Roadmap Project)

A Bash script that analyzes basic Linux server performance stats (CPU, memory, disk, and top processes).  
Built as part of the roadmap.sh DevOps roadmap project: **Server Performance Stats**.

Project URL:https://roadmap.sh/projects/server-stats

## ✅ Features
- Total CPU usage
- Total memory usage (used/free + %)
- Total disk usage (used/free + %)
- Top 5 processes by CPU
- Top 5 processes by memory
- OS version + uptime (stretch goals)

## ▶️ Usage
```bash
chmod +x server-stats.sh
./server-stats.sh
```

🛠️ How it works (high level)

CPU usage is calculated from /proc/stat deltas

Memory stats use MemAvailable from /proc/meminfo

Disk stats use df

Top processes use ps
