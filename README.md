# BIDSTransformers

This is a very basic proof of concept of BIDS Transformers.
It implements two BIDS Transformers: one based on FSL ROI extractor and second based on FSL Skull Stripping.
Example notebook is [BIDS_Transformers.ipynb](https://github.com/neuro-ml/BIDSTransformers/blob/master/BIDS_Transformers.ipynb).
To run this notebook you will need the following:

1. Clone this [repository](https://github.com/neuro-ml/BIDSTransformers)
2. Working Nipype [installation](https://github.com/nipy/nipype). You can also use docker container (see instructions below).
3. [PyBIDS package](https://github.com/INCF/pybids) (pip install pybids)
4. Download data folder from one of the following links and put it into the folder `/bidst/tests/data`

* [Link1](https://drive.google.com/drive/folders/0B6U5KQalulfAOXlHYkdIa25QbG8?usp=sharing)
* [Link2](https://www.dropbox.com/sh/kh5vkp5s5n6eebh/AABejlvSqHV1HhFy91r9nrT8a?dl=0)

## Installing Nipype 

You can follow the [Nipype tutorial](https://miykael.github.io/nipype_tutorial/)

## Using docker

### Getting nipype container:

```bash
sudo docker pull nipype/nipype
```

### Running docker:

```bash
sudo docker run -v $PWD/work:/work -it -p 8809:8809 nipype/nipype:latest
```

### Installing needed packages in the docker:

```bash
pip install ipython notebook pybids
```

### Starting jupyter notebook in the docker:

```bash
jupyter notebook --no-browser --ip="*" --allow-root --port 8809
```

You will see message:

```bash
  Copy/paste this URL into your browser when you connect for the first time,
  to login with a token:
    http://localhost:8809/?token=some_token
```

You will need to open this url in your browser and copy the token.
