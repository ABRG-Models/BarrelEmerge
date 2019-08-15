a = csvread ('data.csv');

fnum = 1;
for doms=unique(a(:,1))'
    figure(fnum);
    clf;
    scatter(a(:,2),a(:,3),"filled")
    hold on;
    b = a(a(:,1)==doms, :);
    for idx=1:length(b(:,1))
        if (b(idx,4)==0) || (b(idx,5)==0)
            plot ( [b(idx,2)], [b(idx,3)], 'color',[b(idx,1),doms./length(a(:,1)),1-b(idx,1)]);
        else
            plot ( [b(idx,2),b(idx,4)], [b(idx,3),b(idx,5)], 'color',[b(idx,1),doms./length(a(:,1)),1-b(idx,1)]);
        end
    end
    fnum = fnum + 1;
end