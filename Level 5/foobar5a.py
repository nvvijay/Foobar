class ExpandingNebula:
    #cache to store row's fibers vs counts
    memory = {}

    #inverse function map
    backward = {0: (
                    ((0, 0),(0, 0)),
                    ((0, 0),(1, 1)),
                    
                    ((0, 1),(0, 1)),
                    ((0, 1),(1, 0)),
                    ((0, 1),(1, 1)),
                    
                    ((1, 0),(0, 1)),
                    ((1, 0),(1, 0)),
                    ((1, 0),(1, 1)),
                    
                    ((1, 1),(0, 0)),
                    ((1, 1),(0, 1)),
                    ((1, 1),(1, 0)),
                    ((1, 1),(1, 1)),
                    ),
                1: (
                    ((0, 0),(0, 1)),
                    ((0, 0),(1, 0)),
                    ((0, 1),(0, 0)),
                    ((1, 0),(0, 0)),
                    )
                }

    #function map
    forward = {
                ((0, 0),(0, 0)) : 0,
                ((0, 0),(1, 1)) : 0,
                ((0, 1),(0, 1)) : 0,
                ((0, 1),(1, 0)) : 0,
                ((0, 1),(1, 1)) : 0,
                ((1, 0),(0, 1)) : 0,
                ((1, 0),(1, 0)) : 0,
                ((1, 0),(1, 1)) : 0,
                ((1, 1),(0, 0)) : 0,
                ((1, 1),(0, 1)) : 0,
                ((1, 1),(1, 0)) : 0,
                ((1, 1),(1, 1)) : 0,

                ((0, 0),(0, 1)) : 1,
                ((0, 0),(1, 0)) : 1,
                ((0, 1),(0, 0)) : 1,
                ((1, 0),(0, 0)) : 1
            }

    #all new possibilities
    new = [(0,0), (0,1), (1,0), (1,1)]

    def __init__(self, g):
        self.g = g

    def transpose(self, matrix):
        return tuple(zip(*matrix))

    def get_initial_fiber_counts(self):
        g = self.g[0]

        #map to maintain counts
        overlap_counts = {}
        
        fibers = self.backward[g[0]]
        for i in range(1, len(g)):
            more_fibers = []
            for preimage in fibers:
                for test in self.new:
                    check = (preimage[i], test)
                    #TODO: optimize for mirror images
                    if self.forward[check] == g[i]:
                        temp = list(preimage)
                        temp.append(test)
                        more_fibers.append(temp)
            fibers = tuple(more_fibers)
        fibers = tuple([self.transpose(img) for img in fibers])
        self.memory[g] = fibers
        for preimage in fibers:
            overlap = preimage[1]
            if overlap in overlap_counts:
                overlap_counts[overlap] += 1
            else:
                overlap_counts[overlap] = 1
        return overlap_counts

    def get_next_counts(self, counts, g_col):
        new_fiber_counts = []
        for item in counts:
            fibers = []
            for test in self.new:
                if self.forward[((item[0], item[1]), test)] == g_col[0]:
                    fibers.append(test)

            for j in range(1, len(g_col)):
                new_fibers = []
                if len(fibers) == 0:
                    break
                for preimg in fibers:
                    for k in range(2):
                        tmp = list(preimg)
                        if self.forward[((item[j], item[j+1]),(preimg[j], k))] == g_col[j]:
                            tmp.append(k)
                            new_fibers.append(tmp)
                fibers = new_fibers
            [new_fiber_counts.append((item, tuple(x))) for x in fibers]
        return tuple(new_fiber_counts)
        
    def brute_it(self, counts):
        for i in range(1, len(self.g)):
            new_counts = {}

            #exponentially decreasing chances of cache hit, but still
            if self.g[i] in self.memory:
                new_fibers = self.memory[self.g[i]]
            else:
                new_fibers = self.get_next_counts(counts, (self.g)[i])
            total = len(new_fibers)
            for item in new_fibers:
                if item[0] in counts:
                    if item[1] in new_counts:
                        new_counts[item[1]] = counts[item[0]] + new_counts[item[1]]
                    else:
                        new_counts[item[1]] = counts[item[0]]
            counts = new_counts
        final_count = 0
        for i, val in counts.items():
            final_count += val

        return final_count

    def count_prev_states(self):
        #transpose since the given spec is a very narrow rectangle.
        self.g = self.transpose(self.g)
        combinations = {}

        #expand the first column of g to get the initial preimages and its counts
        fiber_counts = self.get_initial_fiber_counts()
        #time to bruteforce
        return self.brute_it(fiber_counts)


def answer(g):
    en = ExpandingNebula(g)
    return en.count_prev_states()

test = [[0,1,0,0,1,0,0,1,0,0,1],[0,1,0,0,1,0,0,1,1,0],[0,1,0,0,1,0,0,1,0,0,1]]
print(answer(test))
