python3 master.py
python3 problem_setup.py
radmc3d mctherm setthreads 4
radmc3d image lambda 4.69125225 incl 85 phi 0 zoomau -210 210 14 252 npixx 30 npixy 17
python3 generateimage.py
