import graph_algorithms as graph_algorithms
from graph_algorithms import Graph
from graph_algorithms import Algorithms
import sys
import datetime
from random_graph import create_random_graph
import time
import os


def create_graph():
    israel_cities = graph_algorithms.Graph()

    haifa = israel_cities.create_vertex('haifa')
    naharia = israel_cities.create_vertex('naharia')
    rishon = israel_cities.create_vertex('rishon')
    eilat = israel_cities.create_vertex('eilat')

    israel_cities.create_edge(haifa, naharia, 10)
    israel_cities.create_edge(haifa, rishon, 2)
    israel_cities.create_edge(rishon, eilat, 12)
    israel_cities.create_edge(rishon, naharia, 1)
    israel_cities.create_edge(naharia, eilat, 30)

    return israel_cities


def test_correct_path(edges, correct_edges_attributes):
    assert len(edges) == len(correct_edges_attributes)
    for edge, attributes in zip(edges, correct_edges_attributes):
        # comparing each edge vertex attribute to either one of two vertices because edges are bi-directional
        assert edge.vertex_1 == attributes[0] and edge.vertex_2 == attributes[1] \
               or edge.vertex_2 == attributes[0] and edge.vertex_1 == attributes[1]
        assert edge.length == attributes[2]


def is_path(edges, source, dest):
    vertex = source
    for edge in edges:
        vertex = edge.get_other_vertex(vertex)
    return vertex == dest


