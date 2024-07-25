python3 master.py
python3 problem_setup.py
radmc3d mctherm setthreads 4
radmc3d image lambda 4.6947 incl 85 phi 0 zoomau -280 280 0 280 npixx 80 npixy 40
python3 generateimage.py
