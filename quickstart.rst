Quickstart
==========

::

  $ export LC_ALL=C 
  $ iostat -c -d -x -t -m /dev/sda 1 100 > iostat.out
  $ dd if=/dev/zero of=/tmp/bla.dd bs=1024 count=$(python -c 'print 2**20') > iostat.out
  $ ./iostat_plotter_v3.py iostat.out


.. important:: 

  localisation settings must be set to 'C' or 'en_US.UTF-8' before recording
  data with `iostat`. otherwise `iostat_plotter` fails on parsing the data.
  check your current setting via `locale` and change it via `export LC_ALL=C`
  if needed so. 


more examples
-------------

recording 60 samples at an interval of 60s (== 1h data) for all devices abailable::

    $ iostat -c -d -x -t -m 60 60 | tee iostats_zaphod_all.60s.60.out

    # plot it
    # (option -c stands for "combined" and plots all devices into one plot)

    $ ./iostat_plotter_v3.py [-c] iostats_zaphod_all.60s.60.out


