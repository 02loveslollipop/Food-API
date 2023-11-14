# Food Recomendation System API

> A python API to exchange data between the Flutter Front-end, the MongoDB and and the FRS AI model.

## Food Recomendation System
This repository is part of the Food Recomendation system project, the remaining repositories are listed below:

- [Flutter Front-end](https://github.com/Arroyave03/FRS-Front)

- [AI Model](https://github.com/faendal/FoodRecomendationSystem)

## Installation
To setup this repository you need to have python 3.11 installed in your machine, then you can install the dependencies with the following command:

1. Clone the repository
```bash
git clone https://github.com/02loveslollipop/Food-API.git
```

2. Create a python 3.11 environment using Conda (**Optional**)

```bash
conda create -n <env_name> python=3.11
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. copy the example_config.yaml file and rename it to config.yaml

```bash
cp example_config.yaml config.yaml
```

5. Edit the config.yaml file with your Configuration

6. Run the API

```bash
python main.py
```

## Note

This API is not intended to be used in production, it is only for testing purposes.

As the API is intended to be used in a local network, it does not have any security measures, so it is not recommended to use it in a public network.

To use the API you must execute also the MongoDB server and the [AI model](https://github.com/faendal/FoodRecomendationSystem).

## License
[MIT](https://choosealicense.com/licenses/mit/)

