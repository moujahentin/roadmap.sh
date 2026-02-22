#!/bin/bash

# ---------- colors ----------
GREEN=$'\e[32m'
CYAN=$'\e[36m'
YELLOW=$'\e[33m'
RESET=$'\e[0m'

# Clear to end of current line (prevents leftover chars)
clreol() { tput el; }

# Print one line + clear rest of line
pline() {
  printf "%b" "$1"
  clreol
  printf "\n"
}

# ---------- Banner ----------
banner() {
cat <<'EOF'
 __  __              _       _                _   _
|  \/  | ___  _   _ (_) __ _| |__   ___ _ __ | |_(_)_ __
| |\/| |/ _ \| | | || |/ _` | '_ \ / _ \ '_ \| __| | '_ \
| |  | | (_) | |_| || | (_| | | | |  __/ | | | |_| | | | |
|_|  |_|\___/ \__,_|/ |\__,_|_| |_|\___|_| |_|\__|_|_| |_|
                  |__/
EOF
}


# ---------- cursor handling ----------
tput civis
cleanup() { tput cnorm; printf "\n"; }
trap cleanup EXIT INT TERM

# ---------- CPU (delta from /proc/stat) ----------
prev_total=""
prev_idle=""

cpu_line() {
  # Updates globals prev_total/prev_idle => MUST NOT run in subshell
  read -r cpu user nice system idle iowait irq softirq steal guest guest_nice < /proc/stat
  local total=$((user + nice + system + idle + iowait + irq + softirq + steal))
  local idle_all=$((idle + iowait))

  if [[ -z "$prev_total" ]]; then
    prev_total=$total
    prev_idle=$idle_all
    printf "CPU:  N/A"
    return
  fi

  local dt=$((total - prev_total))
  local di=$((idle_all - prev_idle))

  prev_total=$total
  prev_idle=$idle_all

  if (( dt <= 0 )); then
    printf "CPU:  N/A"
    return
  fi

  local usage=$(( (100 * (dt - di)) / dt ))
  printf "CPU: %3d%% used" "$usage"
}

# ---------- Memory (MemAvailable-based %) ----------
mem_line() {
  local mem_total mem_avail mem_used used_pct free_pct
  mem_total=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)
  mem_avail=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
  mem_used=$((mem_total - mem_avail))

  used_pct=$(( 100 * mem_used / mem_total ))
  free_pct=$(( 100 - used_pct ))

  # show pretty numbers from free -h
  free -h | awk -v up="$used_pct" -v fp="$free_pct" '
    /^Mem:/ {printf "RAM: Used %s (%3d%%) | Free %s (%3d%%) | Total %s", $3, up, $7, fp, $2}'
}

# ---------- Disk ----------
disk_line() {
  df -h / | awk 'NR==2 {printf "DISK(/): Used %s (%s) | Free %s | Total %s", $3, $5, $4, $2}'
}

# ---------- OS (PRETTY_NAME) ----------
os_line() {
  if [[ -r /etc/os-release ]]; then
    . /etc/os-release
    printf "OS: %s" "$PRETTY_NAME"
  else
    printf "OS: Unknown"
  fi
}

# ---------- Uptime ---------#
uptime_line() {
  awk '{printf "Uptime: %d days, %02d:%02d\n", $1/86400, ($1%86400)/3600, ($1%3600)/60}' /proc/uptime
}

# ---------- Top 5 processes (fixed height) ----------
top5_cpu_block() {
  ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6 | awk '
    NR==1 {printf "%-8s %-20s %s\n",$1,$2,$3; next}
          {printf "%-8s %-20s %s\n",$1,$2,$3}
    END{for(i=NR;i<6;i++) print ""}
  '
}

top5_mem_block() {
  ps -eo pid,comm,%mem --sort=-%mem | head -n 6 | awk '
    NR==1 {printf "%-8s %-20s %s\n",$1,$2,$3; next}
          {printf "%-8s %-20s %s\n",$1,$2,$3}
    END{for(i=NR;i<6;i++) print ""}
  '
}

# ---------- main loop ----------
clear
while true; do
  # Go top-left, DO NOT clear full screen -> avoids flicker
  tput cup 0 0

  while IFS= read -r line; do pline "$line"; done < <(banner)


  pline "${YELLOW}$(date '+%Y-%m-%d %H:%M:%S')${RESET}"
  pline ""

  pline "${GREEN}-- Live CPU Usage --${RESET}"
  cpu_line; clreol; printf "\n"     # IMPORTANT: no $(cpu_line)
  pline ""

  pline "${GREEN}-- Live Memory Usage --${RESET}"
  pline "$(mem_line)"
  pline ""

  pline "${GREEN}-- Disk Usage (/) --${RESET}"
  pline "$(disk_line)"
  pline ""

  pline "${GREEN}-- Top 5 Processes by CPU --${RESET}"
  while IFS= read -r line; do pline "$line"; done < <(top5_cpu_block)
  pline ""

  pline "${GREEN}-- Top 5 Processes by Memory --${RESET}"
  while IFS= read -r line; do pline "$line"; done < <(top5_mem_block)
  pline ""

  pline "${GREEN}-- Operation System --${RESET}"
  pline "$(os_line)"
  pline "$(uptime_line)"
  pline ""

  pline "${CYAN}Press Q to exit${RESET}"

  # park cursor at bottom (optional)
  rows=$(tput lines)
  tput cup $((rows-1)) 0

  read -t 1 -n 1 key
  if [[ "${key,,}" == "q" ]]; then
    clear
    break
  fi
done
