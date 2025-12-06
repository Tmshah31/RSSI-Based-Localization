%data = readtable("ESP_Beacon_one_2025-11-20_09-13-42_dataset.csv");

% Extract columns
X = ESP_Beacon_three_2025_11_20_09_13_42_dataset.X;
Y = ESP_Beacon_three_2025_11_20_09_13_42_dataset.Y;
RSSI = ESP_Beacon_three_2025_11_20_09_13_42_dataset.RSSI_avg_;



% Create per-sample grid
[xq, yq] = meshgrid(min(X):1:max(X), min(Y):1:max(Y));

%Semi interpolation 
Zq = griddata(X, Y, RSSI, xq, yq, 'natural');


% Plot the heatmap
figure; hold on;
imagesc(unique(X), unique(Y), Zq);
set(gca,'YDir','normal');

%AP location
plot(0, 17, 'xm', 'MarkerSize', 20, 'LineWidth', 5);

colormap(jet);
colorbar;
xlabel("X");
ylabel("Y");
legend("AP Location", Location="northwest")
title("Heatmap AP 3 located (0,17)");

axis tight; 


