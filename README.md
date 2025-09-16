# Robot Pet 机器猫

## Install Dependencies

```shell
pip insatll -r robot_pet/requirements.txt
```

If you want to generate new requirements.txt, do the following
```shell
cd robot_pet
pip install pipreqs
pipreqs . --encoding=utf-8 --force
```

## Usage 用法

```shell
# copy the config file template and edit it as you like
cp conf/config.yaml.example  conf/config.yaml

# text mode
python robot_pet --chat-type text

# audio mode
python robot_pet --chat-type audio

# robot car mode
python robot_pet --chat-type car
```