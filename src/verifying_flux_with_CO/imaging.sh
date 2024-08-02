python3 master.py
python3 problem_setup.py
radmc3d mctherm setthreads 4
radmc3d image lambda 1300.4036558 incl 0 phi 0 zoomau -600 600 -600 600
python3 generateimage.py
