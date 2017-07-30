#Max flow (Ford Fulkerson w/ Edmund Karp)

class Paths:
	def __init__(self, paths):
		self.paths = paths
		self.order = len(paths)

	#add two vertices that act as source and sink
	#the source connects to all entrances and
	#the sink connects to all the exits
	def add_source_and_sink(self, sources, sinks):
		for i in range(self.order):
			self.paths[i] = [0] + self.paths[i] + [0]

		s_row = [0] * (self.order+2)
		for val in sources: 	
			s_row[val+1] = 2000001

		for val in sinks:
			self.paths[val][self.order+1] = 2000001

		t_row = [0] * (self.order+2)

		self.paths = [s_row] + self.paths + [t_row]
		self.order = len(self.paths)

	#augmented path using bfs
	def find_augment_path(self, source, sink, parent):
		visited = [-1]*self.order
		queue = []

		queue.append(source)
		visited[source] = 1;

		while(len(queue)>0):
			current = queue.pop(0)
			for i, val in enumerate(self.paths[current]):
				if(visited[i] < 0 and val > 0):
					queue.append(i)
					visited[i] = 1
					parent[i] = current

		#if a path exists return ture
		if(visited[sink] > 0):
			return True
		else:
			return False

	def get_max_flow(self):
		max_flow = 0

		#first node is always the source and last node is always the sink
		source = 0
		sink = self.order-1

		#passed by reference to get parent map
		parent = [-1]*self.order;

		while self.find_augment_path(source, sink, parent):
			flow_now = 2000001	#as this is the given infinity
			t = sink
			while(t != source):
				flow_now = min(flow_now, self.paths[parent[t]][t])
				t = parent[t]

			max_flow += flow_now

			#updating residual graph weights and adding back edges (cancellations)
			t = sink
			while(t != source):
				s = parent[t]
				self.paths[s][t] -= flow_now
				self.paths[t][s] += flow_now
				t = parent[t]

		return max_flow

def answer(entrances, exits, paths):
	paths = Paths(paths);
	paths.add_source_and_sink(entrances, exits);
	return paths.get_max_flow()
	

s = [0,1]
t = [4,5]
p = [
		[0,0,4,6,0,0],
		[0,0,5,2,0,0],
		[0,0,0,0,4,4],
		[0,0,0,0,6,6],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0]
	]
print(answer(s,t,p))

s = [0]
t = [3]
p = [
		[0, 7, 0, 0],
		[0, 0, 6, 0],
		[0, 0, 0, 8],
		[9, 0, 0, 0]
	]
print(answer(s,t,p))