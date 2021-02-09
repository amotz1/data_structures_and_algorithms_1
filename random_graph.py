from graph_algorithms import Graph
import random


def create_random_graph(vertices_number, edges_number):
    random_graph = Graph()

    for i in range(vertices_number):
        random_graph.create_vertex(f'vertex{i}')

    edge_counter = 0
    while edge_counter != edges_number:
        vertices_list = [elem.value for elem in random_graph.label2vertex]

        random_ind_1 = random.randrange(0, random_graph.label2vertex.size())
        random_ind_2 = random.randrange(0, random_graph.label2vertex.size())
        random_length = random.randrange(1, 100)

        if random_ind_1 != random_ind_2:
            random_graph.create_edge(vertices_list[random_ind_1], vertices_list[random_ind_2], random_length)
            edge_counter += 1

    return random_graph


create_random_graph(3, 2)