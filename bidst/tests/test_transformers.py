import os
import sys
import numpy as np
sys.path.insert(0, os.path.abspath('../..'))

import pytest
from bids.grabbids import BIDSLayout
from bidst.transformers import ROITransformer
from bidst.transformers import SkullStrippingTransformer

from nipype.interfaces.fsl import ExtractROI
from nipype.interfaces.fsl import BET
import nibabel as nib

from sklearn.pipeline import Pipeline
from nipype import Node, Workflow
from shutil import rmtree


def get_file_paths_with_sessions():
    project_root = os.path.abspath('.') + '/ds114'
    layout = BIDSLayout(project_root)
    files = layout.get(extensions='.nii.gz', session='retest')
    file_paths = [f.filename for f in files]
    return file_paths


def get_file_paths_without_sessions():
    project_root = os.path.abspath('.') + '/ds114_without_sessions'
    layout = BIDSLayout(project_root)
    files = layout.get(extensions='.nii.gz')
    file_paths = [f.filename for f in files]
    return file_paths


def cut_nii_gz(filename):
    filename = os.path.splitext(filename)[0]
    filename = os.path.splitext(filename)[0]
    return filename


def add_nii_gz(filename):
    return filename + '.nii.gz'


def test_ROITrasformer_with_sessions():
    file_paths = get_file_paths_with_sessions()
    basedir = os.path.abspath('.') + '/ds114'
    result_paths = ROITransformer(label='label', t_min=0, t_size=1, basedir=basedir).fit_transform(file_paths)
    for in_file, result_path in zip(file_paths, result_paths):
        roi_file = add_nii_gz(cut_nii_gz(result_path) + '_needed')
        fslroi = ExtractROI(in_file=in_file,
                            roi_file=roi_file,
                            t_min=0,
                            t_size=1)
        fslroi.run()
        result_mat = nib.load(result_path).affine
        output_mat = nib.load(roi_file).affine
        assert np.allclose(result_mat, output_mat)
        os.remove(result_path)
        os.remove(roi_file)
        print(result_path)
        print(roi_file)


def test_ROITransformer_without_sessions():
    file_paths = get_file_paths_without_sessions()
    basedir = os.path.abspath('.') + '/ds114_without_sessions'
    result_paths = ROITransformer(label='label', t_min=0, t_size=1, basedir=basedir).fit_transform(file_paths)
    for in_file, result_path in zip(file_paths, result_paths):
        roi_file = add_nii_gz(cut_nii_gz(result_path) + '_needed')
        fslroi = ExtractROI(in_file=in_file,
                            roi_file=roi_file,
                            t_min=0,
                            t_size=1)
        fslroi.run()
        result_mat = nib.load(result_path).affine
        output_mat = nib.load(roi_file).affine
        assert np.allclose(result_mat, output_mat)
        os.remove(result_path)
        os.remove(roi_file)
        print(result_path)
        print(roi_file)


def test_SkullStrippingTransformer_with_sessions():
    file_paths = get_file_paths_with_sessions()
    basedir = os.path.abspath('.') + '/ds114'
    result_paths = SkullStrippingTransformer(basedir=basedir).fit_transform(file_paths)
    for in_file, result_path in zip(file_paths, result_paths):
        bet_file = add_nii_gz(cut_nii_gz(result_path) + '_needed')
        fslbet = BET(in_file=in_file,
                     out_file=bet_file)
        fslbet.run()
        result_mat = nib.load(result_path).affine
        output_mat = nib.load(bet_file).affine
        assert np.allclose(result_mat, output_mat)
        os.remove(result_path)
        os.remove(bet_file)
        print(result_path)
        print(bet_file)


def test_SkullStrippingTransformer_without_sessions():
    file_paths = get_file_paths_without_sessions()
    basedir = os.path.abspath('.') + '/ds114_without_sessions'
    result_paths = SkullStrippingTransformer(basedir=basedir).fit_transform(file_paths)
    for in_file, result_path in zip(file_paths, result_paths):
        bet_file = add_nii_gz(cut_nii_gz(result_path) + '_needed')
        fslbet = BET(in_file=in_file,
                     out_file=bet_file)
        fslbet.run()
        result_mat = nib.load(result_path).affine
        output_mat = nib.load(bet_file).affine
        assert np.allclose(result_mat, output_mat)
        os.remove(result_path)
        os.remove(bet_file)
        print(result_path)
        print(bet_file)
