from random_graph import create_random_graph


def random_graph_test():
    vertices_number = 785
    edges_number = 87

    random_graph = create_random_graph(vertices_number, edges_number)
    graph_rep = random_graph.dump_graph()

    graph_vertices = []
    graph_edges = []
    for vertex, vertex_edges in graph_rep.items():
        graph_vertices.append(vertex)
        for edge in vertex_edges:
            if edge in graph_edges:
                continue
            graph_edges.append(edge)

    assert(len(graph_vertices) == 785)
    assert(len(graph_edges) == 87)


random_graph_test()

    





