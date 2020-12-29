if __name__ == "__main__":
    # setup a GraphDB repository for testing
    from _graphdb_utils import *
    m = setup_graphdb()
    if m is not None:
        print(m)
        exit()

    # do tests
    import test_prov_reporter as pr
    pr.test_prov_to_graph()
    pr.test_prov_to_graph()
    pr.test_persist_to_string()
    pr.test_persist_to_file()
    pr.test_persist_to_graphdb()
    # pr.test_persist_to_sop()
    # pr.test_persist_to_allegro()
    pr.test_persist_unknown()

    import test_agent as ag
    ag.test_prov_to_graph()

    import test_activity as ac
    ac.test_prov_to_graph()

    import test_entity as en
    en.test_prov_to_graph()

    import test_block as bl
    bl.test_prov_to_graph()

    import test_workflow as wf
    wf.test_prov_to_graph()

    # teardown GraphDB testing repository
    m = teardown_graphdb()
    if m is not None:
        print(m)

    print("testing done")
