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

now = datetime.now()
last_visit = {
    "Hawai'i": now - timedelta(days=12),
    "Tahiti": now - timedelta(days=20),
    "Samoa": now - timedelta(days=5),
    "Fiji": now - timedelta(days=30),
}

# Priority score
def skill_priority(island):
    days_since = (datetime.now() - last_visit[island]).days
    return populations[island] * days_since

# Greedy Algorithm Route 
def full_route_with_revisits(start, time_budget):
    curr = start
    route = [curr]
    time_used = 0
    total_score = 0
    exp_index = defaultdict(int)
    teaching_log = defaultdict(list)

    while time_used < time_budget:
        if exp_index[curr] < len(exp[curr]):
            e_time = exp[curr][exp_index[curr]]
            if time_used + e_time <= time_budget:
                time_used += e_time
                score = skill_priority(curr)
                total_score += score
                teaching_log[curr].append((e_time, score))
                exp_index[curr] += 1
                continue

        next_options = sorted(G[curr], key=lambda x: skill_priority(x[0]), reverse=True)
        moved = False
        for neighbor, travel_time in next_options:
            if time_used + travel_time <= time_budget:
                route.append(neighbor)
                time_used += travel_time
                curr = neighbor
                moved = True
                break
        if not moved:
            break

    return route, time_used, total_score, teaching_log

# Test
start = "Hawai'i"
TIME_BUDGET = 20

route, total_time, priority_score, teaching_log = full_route_with_revisits(start, TIME_BUDGET)

print("Route taken:")
print(" → ".join(route))
print(f"\nTotal time used: {total_time:.2f} hours")
print(f"Total priority score: {priority_score}\n")
# Expected output 
# Route taken: 
# Hawaii → Tahiti → Fiji → Samoa 
# Total time used: 19.25 hours
# Total priority score: 187800