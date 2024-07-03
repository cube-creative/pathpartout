import os
import pathpartout
from unittest import mock, TestCase, main


@mock.patch.dict(
        os.environ,
        {
            # "PATH_PARTOUT_CONF_FOLDERS": Path(__file__).parent.joinpath('..')
            "PATH_PARTOUT_ROOTS":"legacy_fabrication=/mnt/p&legacy_rendu=/mnt/i"
        }
    )
class TestTreeLinux(TestCase):

    def setUp(self) -> None:
        self.initial_shot_working_file = "/mnt/p/SON_Serie/episodes/s01e018_bearselandgretel/shots/sq01sh005/steps/animationT2/sq01sh005_animationt2_v001.blend"
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
    
    def test_tree_from_config(self):
        tree = pathpartout.tree.get_from_config('/mnt/c/Users/smartinez/code/repos/_config/pathpartout/general.conf')
        tree.fill_with_label('shot_working_file', self.initial_shot_working_file)
        generated_shot_working_file = tree.get_label_path('shot_working_file')
        self.assertEqual(self.initial_shot_working_file.lower(), generated_shot_working_file.lower())


if __name__ == '__main__':
    main()