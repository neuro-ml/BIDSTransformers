import os
import sys
import numpy as np
sys.path.insert(0, os.path.abspath('../..'))

import pytest

import bidst
from bidst.path_manager import PathManager
from bidst.transformers import NUCorrectionTransformer
from bidst.transformers import SkullStrippingTransformer
from bidst.transformers import LinearRegistrationTransformer
from bidst.transformers import NonLinearRegistrationTransformer

from nipype.interfaces.fsl import BET
from nipype.interfaces.fsl import FLIRT
from nipype.interfaces.fsl import FNIRT
from nipype.interfaces.ants import N4BiasFieldCorrection

import nibabel as nib

from sklearn.pipeline import Pipeline
from nipype import Node, Workflow
from shutil import rmtree


def test_skull_stripping_tuples():

    data_dir = os.path.abspath('.') + '/data/ds114'
    pipeline_name = 'test_ROITransformer_ds114'

    IDS = [('01', 'retest'), 
           ('02', 'retest'), 
           ('03', 'test')]

    transformer = SkullStrippingTransformer(data_dir=data_dir,
                                            pipeline_name=pipeline_name,
                                            search_param=dict(extensions='T1w.nii.gz'))
    transformer.fit_transform(IDS)

    PM = PathManager(data_dir)

    for subject, session in IDS:

        in_file = PM.get(extensions='T1w.nii.gz',
                         subject=subject,
                         session=session)

        assert len(in_file) == 1
        in_file = in_file[0]

        out_file = PM.make(in_file=in_file,
                           pipeline_name=pipeline_name,
                           derivative='needed_brain')
        dirname = os.path.dirname(out_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        betfsl = BET(in_file=in_file,
                     out_file=out_file)
        betfsl.run()

        res_file = PM.make(in_file=in_file,
                           pipeline_name=pipeline_name,
                           derivative='brain')

        result_mat = nib.load(res_file).affine
        output_mat = nib.load(out_file).affine
        assert np.allclose(result_mat, output_mat)
        os.remove(out_file)
        os.remove(res_file)


def test_skull_stripping_ids_only():

    data_dir = os.path.abspath('.') + '/data/ds114'
    pipeline_name = 'test_ROITransformer_ds114'

    IDS = ['01', '02', '03']

    transformer = SkullStrippingTransformer(data_dir=data_dir,
                                            pipeline_name=pipeline_name,
                                            search_param=dict(extensions='T1w.nii.gz'))
    transformer.fit_transform(IDS)

    PM = PathManager(data_dir)

    for subject in IDS:

        in_files = PM.get(extensions='T1w.nii.gz',
                         subject=subject)
        
        for in_file in in_files:

            out_file = PM.make(in_file=in_file,
                               pipeline_name=pipeline_name,
                               derivative='needed_brain')
            dirname = os.path.dirname(out_file)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            betfsl = BET(in_file=in_file,
                         out_file=out_file)
            betfsl.run()

            res_file = PM.make(in_file=in_file,
                               pipeline_name=pipeline_name,
                               derivative='brain')

            result_mat = nib.load(res_file).affine
            output_mat = nib.load(out_file).affine
            assert np.allclose(result_mat, output_mat)
            os.remove(out_file)
            os.remove(res_file)
