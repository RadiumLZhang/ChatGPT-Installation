# ChatGPT-Installation

## Fool Your Friend
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

