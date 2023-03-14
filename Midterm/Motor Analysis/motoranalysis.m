clc; clear; clf;
angle = importdata("MotorAt50.csv");

l = 50;
A = 0.0046;
B = 0.098;
func = @(t) l*A/B^2*(B/A*t - 1 + exp((-B/A)*t));

inc = 0.005;
t = 0:inc:(length(angle)-1)*inc;

AnAngle = func(t);

figure(1)

plot(t, angle, "DisplayName","Measured Motor Response")
hold on
plot(t, AnAngle, "DisplayName","Analytical Motor Response")
legend
title("Analytical and Measured Motor Response to 50 LVU Step:")
xlabel("angle (deg)")
ylabel("time (s)")
hold off
