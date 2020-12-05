path = '/Users/deveshkumar/Desktop/sem5/CroppedYale/YaleB0';
input_img = im2double(imread('/Users/deveshkumar/Desktop/sem5/image_processing/ajit/assing4/CroppedYale/yaleB28/yaleB28_P00A+010E+00.pgm'));

D = strcat(path,int2str(1));
S = dir(fullfile(D,'*.pgm')); 
im4 = imread(strcat(S(1).folder,'/',S(1).name));
figure(1),imshow(input_img);
title('Input Image');
total_img = 39;
training = 40 ;
perimage = 64;
X = zeros(192*168,38*40); %size of one image
path = '/Users/deveshkumar/Desktop/sem5/CroppedYale/YaleB0';

k = [2,10,20,50,75,100,125,150,175];

for  i = 1:9
    D = strcat(path,int2str(i));
    S = dir(fullfile(D,'*.pgm')); 
        for j = 1:training
        img = im2double(imread(strcat(S(i).folder,'/',S(j).name)));
        img =img(:);
       % mean_img = sum(img);
        %minus( img ,sum);
%        img - mean(img);

        X(:,(i-1)*40 + j) = img;
        end
    
end

path = '/Users/deveshkumar/Desktop/sem5/CroppedYale/YaleB';


for  i = 10:39
    if i ~= 14 %14th element not present
    D = strcat(path,int2str(i));
    S = dir(fullfile(D,'*.pgm')); 
        for j = 1:training
        img = im2double(imread(strcat(S(i).folder,'/',S(j).name)));
        img =img(:);
        X(:,(i-1)*40 + j) = img;
        end
    end
end

%X = X(:, 2:end);
%Average = mean(X, 2);

%X = X-Average;
%L =transpose(X)*X;

[vector,values,none] = svd(X, 'econ');  %eigs(L,kmax);%gives k largest eigen vector
image = input_img(:);


[~, permutation] = sort(diag(values), 'descend');
%S = S(permutation, permutation);
vector = vector(:, permutation);

n = sum(vector.^2,1);
vector = bsxfun(@rdivide, vector, n);

vector = vector(:,1:k(8));

alpha=transpose(vector)*image; 
new = vector*alpha;
new = reshape(new,192,168);


figure(2),imshow(new);


%vector = X*vector;


%alpha=transpose(vector)*image;
%new = vector * alpha;
%new = reshape(new,192,168);
%new1 =new*256/max((max(new))); 
%new1= uint8(new1);

