# This Matlab script can be used to calculate the frequency
axis = 0:100:2850000;
freq = 2850000/(47*57+30);
axis_sec = axis*freq;
axis_time = datestr(axis_sec,'HH:MM:SS');
sec = seconds(axis_sec);
sec.Format = 'hh:mm:ss.SSS';
disp(sec)