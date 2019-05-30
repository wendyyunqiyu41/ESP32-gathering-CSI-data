%% Load Training Data
load ActivityTrainAveCSI

% plot training data
X=XTrain{1};
classes=categories(YTrain{1});
figure
for i=1:numel(classes)
    label=classes(i);
    idx=find(YTrain{1}==label);
    hold on
    scatter(idx,X(idx))
end
hold off

xlabel("Time Step")
ylabel("CSI Magnitude")
title("Training Sequence 1")
legend(classes,'Location','northwest')

X=XTrain{2};
classes=categories(YTrain{2});
figure
for i=1:numel(classes)
    label=classes(i);
    idx=find(YTrain{2}==label);
    hold on
    scatter(idx,X(idx))
end
hold off

xlabel("Time Step")
ylabel("CSI Magnitude")
title("Training Sequence 2")
legend(classes,'Location','northwest')

X=XTrain{3};
classes=categories(YTrain{3});
figure
for i=1:numel(classes)
    label=classes(i);
    idx=find(YTrain{3}==label);
    hold on
    scatter(idx,X(idx))
end
hold off

xlabel("Time Step")
ylabel("CSI Magnitude")
title("Training Sequence 3")
legend(classes,'Location','northwest')


%% Define LSTM Network Atchitecture
featureDimension=1; % sequence of size 1 (feature dimension)
numHiddenUnits=100; % LSTM layer with 100 hidden units
numClasses=2; % 2 classes which are active and inactive

layers=[ ...
    sequenceInputLayer(featureDimension)
    lstmLayer(numHiddenUnits,'OutputMode','sequence')
    fullyConnectedLayer(numClasses)
    softmaxLayer
    classificationLayer];

options=trainingOptions('adam', ...
    'GradientThreshold',1, ...
    'InitialLearnRate',0.01, ...
    'LearnRateSchedule','piecewise', ...
    'LearnRateDropPeriod',20, ...
    'MaxEpochs',100, ...
    'MiniBatchSize',15, ...
    'Verbose',0, ...
    'Plots','training-progress'); % drop learn rate by 0.1 after 20 epochs

net=trainNetwork(XTrain,YTrain,layers,options);

%% Test LSTM Network

% plot test data
figure
plot(XTest')
xlabel("Time Step")
ylabel("CSI Magnitude")
legend("Feature"+(1:featureDimension))
title("Test Data")

YPred=classify(net,XTest); % classify test data
acc=sum(YPred==YTest)./numel(YTest); % accuracy

figure
plot(YPred,'.-')
hold on
plot(YTest)
hold off

xlabel("Time Step")
ylabel("Activity")
title("Predicted Activities")
legend(["Predicted" "Test Data"])


