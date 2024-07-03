import os
from pathlib import Path
import pathpartout
from unittest import mock, TestCase, main

SAMPLE_PROJECT_ROOT = Path(__file__).parent.as_posix()
SAMPLE_PROJECT_NAME = 'Sample_Project'
@mock.patch.dict(
    os.environ,
    {
        "PATH_PARTOUT_CONF_FOLDERS": SAMPLE_PROJECT_ROOT,
        "PATH_PARTOUT_ROOTS":f"fabrication={SAMPLE_PROJECT_ROOT}&render={SAMPLE_PROJECT_ROOT}"
    }
)
class TestAutoArbo(TestCase):
    def test_generate_arbo(self):
        config_filepath = Path(__file__).parent.joinpath('sample.conf').as_posix()
        required_info = {
            'project_name': SAMPLE_PROJECT_NAME,
        }

        pathpartout.auto_arbo.generate(
            config_path=config_filepath,
            required_info=required_info
        )

        self.assertEqual(True, True)
        
if __name__ == '__main__':
    main()