import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from bidst.path_manager import PathManager


basedir001 = os.path.abspath('data/ds001')
basedir114 = os.path.abspath('data/ds114')


def test_simple_file_search():
    PM = PathManager(basedir=basedir001)
    result = PM.get(subject='01', extensions='.nii.gz', run='01')[0]
    assert result == os.path.abspath('data/ds001/sub-01/func/' + \
                        'sub-01_task-balloonanalogrisktask_run-01_bold.nii.gz')


def test_simple_make():
    PM = PathManager(basedir=basedir114)
    in_file = basedir114 + \
              '/sub-01/ses-test/anat' + \
              '/sub-01_ses-test_T1w.nii.gz'
    pipeline_name = 'pipeline0'
    derivative = '<deriv>'
    result = PM.make(in_file=in_file,
                     pipeline_name=pipeline_name,
                     derivative=derivative)
    needed_result = basedir114 + \
                    '/derivatives/pipeline0' + \
                    '/sub-01/ses-test/anat' \
                    '/sub-01_ses-test_T1w_<deriv>.nii.gz'
    assert result == needed_result


def test_tags():
    PM = PathManager(basedir=basedir114)
    in_file = basedir114 + \
              '/sub-01/ses-test/anat' + \
              '/sub-01_ses-test_T1w.nii.gz'
    pipeline_name = 'pipeline0'
    derivative = '<deriv>'
    tags = [('tagname1', '<tagvalue1>'),
            ('tagname2', '<tagvalue2>')]
    result = PM.make(in_file=in_file,
                     pipeline_name=pipeline_name,
                     derivative=derivative,
                     tags=tags)
    needed_result = basedir114 + \
                    '/derivatives/pipeline0' + \
                    '/sub-01/ses-test/anat/' + \
                    'sub-01_ses-test_T1w_tagname1-<tagvalue1>_tagname2-<tagvalue2>_<deriv>.nii.gz'
    assert result == needed_result


def test_extension():
    PM = PathManager(basedir=basedir114)
    in_file = basedir114 + \
              '/sub-01/ses-test/anat' + \
              '/sub-01_ses-test_T1w.nii.gz'
    pipeline_name = 'pipeline0'
    derivative = '<deriv>'
    result = PM.make(in_file=in_file,
                     pipeline_name=pipeline_name,
                     derivative=derivative,
                     extension='.py')
    needed_result = basedir114 + \
                    '/derivatives/pipeline0' + \
                    '/sub-01/ses-test/anat' \
                    '/sub-01_ses-test_T1w_<deriv>.py'
    assert result == needed_result
