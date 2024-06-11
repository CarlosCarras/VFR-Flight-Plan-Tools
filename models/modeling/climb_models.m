clc; clear; close all

% filename = 'data/climb_fuel_gal.csv';
% filename = 'data/climb_time_min.csv';
filename = 'data/climb_distance_nm.csv';

data = readtable(filename);

n = 5;      % model order
p = polyfit(data.y, data.x, n)


%% Evaluating Model

x = 0:data.y(end)+1;
y = polyval(p, x);


%% Plotting

figure
hold on 

scatter(data.y, data.x)
plot(x, y)


