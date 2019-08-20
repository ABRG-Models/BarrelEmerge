load '../logs/25N2M_withcomp_realmap/c_14000.h5'
load '../logs/25N2M_withcomp_realmap/positions.h5'
load '../logs/25N2M_withcomp_realmap/dv_14000.h5'

a=[dv_id', dv_x', dv_y', dv_n_x', dv_n_y'];

fnum = 1;
doms = 0.28
w = 1100;
h = 900;
for doms=unique(a(:,1))'

    h_f = figure(fnum); clf;
    h_f_pos = get(h_f, 'Position');
    set(h_f, 'Position', [h_f_pos(1:2), w, h]);
    hold on;

    % Could plot ALL vertices:
    scatter(a(:,2), a(:,3), 30, 'g', 'filled', 'marker','h')

    % Plot lines.
    b = a(abs(a(:,1)-doms)<0.01, :);
    for idx=1:length(b(:,1))
        if (b(idx,4)==0) || (b(idx,5)==0)
            plot ( [b(idx,2)], [b(idx,3)], 'color', 'r', 'markersize', 30);
        else
            plot ( [b(idx,2),b(idx,4)], [b(idx,3),b(idx,5)], 'color',  'r', 'linewidth', 3);
            plot ( [b(idx,2),b(idx,4)], [b(idx,3),b(idx,5)], '.', 'color', 'r', 'markersize', 30);
        end
    end
    title (['ID: ' num2str(b(1,1)) ]);

    % Plot all the background stuff:
    scatter (x, y, 24, dr, 'filled', 'marker', 'o');

    set (gca, 'Color', 'k')

    fnum = fnum + 1;

end
