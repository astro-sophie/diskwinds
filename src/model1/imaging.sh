python3 master.py
python3 problem_setup.py
radmc3d mctherm setthreads 4
radmc3d image lambda 4.6947 incl 85 phi 0 zoomau -220 220 14 238 npix 40
python3 generateimage.py
