"""Authors: Cody Baker and Ben Dichter."""
import numpy as np
from collections import defaultdict
from unittest import TestCase
from shutil import rmtree
from tempfile import mkdtemp
from uuid import uuid4
from datetime import datetime
from pathlib import Path

import pynwb

from nwbinspector.refactor_inspector import inspect_nwb


class TestInspector(TestCase):
    def setUp(self):
        self.tempdir = Path(mkdtemp())
        self.nwbfile = pynwb.NWBFile(
            session_description="Testing inspector.",
            identifier=str(uuid4()),
            session_start_time=datetime.now().astimezone(),
        )

    def tearDown(self):
        rmtree(self.tempdir)

    def add_bad_check_dataset_compression(self):
        device = self.nwbfile.create_device(name="test_device")
        electrode_group = self.nwbfile.create_electrode_group(
            name="test_group", description="", location="", device=device
        )
        num_electrodes = 4
        electrode_ids = list(range(num_electrodes))
        for id in electrode_ids:
            self.nwbfile.add_electrode(
                id=id,
                x=np.nan,
                y=np.nan,
                z=np.nan,
                imp=np.nan,
                location="",
                filtering="",
                group=electrode_group,
            )
        electrode_table_region = self.nwbfile.create_electrode_table_region(
            electrode_ids, description=""
        )

        n_bytes = 3e6
        # itemsize of 8 because of float dtype
        n_frames = int(n_bytes / (num_electrodes * 8))
        ephys_data = np.zeros(shape=(n_frames, num_electrodes))
        ephys_ts = pynwb.ecephys.ElectricalSeries(
            name="test_ecephys",
            data=ephys_data,
            electrodes=electrode_table_region,
            rate=10.0,
        )
        self.nwbfile.add_acquisition(ephys_ts)

    def test_inspect_nwb(self):
        self.add_bad_check_dataset_compression()

        nwbfile_path = str(self.tempdir / "testing.nwb")
        with pynwb.NWBHDF5IO(path=nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with pynwb.NWBHDF5IO(path=nwbfile_path, mode="r") as io:
            nwbfile_in = io.read()
            check_results = inspect_nwb(nwbfile=nwbfile_in)

        true_results = defaultdict(
            list,
            {
                1: [
                    dict(
                        check_function_name="check_dataset_compression",
                        object_type="ElectricalSeries",
                        object_name="test_ecephys",
                        output="Consider enabling compression when writing a large dataset.",
                    )
                ]
            },
        )
        self.assertDictEqual(d1=check_results, d2=true_results)
