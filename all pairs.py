graph = [
            [0,   1,    4,	4,	5,	4,	3,	2,	3,	1,	5,	4,	4,	5,	5,	5],
            [1,	  0,	4,	4,	5,	4,	3,	2,	3,	1,	5,	4,	4,	5,	5,	5],
            [4,	  4,	0,	2,	2,	1,	4,	3,	4,	3,	5,	4,	4,	5,	5,	5],
            [4,	  4,	2,	0,	2,	1,	3,	3,	4,	3,	5,	4,	4,	5,	5,	5],
            [5,   5,	2,	2,	0,	1,	3,	3,	4,	3,	5,	4,	4,	5,	5,	5],
            [4,	  4,	1,	1,	1,	0,	3,	3,	4,	3,	5,	4,	4,	5,	5,	5],
            [3,	  3,	4,	3,	3,	3,	0,	3,	2,	3,	4,	2,	2,	4,	4,	4],
            [2,	  2,	3,	3,	3,	3,	3,	0,	1,	1,	2,	3,	3,	4,	4,	4],
            [3,	  3,	4,	4,	4,	4,	2,	1,	0,	2,	3,	2,	2,	3,	3,	3],
            [1,	  1,	3,	3,	3,	3,	3,	1,	2,	0,	2,	3,	3,	4,	4,	4],
            [5,   5,	5,	5,	5,	5,	4,	2,	3,	2,	0,	4,	4,	5,	5,	5],
            [4,	  4,	4,	4,	4,	4,	2,	3,	2,	3,	4,	0,	1,	3,	3,	3],
            [4,	  4,	4,	4,	4,	4,	2,	3,	2,	3,	4,	1,	0,	3,	3,	3],
            [5,	  5,	5,	5,	5,	5,	4,	4,	3,	4,	5,	3,	3,	0,	1,	4],
            [5,	  5,	5,	5,	5,	5,	4,	4,	3,	4,	5,	3,	3,	1,	0,	4],
            [5,	  5,  	5,	5,	5,	5,	4,	4,	3,	4,	5,	3,	3,	4,	4,	0] ]

INF = float('inf')


def floyd_warshall(graph):
    dist = [[INF for _ in range(len(graph))] for _ in range(len(graph))]

    for i in range(len(graph)):
        for j in range(len(graph)):
            if i == j:
                dist[i][j] = 0
            elif graph[i][j]:
                dist[i][j] = graph[i][j]

    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    
    return dist

result= floyd_warshall(graph)
print(result)