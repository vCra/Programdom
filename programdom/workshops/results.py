"""
Helpers to process result data, and return it in a format our graphs can understand. They will probably be a timer
for the Presenter Consumer, which should query this every x seconds, and then send it to graphs.
Before we updated the graphs on each change, but with multiple changes happening every second, and processing potentially
taking longer, this is a better approach.
"""
from programdom.models import SubmissionTestResult

ACCEPTED_ID = 3
WRONG_ID = 4
TIME_ID = 5
COMPILATION_ID = 6
ERROR_IDS = list(range(7, 12))

def results_data(workshop, problem):
    """
    Gets results data for the graph
    Results data is data for a problem in a workshop - all submissions should get counted, and
    :return:
    """

    test_results = SubmissionTestResult.objects.filter(submission__problem=problem, submission__workshop=workshop)
    accepted = test_results.filter(results_data__status__id=ACCEPTED_ID).count()
    wrong_answer = test_results.filter(results_data__status__id=WRONG_ID).count()
    time_limit = test_results.filter(results_data__status__id=TIME_ID).count()
    compilation = test_results.filter(results_data__status__id=COMPILATION_ID).count()
    runtime = test_results.filter(results_data__status__id_in=ERROR_IDS).count()

    return [accepted, wrong_answer, time_limit, compilation, runtime]

def time_data(workshop, problem, increment):
    """
    Here we need to get the occurances within each time interval, starting at the start time, and ending at the end time
    :param workshop:
    :param problem:
    :param increment: the time frame to indent by, in seconds
    :return:
    """

    test_results = SubmissionTestResult.objects.filter(submission__problem=problem, submission__workshop=workshop).order_by("submission__date")

    # If no submissions have been made yet, then they is no need to update the data
    if not test_results.first():
        return None

    start_time = test_results.first().date
    end_time = test_results.end().date

    # Calculate the number of results to return
    total_time = end_time-start_time

    return test_results




