# --- Scenario 4: Implementation ---
#   Importing "heapq" for an efficient priority queue (which is used in Dijkstra's algorithm)
#   and "defaultdict" to simplify graph and experience data structures initialization.

import heapq
from collections import defaultdict

# --- Graph + Data Setup (before the function) ---
#   This sets up the graph of islands.
#   It's a directed, weighted graph—-meaning the travel time from A to B might be different from B to A.

#   G[u]  = list of (v, travel_time) edges out of island u
#   Alternative version: G[islands] = list of (neighboring island, travel time)
#   G[u] gives us all the islands reachable from u, and the time it takes to get there.
G = defaultdict(list)
#   format: G["island"].append(("neighboring-island", 7.7)) 

#   exp[u] = list of experience times on island u   (can be 1+ per island)
#   The durations (e.g., 1.0, 0.5, 2.0) represent the time it takes to complete each experience on that island.
#   exp[u] is the list of activities/experiences the tourist can do when they visit island u.
exp = defaultdict(list)
#   format: exp["island"] = [1.0, 0.5, 2.0]

#   start = starting island for the tourist
#   This can be changed to any desired starting island.
start = "Hawaiʻi"

#   This represent the maximum total time the tourist is allowed to spend on their trip
#   including both travel and experience time.
#   When set to None, it means there is no time limit.
TIME_BUDGET = None

# --- Dijkstra: shortest paths (aka travel times) ---
def shortest_paths(source):
    """Return dict: island → min travel time from `source`."""
    dist = {source: 0}  # Starting island takes 0 time to reach (because we're already there).
    pq = [(0, source)]  # Priority queue to explore islands in order of least time taken to reach them.

    while pq:   # Keep exploring until we've checked all reachable islands.
        t, u = heapq.heappop(pq)    # Get the island u with the least travel time t to reach.
        if t > dist[u]:
            continue
        for v, w in G[u]:   # Look at each neighbor v of island u, with travel time w.
            if (nv := t + w) < dist.get(v, float('inf')):   # Calculate the new travel time to get to v by going through u.
                # If this new time is better than any previously found time to v, update it.
                dist[v] = nv
                heapq.heappush(pq, (nv, v))
    return dist


# --- Greedy: building the tourist's route ---
def best_itinerary(start, time_budget=None):
    """Return (route, total_time, total_experiences)."""
    visited = set([start])  # Mark the starting island as visited.
    route   = [start]   # Add it to the route list.

    # Initialize total travel and experience time.
    # Since we're already on the starting island, we "do" all experiences there right away.
    total_time = 0.0
    total_exp  = len(exp[start])
    total_time += sum(exp[start])

    # While there's still a good island to visit...
    while True:
        # Recalculate the shortest travel times from the current island to all others.
        dist = shortest_paths(route[-1])

        # To pick the "best next island" based on experience per time cost.
        best_isle = None
        best_ratio = -1

        # Skip any islands we've already visited.
        for isle, experiences in exp.items():
            if isle in visited:
                continue
            # If the island is not reachable from the current island, skip it.
            travel_t = dist.get(isle)
            if travel_t is None:
                continue 

            exp_time  = sum(experiences)
            gain      = len(experiences)      # The number of experiences on that island.
            cost      = travel_t + exp_time   # The time to travel there and time to enjoy experiences.

            # Skip if it blows the overall travel time budget.
            if time_budget and total_time + cost > time_budget:
                continue

            # Pick the island that gives the most experience per time limit.
            ratio = gain / cost
            if ratio > best_ratio:
                best_ratio, best_isle = ratio, isle

        # Once we've chosen the best island or if no island is worth visiting or reachable, stop the loop.
        if best_isle is None:
            break

        # Commit to best island:
        #   Update the total travel and experience time.
        #   Add the island to our route.
        #   Mark it as visited so we don't visit it again.
        travel = dist[best_isle]
        enjoy  = sum(exp[best_isle])
        total_time += travel + enjoy
        total_exp  += len(exp[best_isle])
        route.append(best_isle)
        visited.add(best_isle)

    return route, total_time, total_exp

# --- Demo Run: to test the algorithm implementation ---
# Note: This is a simple demo run with RANDOMIZED values to show how the algorithm works.
if __name__ == "__main__":
    # Sample graph of Polynesian islands.
    G["Hawaiʻi"].append(("Tahiti", 7))
    G["Tahiti"].append(("Hawaiʻi", 7))

    G["Tahiti"].append(("Samoa", 6))
    G["Samoa"].append(("Tahiti", 6))

    G["Tahiti"].append(("Fiji", 4))
    G["Fiji"].append(("Tahiti", 4))

    G["Samoa"].append(("Fiji", 2.5))
    G["Fiji"].append(("Samoa", 2.5))

    # Experience durations (assuming in hours).
    exp["Hawaiʻi"]    = [1.0, 0.75]        # 2 experiences
    exp["Tahiti"]     = [1.5]              # 1 experience
    exp["Samoa"]      = [0.5, 1.0]         # 2 experiences
    exp["Fiji"]       = [0.75, 0.75, 0.5]  # 3 experiences

    # Run the route builder.
    route, t, e = best_itinerary(start, TIME_BUDGET)

    print("Route:", " → ".join(route))
    print(f"Total time: {t:.2f}")
    print("Total experiences:", e)

# Expected output:
#   Route: Hawaiʻi → Fiji → Samoa → Tahiti
#   Total time: 26.25
#   Total experiences: 8
