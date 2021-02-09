from graph_algorithms import Graph


def graph_rep_test():
    small_graph = Graph()

    natania = small_graph.create_vertex('natania')
    yerushalaim = small_graph.create_vertex('yerushaliam')
    gedera = small_graph.create_vertex('gedera')
    natania_gedera = small_graph.create_edge(natania, gedera, 5)
    graph_rep = small_graph.dump_graph()

    assert graph_rep == {natania: [natania_gedera], gedera: [natania_gedera], yerushalaim: []}


graph_rep_test()




