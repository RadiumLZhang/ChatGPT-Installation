# ChatGPT-Installation

## Setup
```
git clone --recurse-submodules git@github.com:RadiumLZhang/ChatGPT-Installation.git
```

If you've already cloned the repository and forgot to include the --recurse-submodules flag, you can initialize and update the submodule with the following commands:
```
git submodule init
git submodule update
```

## Fool Your Friend
"Fool Your Friend" is a Battleship-style game in which you either play as the "Fooler," who generates misleading images, or the "Guesser," who tries to identify which images are AI-generated. 

By employing generative image AI, you'll create images that appear authentic and blend them with ge

1. use conda to create a new environment called env-ssh
```
conda create -n env-ssh python=3.12
```
2. activate the new environment
```
conda activate env-ssh
```
3. install the required packages
```
pip install -r requirements.txt
```
4. set the environment variable
```
export GT_USERNAME=your_username
export GT_PASSWORD=your_password
export GT_DOMAIN=your_domain
```
5. run the script
```
python3 run.py
```

