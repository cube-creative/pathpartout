import os
import pathpartout
from unittest import mock, TestCase, main

from tests import SAMPLE_PROJECT_NAME, SAMPLE_PROJECT_ROOT, SAMPLE_CONFIG


@mock.patch.dict(
    os.environ,
    {
        "PATH_PARTOUT_CONF_FOLDERS": SAMPLE_PROJECT_ROOT,
        "PATH_PARTOUT_ROOTS":f"fabrication={SAMPLE_PROJECT_ROOT}&render={SAMPLE_PROJECT_ROOT}"
    }
)
class TestAutoArbo(TestCase):
    def test_generate_arbo(self):
        required_info = {
            'project_name': SAMPLE_PROJECT_NAME,
        }

        pathpartout.auto_arbo.generate(
            config_path=SAMPLE_CONFIG,
            required_info=required_info
        )

        self.assertEqual(True, True)
        
if __name__ == '__main__':
    main()