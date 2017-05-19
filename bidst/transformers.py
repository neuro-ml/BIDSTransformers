import os
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from nipype.interfaces.fsl import ExtractROI
from nipype.interfaces.fsl import BET
from bids.grabbids import BIDSLayout


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
        dirname += '{}/'.format(session)
        dirname += '{}/'.format(rec_type)

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

    bet_file += '_label-{}'.format(self.label)
    bet_file = os.path.abspath(bet_file) + '.nii.gz'
    return bet_file


def run_fsl_roi(in_file, self):
    filename = os.path.basename(in_file)
    dirname = os.path.dirname(in_file)
    dirname = build_directory(dirname, self)
    if not os.path.exists(dirname):
            os.makedirs(dirname)

    roi_file = build_filepath_for_ROI(dirname, filename, self)
    
    fslroi = ExtractROI(in_file=in_file,
                        roi_file=roi_file,
                        t_min=0,
                        t_size=1)
    fslroi.run()
    

class ROITransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, label, basedir=os.path.abspath('.'), space=None,
            variant=None, **params):
        self.space = space
        self.variant = variant
        self.label = label
        self.params = params
        self.basedir = basedir
        self.layout = BIDSLayout(basedir)
    
    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):

        assert type(X) == list

        if type(X[0]) == tuple:
            
            X = X.copy()
            for subject, session in X:
                in_file = self.layout.get(subject=subject, session=session, **self.params)[0].filename
                run_fsl_roi(in_file, self)

        elif type(X[0]) == str:

            X = X.copy()
            for subject in X:
                in_file = self.layout.get(subject=subject, **self.params)[0].filename

        return X


def run_fsl_bet(in_file, self):
    filename = os.path.basename(in_file)
    dirname = os.path.dirname(in_file)
    dirname = build_directory(dirname, self)
    if not os.path.exists(dirname):
            os.makedirs(dirname)

    bet_file = build_filepath_for_BET(dirname, filename, self)
    
    fslbet = BET(in_file=in_file,
                 out_file=bet_file)
    fslbet.run()


class SkullStrippingTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, basedir=os.path.abspath('.'), space=None, variant=None, label=None, **params):
        self.space = space
        self.variant = variant
        self.basedir = basedir
        self.layout = BIDSLayout(basedir)
        self.params = params
        self.label = label
    
    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):

        assert type(X) == list

        if type(X[0]) == tuple:

            X = X.copy()
            for subject, session in X:
                in_file = self.layout.get(subject=subject, session=session, **self.params)

                if self.label is not None:
                    for File in in_file:
                        if '_label-{}'.format(self.label) in File.filename:
                            in_file = File

                if type(in_file) == list:
                    in_file = in_file[0].filename
                else:
                    in_file = in_file.filename

                run_fsl_bet(in_file, self)

        elif type(X[0]) == str:

            X = X.copy()
            for subject in X:

                in_file = self.layout.get(subject=subject, **self.params)

                if self.label is not None:
                    for File in in_file:
                        if '_label-{}'.format(self.label) in File.filename:
                            in_file = File

                if type(in_file) == list:
                    in_file = in_file[0].filename
                else:
                    in_file = in_file.filename

                run_fsl_bet(in_file, self)

        return X
