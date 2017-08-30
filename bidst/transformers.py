import pandas as pd
import os
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

from bids.grabbids import BIDSLayout

from nipype.interfaces.fsl import ExtractROI
from nipype.interfaces.fsl import BET
from nipype.interfaces.fsl import FLIRT
from nipype.interfaces.fsl import FNIRT
from nipype.interfaces.fsl import FAST
from nipype.interfaces.ants import N4BiasFieldCorrection


def get_brain_filename(filename):
    index = filename.find('_T1w') + 4
    filename = filename[:index] + '_brain.nii.gz'
    return filename

def get_nu_filename(filename):
    index = filename.find('_T1w') + 4
    filename = filename[:index] + '_nu.nii.gz'
    return filename


def get_destination_path_for_fast(step_dir, filepath_source):
    path, filename = os.path.split(filepath_source)
    path, directory = os.path.split(path)

    inner_structure_path = list()
    inner_structure_path.append(directory)
    while 'sub-' not in directory:
        path, directory = os.path.split(path)
        inner_structure_path.append(directory)
    inner_structure_path = reversed(inner_structure_path) 

    print('Renaming filename: {}'.format(filename))
    if 'pve_0' in filename:
        filename = filename.replace('pve_0', 'class-CSF_probtissue')
    if 'pve_1' in filename:
        filename = filename.replace('pve_1', 'class-GM_probtissue')
    if 'pve_2' in filename:
        filename =filename.replace('pve_2', 'class-WM_probtissue')
    print('New filename: {}'.format(filename))

    destination_dir = os.path.join(step_dir,
                                    *inner_structure_path)

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    destination_file = os.path.join(destination_dir,
                                    filename)

    return destination_file


class TissueSegmentation(BaseEstimator, TransformerMixin):

    def __init__(
            self,
            pipeline_name,
            project_path,
            gather_steps=dict(),
            backend='fsl',
            backend_param=dict(),
            transformer_name='tissuesegmentation'):

        self.pipeline_name = pipeline_name
        self.project_path = project_path
        self.gather_steps = gather_steps
        self.backend = backend
        self.backend_param = backend_param
        self.transformer_name = transformer_name

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):

        in_files_search_param = self.gather_steps[1]

        if type(X[0]) == str and  \
           self.backend == 'fsl' and \
           self.gather_steps[0] != 'source':

            in_files_dir = os.path.join(self.project_path,
                                        'derivatives',
                                        self.pipeline_name,
                                        'steps',
                                        self.gather_steps[0])

            layout = BIDSLayout(in_files_dir)

            X.copy()

            for subject in X:
                
                in_files = []
                for path in layout.get(subject=subject,
                                       **in_files_search_param):
                    path = path.filename
                    in_files.append(path)

                for in_file in in_files:

                    dirname = os.path.dirname(in_file)
                    prev_files = os.listdir(dirname)

                    fastfsl = FAST(in_files=in_file,
                                   **self.backend_param)
                    fastfsl.run()

                    step_dir = os.path.join(self.project_path,
                                            'derivatives',
                                            self.pipeline_name,
                                            'steps',
                                            self.transformer_name)

                    curr_files = os.listdir(dirname)
                    for dir_file in curr_files:
                        if dir_file not in prev_files:
                            filepath_source = os.path.join(dirname,
                                                           dir_file)
                            filepath_destination = get_destination_path_for_fast(
                                                        step_dir,
                                                        filepath_source)
                            os.rename(filepath_source, filepath_destination)


        elif type(X[0]) == str and \
             self.backend == 'fsl' and \
             self.gather_steps[0] == 'source':

            in_files_dir = self.project_path

            layout = BIDSLayout(in_files_dir)

            X = X.copy()

            for subject in X:
                print('\n\nSUBJECT: {}'.format(subject))

                in_files = []
                for path in layout.get(subject=subject,
                                       **in_files_search_param):
                    path = path.filename
                    if 'derivatives' not in path.split(os.sep):
                        in_files.append(path)

                for in_file in in_files:
                    print('in_file: {}'.format(in_file))

                    dirname = os.path.dirname(in_file)
                    prev_files = os.listdir(dirname)

                    print('prev_files: {}'.format(prev_files))
                    print('Processing...')

                    fastfsl = FAST(in_files=in_file,
                                   **self.backend_param)
                    fastfsl.run()

                    step_dir = os.path.join(self.project_path,
                                            'derivatives',
                                            self.pipeline_name,
                                            'steps',
                                            self.transformer_name)

                    curr_files = os.listdir(dirname)

                    print('step_dir: {}'.format(step_dir))
                    print('curr_files: {}'.format(curr_files))

                    for dir_file in curr_files:
                        if dir_file not in prev_files:
                            filepath_source = os.path.join(dirname,
                                                           dir_file)
                            filepath_destination = get_destination_path_for_fast(
                                                        step_dir,
                                                        filepath_source)

                            print('filepath_source: {}'.format(filepath_source))
                            print('filepath_destination: {}'.format(filepath_destination))

                            os.rename(filepath_source, filepath_destination)

        return X
            

