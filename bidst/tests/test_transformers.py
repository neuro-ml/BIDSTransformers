import os
import sys
import numpy as np
sys.path.insert(0, os.path.abspath('../..'))

import pytest

import bidst
from bidst.transformers import NUCorrectionTransformer
from bidst.transformers import SkullStrippingTransformer
from bidst.transformers import LinearRegistrationTransformer
from bidst.transformers import NonLinearRegistrationTransformer

from nipype.interfaces.fsl import BET
from nipype.interfaces.fsl import FLIRT
from nipype.interfaces.fsl import FNIRT
from nipype.interfaces.ants import N4BiasFieldCorrection

import nibabel as nib


def build_T1w_in_file_path(data_dir, subject, session):

    return data_dir + \
        '/sub-{}/ses-{}/anat/sub-{}_ses-{}_T1w.nii.gz'.format(
            subject, session,
            subject, session)


def build_T1w_out_file_path(
        data_dir,
        pipeline_name,
        subject,
        session,
        variant,
        derivative):

    full_path = '{}/derivatives/{}/' + \
                'sub-{}/ses-{}/anat/' + \
                'sub-{}_ses-{}_T1w_variant-{}_{}.nii.gz'

    return full_path.format(data_dir,
                            pipeline_name,
                            subject, session,
                            subject, session,
                            variant,
                            derivative)


def test_skull_stripping_tuples():

    data_dir = os.path.abspath('.') + '/data/ds114'
    pipeline_name = 'test_skullStrippingTransformer_ds114'

    IDS = [('01', 'retest'),
           ('02', 'retest'),
           ('03', 'test')]

    transformer = SkullStrippingTransformer(
        data_dir=data_dir,
        pipeline_name=pipeline_name,
        search_param=dict(
            extensions='T1w.nii.gz'),
        variant='skullStrippingTuples')
    transformer.fit_transform(IDS)

    for subject, session in IDS:

        in_file = build_T1w_in_file_path(data_dir,
                                         subject,
                                         session)

        out_file = build_T1w_out_file_path(data_dir,
                                           pipeline_name,
                                           subject,
                                           session,
                                           'skullStrippingTuples',
                                           'neededBrain')

        dirname = os.path.dirname(out_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        betfsl = BET(in_file=in_file,
                     out_file=out_file)
        betfsl.run()

        res_file = build_T1w_out_file_path(data_dir,
                                           pipeline_name,
                                           subject,
                                           session,
                                           'skullStrippingTuples',
                                           'brain')

        result_mat = nib.load(res_file).affine
        output_mat = nib.load(out_file).affine
        assert np.allclose(result_mat, output_mat)
        os.remove(res_file)
        os.remove(out_file)


def test_skull_stripping_ids_only():

    data_dir = os.path.abspath('.') + '/data/ds114'
    pipeline_name = 'test_skullStrippingTransformer_ds114'

    IDS = ['01', '02', '03']
    sessions = ['test', 'retest']

    transformer = SkullStrippingTransformer(
        data_dir=data_dir,
        pipeline_name=pipeline_name,
        search_param=dict(
            extensions='T1w.nii.gz'),
        variant='skullStrippingIDsOnly')
    transformer.fit_transform(IDS)

    for subject in IDS:
        for session in sessions:

            in_file = build_T1w_in_file_path(data_dir,
                                             subject,
                                             session)

            out_file = build_T1w_out_file_path(data_dir,
                                               pipeline_name,
                                               subject,
                                               session,
                                               'skullStrippingIDsOnly',
                                               'neededBrain')

            dirname = os.path.dirname(out_file)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            betfsl = BET(in_file=in_file,
                         out_file=out_file)
            betfsl.run()
            
            res_file = build_T1w_out_file_path(data_dir,
                                               pipeline_name,
                                               subject,
                                               session,
                                               'skullStrippingIDsOnly',
                                               'brain')

            result_mat = nib.load(res_file).affine
            output_mat = nib.load(out_file).affine
            assert np.allclose(result_mat, output_mat)
            os.remove(res_file)
            os.remove(out_file)


def test_nu_correction_tuples():

    data_dir = os.path.abspath('.') + '/data/ds114'
    pipeline_name = 'test_nuCorrectionTransformer_ds114'

    IDS = [('01', 'retest'),
           ('02', 'retest'),
           ('03', 'test')]

    transformer = NUCorrectionTransformer(
        data_dir=data_dir,
        pipeline_name=pipeline_name,
        search_param=dict(
            extensions='T1w.nii.gz'),
        variant='nuCorrectionTuples')
    transformer.fit_transform(IDS)

    for subject, session in IDS:

        in_file = build_T1w_in_file_path(data_dir,
                                         subject,
                                         session)

        out_file = build_T1w_out_file_path(data_dir,
                                           pipeline_name,
                                           subject,
                                           session,
                                           'nuCorrectionTuples',
                                           'neededNu')

        dirname = os.path.dirname(out_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        nuants = N4BiasFieldCorrection()
        nuants.inputs.input_image = in_file
        nuants.inputs.output_image = out_file
        nuants.run()

        res_file = build_T1w_out_file_path(data_dir,
                                           pipeline_name,
                                           subject,
                                           session,
                                           'nuCorrectionTuples',
                                           'nu')

        result_mat = nib.load(res_file).affine
        output_mat = nib.load(out_file).affine
        assert np.allclose(result_mat, output_mat)
        os.remove(res_file)
        os.remove(out_file)


def test_nu_correction_ids_only():

    data_dir = os.path.abspath('.') + '/data/ds114'
    pipeline_name = 'test_nuCorrectionTransformer_ds114'

    IDS = ['01', '02', '03']
    sessions = ['test', 'retest']

    transformer = NUCorrectionTransformer(
        data_dir=data_dir,
        pipeline_name=pipeline_name,
        search_param=dict(
            extensions='T1w.nii.gz'),
        variant='nuCorrectionIDsOnly')
    transformer.fit_transform(IDS)

    for subject in IDS:
        for session in sessions:

            in_file = build_T1w_in_file_path(data_dir,
                                             subject,
                                             session)

            out_file = build_T1w_out_file_path(data_dir,
                                               pipeline_name,
                                               subject,
                                               session,
                                               'nuCorrectionIDsOnly',
                                               'neededNu')

            dirname = os.path.dirname(out_file)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            nuants = N4BiasFieldCorrection()
            nuants.inputs.input_image = in_file
            nuants.inputs.output_image = out_file
            nuants.run()
            
            res_file = build_T1w_out_file_path(data_dir,
                                               pipeline_name,
                                               subject,
                                               session,
                                               'nuCorrectionIDsOnly',
                                               'nu')

            result_mat = nib.load(res_file).affine
            output_mat = nib.load(out_file).affine
            assert np.allclose(result_mat, output_mat)
            os.remove(res_file)
            os.remove(out_file)
