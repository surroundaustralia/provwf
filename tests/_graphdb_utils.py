import requests


def setup_graphdb():
    # check to see if GraphDB is online
    try:
        r = requests.get("http://localhost:7200")
    except:
        return "Local GraphDB not available"

    # check to see if we have a repository available for testing
    r = requests.get("http://localhost:7200/rest/repositories", headers={"Accept": "application/json"})
    have_repo = False
    if hasattr(r.json(), "message"):
        if r.json()["message"] == "There is no active location!":
            return "Local GraphDB has no active locations"

    for repo in r.json():
        if repo["id"] == "provwftesting":
            have_repo = True
    if not have_repo:
        multipart_form_data = {
            'config': ("_graphdb-repo-config.ttl", open("_graphdb-repo-config.ttl", 'r'))
        }
        r = requests.post("http://localhost:7200/rest/repositories", files=multipart_form_data)
        if not r.ok:
            return "Unable to access or create testing repo"

    # clear repo
    r = requests.delete(
        "http://localhost:7200/repositories/provwftesting/statements",
        headers={"Accept": "application/json"}
    )
    if not r.ok:
        return "Could not clear all data in provwftesting repository"

    return None


def teardown_graphdb():
    r = requests.delete(
        "http://localhost:7200/repositories/provwftesting",
        headers={"Accept": "application/json"}
    )
    if not r.ok:
        return "Could not delete repo provwftesting"
