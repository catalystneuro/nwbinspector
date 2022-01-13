"""Authors: Cody Baker and Ben Dichter."""
from collections import defaultdict

global default_checks
default_checks = {1: defaultdict(list), 2: defaultdict(list), 3: defaultdict(list)}


def add_to_default_checks(severity: int, neurodata_type):
    """Wrap a check function to add it to the list of default checks for that severity and neurodata type."""

    def decorator(check_function):
        if severity not in [1, 2, 3]:
            raise ValueError(
                f"Indicated severity ({severity}) of custom check ({check_function.__name__}) is not in range of 1-3."
            )
        default_checks[severity][neurodata_type].append(check_function)
        return check_function

    return decorator
