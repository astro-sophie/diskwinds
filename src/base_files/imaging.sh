python3 master.py
python3 problem_setup.py
radmc3d mctherm setthreads 4
radmc3d image lambda 1301.3 incl 85 phi 0 zoomau -400 400 -400 400 npixx 60 npixy 60
python3 generateimage.py
