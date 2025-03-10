@echo off
call "F:\anaconda3\Scripts\activate.bat" base
echo Conda environment activated.
python --version
python "f:\BIT-srun-login-script\AutoLoad.py"