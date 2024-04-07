from contextlib import nullcontext
from unittest.mock import Mock

import pytest


# Helper function to show we expect some output (and not an error!)
def expected(x):
    """Uses to show that function must be executed without any error.
    Return value MUST be specified.

    :x: Any return value.
    """
    return x, nullcontext()


# Helper function to show we do expect an error
def error(*args, **kwargs):
    """Uses to show that execution of function will fail. Exception type(s)
    MUST be specified, additional parameters can be provided as kwargs.

    :args: Exception type(s).
    :kwargs: Additional keyword parameters for `pytest.raises`.
    """

    return Mock(), pytest.raises(*args, **kwargs)