def test_shortest_path_algorithms():
    israel_cities = create_graph()
    haifa = israel_cities.get_vertex('haifa')
    rishon = israel_cities.get_vertex('rishon')
    naharia = israel_cities.get_vertex('naharia')
    eilat = israel_cities.get_vertex('eilat')

    haifa_naharia = haifa.edges[0]
    assert haifa_naharia.get_other_vertex(haifa) == naharia
    assert haifa_naharia.get_other_vertex(naharia) == haifa

    haifa_rishon = haifa.edges[1]
    assert haifa_rishon.get_other_vertex(haifa) == rishon
    assert haifa_rishon.get_other_vertex(rishon) == haifa

    rishon_naharia = rishon.edges[2]
    assert rishon_naharia.get_other_vertex(naharia) == rishon
    assert rishon_naharia.get_other_vertex(rishon) == naharia

    rishon_eilat = rishon.edges[1]
    assert rishon_eilat.get_other_vertex(eilat) == rishon
    assert rishon_eilat.get_other_vertex(rishon) == eilat

    naharia_eilat = naharia.edges[2]
    assert naharia_eilat.get_other_vertex(naharia) == eilat
    assert naharia_eilat.get_other_vertex(eilat) == naharia

    assert Algorithms.compute_all_paths(haifa, eilat) == [[haifa_naharia, rishon_naharia, rishon_eilat],
                                                          [haifa_naharia, naharia_eilat],
                                                          [haifa_rishon, rishon_eilat],
                                                          [haifa_rishon, rishon_naharia, naharia_eilat]]

    (min_path_length, min_path) = Algorithms.shortest_path_bf(haifa, eilat)
    assert min_path_length == 14

    (shortest_path_length, shortest_path) = Algorithms.shortest_path_bf(haifa, haifa)
    assert shortest_path_length == 0
    assert shortest_path == []

    paths = []
    Algorithms._compute_all_paths(naharia, eilat, [haifa_naharia], paths)
    print(paths)

    # basic functionality test graph

    israel_cities = graph_algorithms.Graph()
    hulon = israel_cities.create_vertex('hulon')
    rishon = israel_cities.create_vertex('rishon')
    haifa = israel_cities.create_vertex('haifa')
    beer_sheva = israel_cities.create_vertex('beer_sheva')
    naharia = israel_cities.create_vertex('naharia')
    eilat = israel_cities.create_vertex('eilat')

    israel_cities.create_edge(haifa, hulon, 25)
    israel_cities.create_edge(haifa, eilat, 100)
    israel_cities.create_edge(haifa, rishon, 40)
    israel_cities.create_edge(hulon, rishon, 50)
    israel_cities.create_edge(hulon, naharia, 60)
    israel_cities.create_edge(rishon, beer_sheva, 20)
    israel_cities.create_edge(naharia, eilat, 10)
    israel_cities.create_edge(naharia, beer_sheva, 20)
    israel_cities.create_edge(beer_sheva, eilat, 90)

    (shortest_path_length, shortest_path) = Algorithms.dykstra(haifa, haifa)
    (shortest_path_length_bf, shortest_path_bf) = Algorithms.shortest_path_bf(haifa, haifa)

    assert shortest_path_length == shortest_path_length_bf
    assert shortest_path == shortest_path_bf
    assert shortest_path_length == 0
    assert is_path(shortest_path, haifa, haifa)

    correct_edges_attributes = []
    test_correct_path(shortest_path, correct_edges_attributes)

    (shortest_path_length, shortest_path) = Algorithms.dykstra(haifa, rishon)
    (shortest_path_length_bf, shortest_path_bf) = Algorithms.shortest_path_bf(haifa, rishon)

    assert shortest_path_length == shortest_path_length_bf
    assert shortest_path == shortest_path_bf
    assert shortest_path_length == 40
    assert is_path(shortest_path, haifa, rishon)

    correct_edges_attributes = [(haifa, rishon, 40)]
    test_correct_path(shortest_path, correct_edges_attributes)

    (shortest_path_length, shortest_path) = Algorithms.dykstra(rishon, haifa)
    (shortest_path_length_bf, shortest_path_bf) = Algorithms.shortest_path_bf(rishon, haifa)

    assert shortest_path_length == shortest_path_length_bf
    assert shortest_path == shortest_path_bf
    assert shortest_path_length == 40
    assert is_path(shortest_path, rishon, haifa)

    correct_edges_attributes = [(rishon, haifa, 40)]
    test_correct_path(shortest_path, correct_edges_attributes)

    (shortest_path_length, shortest_path) = Algorithms.dykstra(haifa, eilat)
    (shortest_path_length_bf, shortest_path_bf) = Algorithms.shortest_path_bf(haifa, eilat)

    assert shortest_path_length == shortest_path_length_bf
    assert shortest_path == shortest_path_bf
    assert shortest_path_length == 90
    assert is_path(shortest_path, haifa, eilat)

    correct_edges_attributes = [(haifa, rishon, 40), (rishon, beer_sheva, 20), (beer_sheva, naharia, 20),
                                (naharia, eilat, 10)]

    test_correct_path(shortest_path, correct_edges_attributes)

    # the graph i create below is a test case to a bug related to the condition for stopping the while loop
    # in shortest_path function of the grath algorithms file.
    # (stopping the while loop if dest is smaller then the max or min path lengths of paths that i developed)

    israel_cities = graph_algorithms.Graph()
    haifa = israel_cities.create_vertex('haifa')
    petach_tikva = israel_cities.create_vertex('petach_tikva')
    rishon = israel_cities.create_vertex('rishon')
    eilat = israel_cities.create_vertex('eilat')

    israel_cities.create_edge(haifa, eilat, 10)
    israel_cities.create_edge(haifa, petach_tikva, 2)
    israel_cities.create_edge(haifa, rishon, 12)
    israel_cities.create_edge(petach_tikva, eilat, 1)
    israel_cities.create_edge(rishon, eilat, 30)

    (shortest_path_length, shortest_path) = Algorithms.dykstra(haifa, eilat)
    (shortest_path_length_bf, shortest_path_bf) = Algorithms.shortest_path_bf(haifa, eilat)

    assert shortest_path_length == shortest_path_length_bf
    assert shortest_path == shortest_path_bf
    assert shortest_path_length == 3

    correct_edges_attributes = [(haifa, petach_tikva, 2), (petach_tikva, eilat, 1)]
    test_correct_path(shortest_path, correct_edges_attributes)
    assert is_path(shortest_path, haifa, eilat)

    # checking a test case of a graph with unreachable dest
    unreachable_test_graph = Graph()
    x = unreachable_test_graph.create_vertex('dummy')
    y = unreachable_test_graph.create_vertex('dummy')
    assert Algorithms.dykstra(x, y) == (sys.maxsize, None)
    assert Algorithms.shortest_path_bf(x, y) == (sys.maxsize, None)

    # checking a test case of a graph with 2 edges between 2 vertices
    israel_cities = Graph()
    haifa = israel_cities.create_vertex('haifa')
    rishon = israel_cities.create_vertex('rishon')
    eilat = israel_cities.create_vertex('eilat')
    haifa_rishon1 = israel_cities.create_edge(haifa, rishon, 10)
    haifa_rishon2 = israel_cities.create_edge(haifa, rishon, 6)
    rishon_eilat = israel_cities.create_edge(rishon, eilat, 10)
    assert haifa.get_edges() == [haifa_rishon1, haifa_rishon2]
    assert rishon.get_edges() == [haifa_rishon1, haifa_rishon2, rishon_eilat]
    assert eilat.get_edges() == [rishon_eilat]

    assert Algorithms.dykstra(haifa, eilat) == (16, [haifa_rishon2, rishon_eilat])
    assert Algorithms.shortest_path_bf(haifa, eilat) == (16, [haifa_rishon2, rishon_eilat])


