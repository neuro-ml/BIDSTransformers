import os
from bids.grabbids import BIDSLayout


class PathManager(object):

    def __init__(self, basedir):

        self.basedir = basedir
        self.layout = BIDSLayout(basedir)

    def get(self, **params):

        paths = list()
        for path in self.layout.get(**params):
            paths.append(path.filename)
        return paths

    def make(
            self,
            in_file,
            pipeline_name,
            derivative,
            tags=None,
            extension=None):

        pipeline_dir = os.path.join(self.basedir, 'derivatives', pipeline_name)
        path, filename = os.path.split(in_file)

        inner_structure_path = list()
        while path != self.basedir:
            path, dir = os.path.split(path)
            inner_structure_path.append(dir)
        inner_structure_path = reversed(inner_structure_path)

        if extension:
            filename, _ = os.path.splitext(filename)

            if _ == '.gz':
                filename, _ = os.path.splitext(filename)
        else:
            filename, extension = os.path.splitext(filename)

            if extension == '.gz':
                filename, subextension = os.path.splitext(filename)
                extension = subextension + extension

        if tags:
            tags_str = ''
            for tag_name, tag_value in tags:
                tags_str += '_{}-{}'.format(tag_name, tag_value)
            filename += '{}_{}{}'.format(tags_str, derivative, extension)
        else:
            filename += '_{}{}'.format(derivative, extension)

        out_file = os.path.join(pipeline_dir,
                                *inner_structure_path,
                                filename)
        return out_file
