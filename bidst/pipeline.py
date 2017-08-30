from sklearn.pipeline import Pipeline

class BIDSPipeline(Pipeline):
    def __init__(self, steps, pipeline_name, project_path, memory=None):
        super().__init__(steps)
        self.pipeline_name = pipeline_name
        self.project_path = project_path
        # shallow copy of steps
        #self.steps = tosequence(steps)
        self._validate_steps()
        self._set_step_names()
        self._set_pipeline_name()
        self._set_project_path()


    def _set_step_names(self):
        for step in self.steps:
            #print(step)
            step[1].transformer_name = step[0]

    def _set_pipeline_name(self):
        for step in self.steps:
            #print(step)
            step[1].pipeline_name = self.pipeline_name

    def _set_project_path(self):
        for step in self.steps:
            #print(step)
            step[1].project_path = self.project_path
