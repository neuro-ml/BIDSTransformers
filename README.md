# BIDSTransformers

## Using Docker

You can follow the [Nipype tutorial](https://miykael.github.io/nipype_tutorial/)

or use this dcoker container:

```bash
sudo docker pull nipype/nipype
```

### Running docker:

```bash
sudo docker run -v $PWD/work:/work -it -p 8809:8809 nipype/nipype:latest
```

### Install needed packages into docker

```bash
pip install ipython notebook pybids
```

### Start jupyter notebook into docker

```bash
jupyter notebook --no-browser --ip="*" --allow-root --port 8809
```

You will see message:

```bash
  Copy/paste this URL into your browser when you connect for the first time,
  to login with a token:
    http://localhost:8809/?token=some_token
```
