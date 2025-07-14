from collections import defaultdict
from datetime import datetime, timedelta

# Below information is just an example case
G = defaultdict(list)
G["Hawai'i"].append(("Tahiti", 7))
G["Tahiti"].append(("Hawai'i", 7))
G["Tahiti"].append(("Samoa", 6))
G["Samoa"].append(("Tahiti", 6))
G["Tahiti"].append(("Fiji", 4))
G["Fiji"].append(("Tahiti", 4))
G["Samoa"].append(("Fiji", 2.5))
G["Fiji"].append(("Samoa", 2.5))

exp = {
    "Hawai'i": [1.0, 0.75],
    "Tahiti": [1.5],
    "Samoa": [0.5, 1.0],
    "Fiji": [0.75, 0.75, 0.5],
}

populations = {
    "Hawai'i": 1200,
    "Tahiti": 1000,
    "Samoa": 800,
    "Fiji": 1500,
}

last_visit = {
    "Hawai'i": datetime.now() - timedelta(days=12),
    "Tahiti": datetime.now() - timedelta(days=20),
    "Samoa": datetime.now() - timedelta(days=5),
    "Fiji": datetime.now() - timedelta(days=30),
}

# Priority score 
def skill_priority(island):
    days_since = (datetime.now() - last_visit[island]).days
    return populations[island] * days_since

# DFS route finder 
def prioritized_leader_route(start, time_budget):
    best_route = []
    best_score = -1
    best_time = float('inf')

    def dfs(curr, visited, curr_time, priority_score, route):
        nonlocal best_route, best_score, best_time

        for e_time in sorted(exp[curr]):
            if curr_time + e_time <= time_budget:
                curr_time += e_time

        priority_score += skill_priority(curr)

        if priority_score > best_score or (priority_score == best_score and curr_time < best_time):
            best_route = route[:]
            best_score = priority_score
            best_time = curr_time

        for neighbor, travel_time in G[curr]:
            if neighbor not in visited and curr_time + travel_time <= time_budget:
                visited.add(neighbor)
                dfs(neighbor, visited, curr_time + travel_time, priority_score, route + [neighbor])
                visited.remove(neighbor)

    dfs(start, set([start]), 0, 0, [start])
    return best_route, best_time, best_score

# Test
start = "Hawai'i"
TIME_BUDGET = 30

leader_route, total_time, priority_score = prioritized_leader_route(start, TIME_BUDGET)

print("Route:", " → ".join(leader_route))
print(f"Total time used: {total_time:.2f} hours")
print("Total priority score:", priority_score)

# Expected output 
# Route: Hawaii → Tahiti → Fiji → Samoa 
# Total time used: 20.25 hours
# Total priority score: 83400