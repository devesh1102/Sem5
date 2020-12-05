
k = 20;
total_img = 32;
training = 6 ;
perimage = 10;
X = zeros(112*92,32*6); %size of one image

path = '/Users/deveshkumar/Desktop/sem5/image_processing/ajit/assing4/q1/att_faces/s';
for  i = 1:total_img
    for j = 1:training
        img = im2double(imread(strcat(path,int2str(i),'/',int2str(j),'.pgm')));
        img =img(:);
       % mean_img = sum(img);
        %minus( img ,sum);
        img - mean(img);

        X(:,(i-1)*6 + j) = img;
     end
end
L =transpose(X)*X;
[vector,values] = eigs(L,k);%gives k largest eigen vector
V = X*vector;
V= normalize(V);
alpha = transpose(V) * X;

% test:
j =j+1;
wrong = 0;
for  i = 1:total_img
    for j = j:perimage
        img = im2double(imread(strcat(path,int2str(i),'/',int2str(j),'.pgm')));
        img =img(:);
       % mean_img = sum(img);
        %minus( img ,sum);
        img - mean(img);
        alpha_img = transpose(V)*img;
        error = alpha - alpha_img;
        error1 = error.^2;
        error2 = (sum(error1, 1)).^(0.5);
        [value, index] = min ( error2);
        output = floor((index-1)/6) + 1;
        if output ~= i 
            wrong = wrong + 1;
        end
    end
end




