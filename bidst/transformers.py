import os
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

from .path_manager import PathManager

from nipype.interfaces.fsl import ExtractROI
from nipype.interfaces.fsl import BET
from nipype.interfaces.fsl import FLIRT
from nipype.interfaces.fsl import FNIRT
from nipype.interfaces.ants import N4BiasFieldCorrection


class SkullStrippingTransformer(BaseEstimator, TransformerMixin):
    
    def __init__(
            self,
            pipeline_name,
            data_dir,
            search_param=dict(),
            transform_param=dict(),
            space=None,
            variant=None):

        self.pipeline_name = pipeline_name
        self.data_dir = data_dir
        self.search_param = search_param
        self.transform_param = transform_param

        self.tags = list()
        if space:
            self.tags.append( ('space', space) )
        if variant:
            self.tags.append( ('variant', variant) )
        if self.tags == list():
            self.tags = None

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):
        
        PM = PathManager(self.data_dir)

        if type(X[0]) == tuple:

            X = X.copy()

            for subject, session in X:

                in_file = PM.get(subject=subject,
                                 session=session,
                                 **self.search_param)
                assert len(in_file) == 1
                in_file = in_file[0]

                out_file = PM.make(in_file=in_file,
                                   pipeline_name=self.pipeline_name,
                                   derivative='brain',
                                   tags=self.tags)

                dirname = os.path.dirname(out_file)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                betfsl = BET(in_file=in_file,
                             out_file=out_file,
                             **self.transform_param)
                betfsl.run()

        elif type(X[0]) == str:
            
            X = X.copy()

            for subject in X:

                in_files = PM.get(subject=subject,
                                 **self.search_param)

                for in_file in in_files:

                    out_file = PM.make(in_file=in_file,
                                       pipeline_name=self.pipeline_name,
                                       derivative='brain',
                                       tags=self.tags)

                    dirname = os.path.dirname(out_file)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)

                    betfsl = BET(in_file=in_file,
                                 out_file=out_file,
                                 **self.transform_param)
                    betfsl.run()

        return X


class NUCorrectionTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):
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
