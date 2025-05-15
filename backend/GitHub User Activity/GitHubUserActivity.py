import sys
import json
import urllib.request
import urllib.error

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            events = json.loads(data)
            return events
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Error: User not found.")
        else:
            print(f"HTTP Error: {e.code}")
    except urllib.error.URLError:
        print("Error: Unable to reach GitHub API.")
    return []

def parse_activity(events):
    activity_log = []
    for event in events[:5]:  # Limit to 5 recent activities
        event_type = event["type"]
        repo_name = event["repo"]["name"]
        if event_type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            activity_log.append(f"Pushed {commit_count} commits to {repo_name}")
        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            activity_log.append(f"{action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            activity_log.append(f"Starred {repo_name}")
        elif event_type == "ForkEvent":
            activity_log.append(f"Forked {repo_name}")
        else:
            activity_log.append(f"Performed {event_type} on {repo_name}")
    return activity_log

def main():
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    events = fetch_github_activity(username)
    if events:
        activity_log = parse_activity(events)
        print("\nRecent Activity:")
        for activity in activity_log:
            print(f"- {activity}")
    else:
        print("No recent activity found.")

if __name__ == "__main__":
    main()