class SkullStrippingTransformer(BaseEstimator, TransformerMixin):

    def __init__(
            self,
            pipeline_name,
            project_path,
            gather_steps=dict(),
            backend='fsl',
            backend_param=dict(),
            transformer_name='skullstripping'):

        self.pipeline_name = pipeline_name
        self.project_path = project_path
        self.gather_steps = gather_steps
        self.backend = backend
        self.backend_param = backend_param
        self.transformer_name = transformer_name

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):

        in_files_search_param = self.gather_steps[1]

        if type(X[0]) == str and  \
           self.backend == 'fsl' and \
           self.gather_steps[0] != 'source':

            in_files_dir = os.path.join(self.project_path,
                                        'derivatives',
                                        self.pipeline_name,
                                        'steps',
                                        self.gather_steps[0])

            layout = BIDSLayout(in_files_dir)

            X.copy()

            for subject in X:
                
                in_files = []
                for path in layout.get(subject=subject,
                                       **in_files_search_param):
                    path = path.filename
                    in_files.append(path)

                for in_file in in_files:

                    path, filename = os.path.split(in_file)
                    path, directory = os.path.split(path)

                    inner_structure_path = list()
                    inner_structure_path.append(directory)
                    while 'sub-' not in directory:
                        path, directory = os.path.split(path)
                        inner_structure_path.append(directory)
                    inner_structure_path = reversed(inner_structure_path)

                    out_dir = os.path.join(self.project_path,
                                           'derivatives',
                                           self.pipeline_name,
                                           'steps',
                                           self.transformer_name,
                                           *inner_structure_path)

                    if not os.path.exists(out_dir):
                        os.makedirs(out_dir)

                    out_filename = get_nu_filename(filename)
                    out_file = os.path.join(out_dir,
                                            out_filename)

                    betfsl = BET(in_file=in_file,
                                 out_file=out_file,
                                 **self.backend_param)
                    betfsl.run()

        if type(X[0]) == str and  \
           self.backend == 'fsl' and \
           self.gather_steps[0] == 'source':
        
            in_files_dir = self.project_path

            layout = BIDSLayout(in_files_dir)

            X = X.copy()

            for subject in X:

                in_files = []
                for path in layout.get(subject=subject,
                                       **in_files_search_param):
                    path = path.filename
                    if 'derivatives' not in path.split(os.sep):
                        in_files.append(path)

                for in_file in in_files:
                    
                    path, filename = os.path.split(in_file)
                    path, directory = os.path.split(path)

                    inner_structure_path = list()
                    inner_structure_path.append(directory)
                    while 'sub-' not in directory:
                        path, directory = os.path.split(path)
                        inner_structure_path.append(directory)
                    inner_structure_path = reversed(inner_structure_path)

                    out_dir = os.path.join(self.project_path,
                                           'derivatives',
                                           self.pipeline_name,
                                           'steps',
                                           self.transformer_name,
                                           *inner_structure_path)

                    if not os.path.exists(out_dir):
                        os.makedirs(out_dir)

                    out_filename = get_brain_filename(filename)
                    out_file = os.path.join(out_dir,
                                            out_filename)
                    print(out_file)

                    betfsl = BET(in_file=in_file,
                                 out_file=out_file,
                                 **self.backend_param)
                    betfsl.run()

        return X


