# Stable Diffusion

Background: [https://huggingface.co/blog/stable\_diffusion](https://huggingface.co/blog/stable_diffusion)

Main project: [https://github.com/CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)

Optimized for GPU's with lower RAM: [https://github.com/basujindal/stable-diffusion](https://github.com/basujindal/stable-diffusion)

<div id="bkmrk-run-the-stablediffus"><div><div class="aui-page-panel"><div class="view"><div class="wiki-content group">- run the stablediffusion command from inside the optimizedSD folder to use the optimized version
- this code was the only one that would run on an 8GB 1080TI
- resolution still has to be capped at around 500x500 for the process to complete instead of hitting its VRAM limit and exiting


**Installation process:**

Stable Diffusion is built off of Python and makes use of the project's Anaconda environment. Prerequisite software includes Anaconda (from conda.io) and git. Anaconda environments are designed to run from a user's home directory, so the installation notes below describe a per-user setup that each user needs to complete for themselves.

### Install dependencies and prerequisites:

\# apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6  
\# apt install git

created /ckpt at the root level as a place to store model checkpoints for users to access  
downloaded the recommended checkpoint file from HuggingFace [https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt)

### Per-user setup:

<div id="bkmrk-install-anaconda%3Ahtt"><div><div class="aui-page-panel"><div class="view"><div class="wiki-content group">1. Install Anaconda****:**** [https://docs.anaconda.com/anaconda/install/linux/](https://docs.anaconda.com/anaconda/install/linux/)
    1. $ wget [https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86\_64.sh](https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh)
    2. $ ./Anaconda3-2022.10-Linux-x86\_64.sh  accept the license agreement; when prompted to run conda init, type yes  
         anaconda installs by default into /home/YOUR ACCOUNT/anaconda3
    3. close and reopen your terminal and/or SSH session to reload your .bashrc, or do   
        $ source ~/.bashrc
    4. $ export PATH=~/anaconda3/bin:$PATH
    5. $ conda init bash
    6. You should now see the phrase (base) before your username at the prompt. This indicates that you're in the default conda environment, and that Anaconda is installed and active on your account. For verification, open the Python prompt and note whether the info it displays on startup includes "Anaconda." To exit the Python shell, type exit() or quit()
2. Clone the project into ~/stable-diffusion and create the Python environment, using the project's included environment.yaml file: 
    1. $ git clone [https://github.com/CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)
    2. $ cd ~/stable-diffusion
    3. conda env create -f environment.yaml  
        Be aware: this downloads **13GB of Python packages** into ~/anaconda3/envs/ldm
3. Checkpoint v. 1-4 file has been downloaded from the HuggingFace repo (link above) and placed into /ckpt with group read permissions 
    1. $ cd ~/stable-diffusion/models
    2. $ mkdir -p ldm/stable-diffusion-v1/
    3. $ cd ldm/stable-diffusion-v1
    4. $ ln -s /ckpt/sd v1-4.ckpt model.ckpt

</div></div></div></div></div>**Test the software with a prompt:**

<div id="bkmrk-%24-cd-%7E%2Fstable-diffus"><div><div class="aui-page-panel"><div class="view"><div class="wiki-content group">1. $ conda bash (to activate the base python environment)
2. $ cd ~/stable-diffusion
3. $ conda activate ldm
4. $ python scripts/txt2img.py --prompt "A wooly mammoth riding a penny-farthing bicycle in Paris. The sun is shining but it's raining. The streets are made of cobblestone." --plms  the script will place the output files in ~/stable-diffusion/outputs/txt2img-samples
</div></div></div></div></div>**To download the output files,** use an official copy of FileZilla (from https://filezilla-project.org -- copies hosted elsewhere may contain malware) or your favorite reputable sFTP program. Connection info is the same as for SSH:

Reminder: SSH/SFTP and port 22 are available from VPN only!

hostname: gpu-stats-20212.iac.gatech.edu  
username: (your GT username)  
password: (your GT password)  
port: 22

### Troubleshooting:

**If the script reports "no CUDA GPUs are available"**

sources:  
[https://stackoverflow.com/questions/70148547/wsl2-pytorch-runtimeerror-no-cuda-gpus-are-available-with-rtx3080](https://stackoverflow.com/questions/70148547/wsl2-pytorch-runtimeerror-no-cuda-gpus-are-available-with-rtx3080)  
[https://www.nvidia.com/Download/index.aspx?lang=en-us](https://www.nvidia.com/Download/index.aspx?lang=en-us)

Had to remove the default nvidia drivers and CUDA libraries I installed on GPU-Stats-2021 and reinstall. The cuda toolkit previously installed wasn't happy with either the A100 cards or the version of PyTorch vended in the Stable Diffusion python env.


apt-get remove --purge nvidia\*  
wget [https://us.download.nvidia.com/tesla/525.60.13/NVIDIA-Linux-x86\_64-525.60.13.run](https://us.download.nvidia.com/tesla/525.60.13/NVIDIA-Linux-x86_64-525.60.13.run)

**Version 525.60.13 with CUDA 12 support works with this version of the Stable Diffusion project. This may change in the future.**

**If calling conda activate gives an error:**

edit the .bashrc file and remove all data. re-run $ conda init bash

[bash](https://docs.iac.gatech.edu/attachments/62)

<div id="bkmrk--2"><div><div class="aui-page-panel"><div class="view"><div class="wiki-content group" id="bkmrk--3"></div><div class="pageSection group">  
</div></div></div></div></div>
