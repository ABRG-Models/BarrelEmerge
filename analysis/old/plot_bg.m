load '../logs/25N2M_withcomp_realmap/c_12000.h5'
load '../logs/25N2M_withcomp_realmap/positions.h5'

fnum = 1;
w = 1100;
h = 900;

h_f = figure(fnum); clf;
h_f_pos = get(h_f, 'Position');
set(h_f, 'Position', [h_f_pos(1:2), w, h]);
hold on;

% Plot all the background stuff:
scatter (x, y, 24, dr, 'filled', 'marker', 'o');
set (gca, 'Color', 'k')
