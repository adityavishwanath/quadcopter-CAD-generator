function [arr] = AeroHacks
v = 10;
xi = 0;
thresh = 15;
deltat = 0.5;
num = csvread('data.csv');
num = num(num<=thresh);
[N,~] = size(num);
N = floor(N/4);
time = N.*deltat;
s = v.*time; %side length
deltas = s/N; %calculating inteval size for coordinates
i = 0;
X1a = [];
while i<=N
    X1a = [X1a xi];
    xi = xi + deltas;
    i = i + 1;
end
N1 = length(X1a);
Y1 = zeros(1,N1);
Y2 = Y1 + s;
Z1a = zeros(1,N1);
X1b = zeros(1,N1) + s;
Z1b = -1.*X1a;
Z1b(1) = 0;
X1c = X1a;
Z1c = -1.*(zeros(1,N1) + s);
X1d = zeros(1,N1);
Z1d = -1.*X1a;
Z1d(1) = 0;

arr = [X1a' Y1' Z1a'; X1b' Y1' Z1b'; X1c' Y1' Z1c'; X1d' Y1' Z1d'];
arr = [arr; X1a' Y2' Z1a'; X1b' Y2' Z1b'; X1c' Y2' Z1c'; X1d' Y2' Z1d'];
%xlswrite('Corrected_Data.csv',arr);

fileID = fopen('data.txt','w');

for i = 1:4*N1
    fprintf(fileID,'%2.2f %2.2f %2.2f\n', arr(i,1), arr(i,2), arr(i,3));
end

fclose(fileID);
end