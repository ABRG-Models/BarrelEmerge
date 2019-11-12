% Compare the "cubed competition" with "cubed via logistic" competition.
l = 3
m = 0.3

Eps = 5000;
Eps_p = 200;

x=[0:0.01:50];
y = power(x,3);

figure (1);
hold off;
fy = Eps .* 2.* (-0.5 + 1./(1 + exp(-m.*y)));
plot (x,fy);
hold on;
% Compare with just the raw geometric fn:
plot (x, Eps_p.*y);

lg = legend(['power logistic: ' num2str(2.*Eps) '/(1+e^{-' num2str(m) 'a^' num2str(l) '})'], ...
['power only (' num2str(Eps_p) 'a^' num2str(l) ')'], 'location', 'southeast')


xlim([0,5]);
ylim([0,Eps]);
xlabel('a')
ylabel('f(a)')

tstr = ['l = ' num2str(l) ', m = ' num2str(m)]
title(tstr)
