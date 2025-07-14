import heapq
from collections import defaultdict, deque

# Graph setup: Directed weighted graph
G = defaultdict(list)
G["Hawai'i"].append(("Tahiti", 7))
G["Tahiti"].append(("Hawai'i", 7))
G["Tahiti"].append(("Samoa", 6))
G["Samoa"].append(("Tahiti", 6))
G["Tahiti"].append(("Fiji", 4))
G["Fiji"].append(("Tahiti", 4))
G["Samoa"].append(("Fiji", 2.5))
G["Fiji"].append(("Samoa", 2.5))

# Each island start with 0 shells, except the source
resource_received = defaultdict(float)
source = "Hawai'i"
# 100 shell units at Hawai'i
initial_amount = 100.0
resource_received[source] = initial_amount

# Step 1: Dijkstra's algorithm from source
def shortest_paths(source):
  dist = {source: 0}
  pq = [(0, source)]
  parent = {source: None}
  
  while pq: 
    time, u = heapq.heappop(pq)
    for v, w in G[u]:
      if (new_time := time + w) < dist.get(v, float('inf')):
        dist[v] = new_time
        parent[v] = u
        heapq.heappush(pq, (new_time,v))
  return dist, parent

# Step 2: Distribute resource down the shortest path tree
def distribute_resources(source, initial_amount):
  dist, parent = shortest_paths(source)

  # Build a tree of the shortest paths
  children = defaultdict(list)
  for island, p in parent.items():
    if p:
      children[p].append(island)

  # BFS style distribution of resource
  queue = deque([source])
  while queue:
    island = queue.popleft()
    curr_amount = resource_received[island]
    receivers = children[island]
    if not receivers:
      continue

    amount_per_neighbor = curr_amount / len(receivers)
    for neighbor in receivers:
      resource_received[neighbor] += amount_per_neighbor
      queue.append(neighbor)

  return resource_received, dist

# Run
resource_map, travel_times = distribute_resources(source, initial_amount)

# Output
print("Resource Distribution from Hawai'i:")
for island in sorted(sesource_map.keys(), key=lambda x: travel_times.get(x, float('inf))): print(f"{island}: {resource_map[island]:.2f} shells (Travel Time: {travel_times[island]} hours)")
