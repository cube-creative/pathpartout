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
class TestTree(TestCase):
    def setUp(self) -> None:
        self.initial_shot_working_file = f"{SAMPLE_PROJECT_ROOT}/{SAMPLE_PROJECT_NAME}/episodes/s01e018_bearselandgretel/shots/sq01sh005/steps/animationT2/sq01sh005_animationt2_v001.blend"
        return super().setUp()

    def test_tree_from_label(self):
        tree = pathpartout.tree.get_from_label('shot_working_file', self.initial_shot_working_file)
        generated_shot_working_file = tree.get_label_path('shot_working_file')
        self.assertEqual(self.initial_shot_working_file.lower(), generated_shot_working_file.lower())

    def test_tree_from_path(self):
        tree = pathpartout.tree.get_from_path(self.initial_shot_working_file)
        tree.fill_with_label('shot_working_file', self.initial_shot_working_file)
        generated_shot_working_file = tree.get_label_path('shot_working_file')
        self.assertEqual(self.initial_shot_working_file.lower(), generated_shot_working_file.lower())

    def test_tree_from_config_win(self):
        tree = pathpartout.tree.get_from_config(f'{SAMPLE_PROJECT_ROOT}/sample.conf')
        tree.fill_with_label('shot_working_file', self.initial_shot_working_file)
        generated_shot_working_file = tree.get_label_path('shot_working_file')
        self.assertEqual(self.initial_shot_working_file.lower(), generated_shot_working_file.lower())

    def test_tree_fill_with_agregate(self):
        tree = pathpartout.tree.get_from_config(f'{SAMPLE_PROJECT_ROOT}/sample.conf')
        tree.info["project_name"] = SAMPLE_PROJECT_NAME
        tree.fill_with_aggregate("episode_full_name", 's01e018_bearselandgretel')
        folder_path = tree.get_label_path('episode_library_folder')

        self.assertEqual(f"{SAMPLE_PROJECT_ROOT}/{SAMPLE_PROJECT_NAME}/episodes/s01e018_bearselandgretel".lower(), folder_path.lower())
if __name__ == '__main__':
    main()