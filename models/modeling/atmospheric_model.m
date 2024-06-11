clc; clear; close all

dirpath = "data/atmospheric";
files = dir(dirpath + "/*.csv");
legend = {};
legend_ctr = 1;


figure
hold on

for i=1:length(files)
    filename = files(i).name;
    filepath = fullfile(dirpath, filename);
    data = readtable(filepath);

    split_filename = split(filename, "_");
    altitude = split_filename(2);

    % building model
    n = 2;      % order
    p = polyfit(data.x, data.y, n);

    % evaluating model
    x = -20:1:100;
    y = polyval(p, x);

    scatter(data.x, data.y)
    plot(x, y)

    legend{legend_ctr} = altitude + " ft";
    legend_ctr = legend_ctr + 1;

    disp(altitude)
    p
end

xlim([-20, 100])
ylim([0, 28])