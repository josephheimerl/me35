clear; clc; clf;
%THIS SCRIPT MUST BE RUN FROM THE SAME DIRECTORY AS mysecrets.py

%next few lines find broker IP from secrets file
temp = fileread("mysecrets.py");
temp = erase(temp, " ");
broker = extractBetween(temp,"Broker_IP='","'");

mqttClient = mqttclient("tcp://" + broker, ClientID="JosephLiveAnimation", ...
                        Timeout=10);

subscribe(mqttClient,"angles",Callback=@myCallback);

global gt1 gt2
gt1 = [];
gt2 = [];
elem = 1;

figure(1)
hold on
xlabel("x position")
ylabel("y position")
title("Current Leg Position")
xlim([-20,20])
ylim([-20,20])
path = animatedline;
head = scatter(nan,nan,20,'b');
upperArm = line([0,0],[0,-7],'Color','r','LineWidth',1);
foreArm = line([0,0],[-7,-20],'Color','b','LineWidth',1);

while true
    if length(gt1)+1 > elem
        updatePlot(path,head,upperArm,foreArm,gt1(elem),gt2(elem))
        elem = elem+1;
    end
    pause(0.05)
end


function myCallback(~,data)
    global gt1 gt2
    t1s = extractBetween(data,"(",",");
    t2s = extractBetween(data,",",")");
    t1 = str2double(t1s);
    t2 = str2double(t2s);
    gt1(end+1) = t1;
    gt2(end+1) = t2;

end

% assumes upper arm is 7 inches and forearm is 13 inches
function updatePlot(path,head,upperArm, foreArm,t1,t2)
    l1 = 7;
    l2 = 13;
    [x,y] = ang2pos(t1,t2,l1,l2);
    addpoints(path,x,y)
    set(head,'xdata',x,'ydata',y)
    xElbow = -1*l1*sin(t1*pi/180);
    yElbow = -1*l1*cos(t1*pi/180);
    set(upperArm,'XData',[0,xElbow],'YData',[0,yElbow]);
    set(foreArm,'XData',[xElbow,x],'YData',[yElbow,y])
    drawnow limitrate
end

% converts angles to the coordinate positions of the legs
function [x,y] = ang2pos(t1,t2,l1,l2)
    t1 = t1*pi/180;
    t2 = t2*pi/180;
    x = -l1*sin(t1)-l2*sin(t1+t2);
    y = -l1*cos(t1)-l2*cos(t1+t2);
end