class StatAggregator(BaseEstimator, TransformerMixin):
    
    def __init__(
            self,
            function,
            pipeline_name,
            project_path,
            gather_steps=dict(),
            transformer_name='stataggregator'):

        self.function = function
        self.pipeline_name = pipeline_name
        self.project_path = project_path
        self.gather_steps = gather_steps
        self.transformer_name = transformer_name

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):

        agg_results = dict()
        in_files_search_param = self.gather_steps[1]

        if type(X[0]) == str and  \
           self.gather_steps[0] != 'source':
            """
            in_files_dir = os.path.join(self.project_path,
                                        'derivatives',
                                        self.pipeline_name,
                                        'steps',
                                        self.gather_steps[0])
            print(in_files_dir)
            """
            layout = BIDSLayout(self.project_path)

            X.copy()

            for subject in X:
                print('SUBJECT {}'.format(subject))
                
                in_files = layout.get(subject=subject,
                                     **in_files_search_param)
                print(in_files_search_param)
                print(in_files)
                sessions = []
                dirnames = []
                for in_file in in_files:
                    print('in_file {}'.format(in_file))
                    path, filename = os.path.split(in_file.filename)
                    session = filename.split('_')[1][4:]
                    if session not in sessions:
                        sessions.append(session)
                    print('session {}'.format(session))
                        
                    if path not in dirnames:
                        dirnames.append(path)
                    print('path {}'.format(path))

                for dirname, session in zip(dirnames, sessions):

                    agg_results[(subject, session)] = self.function(dirname)

        return pd.DataFrame(agg_results).T


class NUCorrectionTransformer(BaseEstimator, TransformerMixin):

    def __init__(
            self,
            pipeline_name,
            project_path,
            gather_steps=dict(),
            backend='ants',
            backend_param=dict(),
            transformer_name='nucorrection'):

        self.pipeline_name = pipeline_name
        self.project_path = project_path
        self.gather_steps = gather_steps
        self.backend = backend
        self.backend_param = backend_param
        self.transformer_name = transformer_name

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):

        in_files_search_param = self.gather_steps[1]

        if type(X[0]) == str and  \
           self.backend == 'ants' and \
           self.gather_steps[0] != 'source':

            in_files_dir = os.path.join(self.project_path,
                                        'derivatives',
                                        self.pipeline_name,
                                        'steps',
                                        self.gather_steps[0])

            layout = BIDSLayout(in_files_dir)

            X.copy()

            for subject in X:
                
                in_files = []
                for path in layout.get(subject=subject,
                                       **in_files_search_param):
                    path = path.filename
                    in_files.append(path)

                for in_file in in_files:

                    path, filename = os.path.split(in_file)
                    path, directory = os.path.split(path)

                    inner_structure_path = list()
                    inner_structure_path.append(directory)
                    while 'sub-' not in directory:
                        path, directory = os.path.split(path)
                        inner_structure_path.append(directory)
                    inner_structure_path = reversed(inner_structure_path)

                    out_dir = os.path.join(self.project_path,
                                           'derivatives',
                                           self.pipeline_name,
                                           'steps',
                                           self.transformer_name,
                                           *inner_structure_path)

                    if not os.path.exists(out_dir):
                        os.umask(0)
                        os.makedirs(out_dir)

                    out_filename = get_brain_filename(filename)
                    out_file = os.path.join(out_dir,
                                            out_filename)

                    nuants = N4BiasFieldCorrection()
                    nuants.inputs.input_image = in_file
                    nuants.inputs.output_image = out_file
                    nuants.run()

        if type(X[0]) == str and  \
           self.backend == 'ants' and \
           self.gather_steps[0] == 'source':
        
            in_files_dir = self.project_path

            layout = BIDSLayout(in_files_dir)

            X = X.copy()

            for subject in X:

                in_files = []
                for path in layout.get(subject=subject,
                                       **in_files_search_param):
                    path = path.filename
                    if 'derivatives' not in path.split(os.sep):
                        in_files.append(path)

                for in_file in in_files:
                    
                    path, filename = os.path.split(in_file)
                    path, directory = os.path.split(path)

                    inner_structure_path = list()
                    inner_structure_path.append(directory)
                    while 'sub-' not in directory:
                        path, directory = os.path.split(path)
                        inner_structure_path.append(directory)
                    inner_structure_path = reversed(inner_structure_path)

                    out_dir = os.path.join(self.project_path,
                                           'derivatives',
                                           self.pipeline_name,
                                           'steps',
                                           self.transformer_name,
                                           *inner_structure_path)

                    if not os.path.exists(out_dir):
                        os.umask(0)
                        os.makedirs(out_dir)

                    out_filename = get_nu_filename(filename)
                    out_file = os.path.join(out_dir,
                                            out_filename)
                    print(out_file)

                    nuants = N4BiasFieldCorrection()
                    nuants.inputs.input_image = in_file
                    nuants.inputs.output_image = out_file
                    nuants.run()

        return X


class LinearRegistrationTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self):
        return self

    def transform(self, X):
        return X


class NonLinearRegistrationTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self):
        return self

    def transform(self, X):
        return X