test_shortest_path_algorithms()


def test_algorithms_equivalence(num_vertex_pairs, num_vertices, num_edges):
    random_graph = create_random_graph(num_vertices, num_edges)
    vertices = [elem.value for elem in random_graph.label2vertex]
    max_num_pairs = len(vertices) ** 2
    assert max_num_pairs >= num_vertex_pairs >= 0, 'you specified a number out of range, please try ' \
                                                             'a number between 0 and %d' % max_num_pairs

    pair_counter = 0
    for vertex1 in vertices:
        for vertex2 in vertices:
            pair_counter += 1
            (shortest_path_length, shortest_path) = Algorithms.dykstra(vertex1, vertex2)
            (shortest_path_length_bf, shortest_path_bf) = Algorithms.shortest_path_bf(vertex1, vertex2)

            assert shortest_path_length == shortest_path_length_bf

        if pair_counter == num_vertex_pairs:
            break


def calc_algorithms_exec_times(num_vertex_pairs, random_graph):
    vertices = [elem.value for elem in random_graph.label2vertex]
    max_num_pairs = len(vertices) ** 2
    assert max_num_pairs >= num_vertex_pairs >= 0, 'you specified a number out of range, please try ' \
                                                   'a number between 0 and %d' % max_num_pairs

    pair_counter = 0
    shortest_path_total_time = 0
    shortest_path_bf_total_time = 0
    for vertex1 in vertices:
        for vertex2 in vertices:
            pair_counter += 1

            if pair_counter >= num_vertex_pairs:
                break

            shortest_path_start_time = time.process_time()
            Algorithms.dykstra(vertex1, vertex2)
            shortest_path_exec_time = time.process_time() - shortest_path_start_time
            shortest_path_total_time += shortest_path_exec_time

            shortest_path_bf_start_time = time.process_time()
            Algorithms.shortest_path_bf(vertex1, vertex2)
            shortest_path_bf_exec_time = time.process_time() - shortest_path_bf_start_time
            shortest_path_bf_total_time += shortest_path_bf_exec_time

    return shortest_path_bf_total_time, shortest_path_total_time


def create_perf_exp(num_vertices, num_edges, num_vertex_pairs, edge_increment, num_tests):
    print('starting experiment... \n')
    time.sleep(2)

    date_time = datetime.datetime.now()
    d = (str(date_time).split(' ')[0])
    t = (str(date_time).split(' ')[1]).replace(":", "-")
    with open(f'performance experiment for dykstra and brute_force ' + str(d) + ' ' + str(t)
              + '.txt', 'a') as text_file:

        text_file.write(f'uniform random graph with {num_edges} edges and {num_vertices} '
                        f'vertices. doing {num_tests} tests with {edge_increment} edge increment. searching '
                        f'{num_vertex_pairs} vertex pairs.' + '\n' + '\n')

        for test in range(num_tests):
            uniform_random_graph = create_random_graph(num_vertices, num_edges)
            (dykstra, brute_force) = calc_algorithms_exec_times(num_vertex_pairs, uniform_random_graph)
            text_file.write(str(dykstra) + ' ' + str(brute_force) + '\n')
            print(f'd {dykstra} b {brute_force} num tests {test}')
            num_edges += edge_increment

    print('end of experiment \n')
    time.sleep(2)


create_perf_exp(10, 10, 90, 1, 20)
create_perf_exp(15, 15, 203, 1, 20)
create_perf_exp(20, 20, 360, 1, 20)

create_perf_exp(100, 20, 9000, 1, 20)
create_perf_exp(120, 30, 12960, 1, 20)
create_perf_exp(160, 40, 23040, 1, 20)

test_algorithms_equivalence(90000, 1000, 500)

# TODO optimizing path_vartices to be a hashtable  for better performance in find_path_vertices function.
# TODO maybe trying to avoid the find_path_vertices and using lambda instead for lazy evaluation
# TODO making the recursion call r
#  eturn a list of paths instead of an output parameter
# TODO making random_graph and comparing shortest_path_bf with shortest_path
