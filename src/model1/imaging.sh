python3 master.py
python3 problem_setup.py
radmc3d mctherm setthreads 12
radmc3d image lambda 4.6947 incl 85 phi 0 zoomau -210 210 14 252 npixx 60 npixy 34
python3 generateimage.py
