"""Authors: Cody Baker, Ben Dichter, and Ryan Ly."""
import numpy as np

import h5py
from pynwb import NWBContainer, TimeSeries

from ..utils import nwbinspector_check


@nwbinspector_check(severity=1, neurodata_type=NWBContainer)
def check_dataset_compression(nwb_container: NWBContainer, bytes_threshold=2e6):
    """
    If the data in the TimeSeries object is a h5py.Dataset, check if it has compression enabled.

    Will only run if the size of the h5py.Dataset is larger than bytes_threshold.
    """
    for field in getattr(nwb_container, "fields", dict()).values():
        if (
            isinstance(field, h5py.Dataset)
            and field.size * field.dtype.itemsize > bytes_threshold
            and field.compression is None
        ):
            return "Consider enabling compression when writing a large dataset."


# TODO: break up extra logic
# def check_data_uniqueness(ts):
#     """Check whether data of a timeseries has few unique values and can be stored in a better way."""
#     uniq = np.unique(ts.data)
#     if len(uniq) == 1:
#         error_code = "A101"
#         print("- %s: '%s' %s data has all values = %s" % (error_code, ts.name, type(ts).__name__, uniq[0]))
#     elif np.array_equal(uniq, [0.0, 1.0]):
#         if ts.data.dtype != bool and type(ts) is TimeSeries:
#             # if a base TimeSeries object has 0/1 data but is not using booleans
#             # note that this tests only base TimeSeries objects. TimeSeries subclasses may require numeric/int/etc.
#             error_code = "A101"
#             print(
#                 "- %s: '%s' %s data only contains values 0 and 1. Consider changing to type boolean instead of %s"
#                 % (error_code, ts.name, type(ts).__name__, ts.data.dtype)
#             )
#     elif len(uniq) == 2:
#         print(
#             "- NOTE: '%s' %s data has only 2 unique values: %s. Consider storing the data as boolean."
#             % (ts.name, type(ts).__name__, uniq)
#         )
#     elif len(uniq) <= 4:
#         print("- NOTE: '%s' %s data has only unique values %s" % (ts.name, type(ts).__name__, uniq))
