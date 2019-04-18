from django.core.cache import cache

"""
For this project we are going to have 2 different graphs presented to lectureres when they are presenting a workshop:
1. Status - Users online, Submissions, Passed
2. Results - For each problem have Accepted Answers, Wrong answers, Time Limits, Compilation, Runtime

How?

Users online: On a WS connection, incr f'workshop_{workshop_code}_users_count'
Submissions: On a submission,
"""

def gen_graph_data(workshop_id, problem_id):
    """
    Generates JSON for the graphs required
    :param workshop_id: The ID of the workshop to generate the JSON for
    :param problem_id: The ID of the problem
    :return: a dict with the graph data in...
    """

    graph_data = {
        "action": "graph_update",
        "cpa": gen_cpa_graph(workshop_id, problem_id),
        "results": 
    }

    return graph_data


def gen_cpa_graph(workshop_id, problem_id):
    """
    Generates a Count Passed Attempted graph
    :param workshop_id:
    :return:
    """
    return {
        "count": cache.get(f'workshop_{workshop_id}_users_count'),
        "passed": cache.get(f'workshop_{workshop_id}_problem_{problem_id}_users_passed'),
        "attempted": cache.get(f'workshop_{workshop_id}_problem_{problem_id}_users_attempted')
    }
