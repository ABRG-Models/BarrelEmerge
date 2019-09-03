function add_cross (cx, cy)

    hold on;
    dx = 0.05;
    plot ([cx-dx, cx+dx], [cy, cy], 'r');
    plot ([cx, cx], [cy-dx, cy+dx], 'r');

end