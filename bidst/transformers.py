import os
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from nipype.interfaces.fsl import ExtractROI
from nipype.interfaces.fsl import BET


def cut_nii_gz(filename):
    filename = os.path.splitext(filename)[0]
    filename = os.path.splitext(filename)[0]
    return filename


def get_session_from_dir(dirname):
    for directory in dirname.split('/'):
        if 'ses-' in directory:
            return directory
    return None


def root_directory(directory):
    neardirs = os.listdir(directory)
    for neardir in neardirs:
        if 'sub-' in neardir:
            return True
    return False


def build_directory(dirname, self):
    rec_type = dirname.split('/')[-1]
   
    if 'ses-' in dirname:
        session = get_session_from_dir(dirname)
        dirname = self.basedir
        dirname += '/derivatives'
        dirname += '/{}/'.format(self.__class__.__name__)
        dirname += '{}/'.format(rec_type)
        dirname += '{}/'.format(session)

    else:
        
        dirname = self.basedir
        dirname += '/derivatives'
        dirname += '/{}/'.format(self.__class__.__name__)
        dirname += '{}/'.format(rec_type)

    return dirname


def build_filepath_for_ROI(dirname, filename, self):
    roi_file = dirname + cut_nii_gz(filename)

    if self.space is not None:
        roi_file += '_space-{}'.format(self.space)

    if self.variant is not None:
        roi_file += '_variant-{}'.format(self.variant)

    roi_file += '_label-{}'.format(self.label)
    roi_file = os.path.abspath(roi_file) + '.nii.gz'
    return roi_file


def build_filepath_for_BET(dirname, filename, self):
    bet_file = dirname + cut_nii_gz(filename)

    if self.space is not None:
        bet_file += '_space-{}'.format(self.space)

    if self.variant is not None:
        bet_file += '_variant-{}'.format(self.variant)

    bet_file = os.path.abspath(bet_file) + '.nii.gz'
    return bet_file
    

class ROITransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, label, basedir=os.path.abspath('.'), space=None, variant=None, **params):
        self.space = space
        self.variant = variant
        self.label = label
        self.params = params
        self.basedir = basedir
    
    def fit(self, filepaths, y=None, **fit_params):
        return self

    def transform(self, filepaths, y=None):
        filepaths = filepaths.copy()
        out_files = []
        for in_file in filepaths:
            filename = os.path.basename(in_file)
            dirname = os.path.dirname(in_file)
            dirname = build_directory(dirname, self)
            if not os.path.exists(dirname):
                    os.makedirs(dirname)

            roi_file = build_filepath_for_ROI(dirname, filename, self)
            out_files.append(roi_file)
            
            fslroi = ExtractROI(in_file=in_file,
                                roi_file=roi_file,
                                **self.params)
            fslroi.run()

        return out_files


class SkullStrippingTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, basedir=os.path.abspath('.'), space=None, variant=None):
        self.space = space
        self.variant = variant
        self.basedir = basedir
    
    def fit(self, filepaths, y=None, **fit_params):
        return self

    def transform(self, filepaths, y=None):
        filepaths = filepaths.copy()
        out_files = []
        for in_file in filepaths:
            filename = os.path.basename(in_file)
            dirname = os.path.dirname(in_file)
            dirname = build_directory(dirname, self)
            if not os.path.exists(dirname):
                    os.makedirs(dirname)

            bet_file = build_filepath_for_BET(dirname, filename, self)
            out_files.append(bet_file)
            
            fslbet = BET(in_file=in_file,
                         out_file=bet_file)
            fslbet.run()

        return out_files
