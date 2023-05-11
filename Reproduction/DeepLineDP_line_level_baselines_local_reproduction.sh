#! /usr/bin/bash

echo "Downloading dataset"
cd ./DeepLineDP/
mkdir ./datasets/original/
cd ./datasets/original/
git clone https://github.com/awsm-research/line-level-defect-prediction.git
cp -r ./line-level-defect-prediction/Dataset/File-level/ ./
cp -r ./line-level-defect-prediction/Dataset/Line-level/ ./

echo "Setting conda envirnment"
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
chmod +x Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
bash ./Miniconda3-py39_23.1.0-1-Linux-x86_64.sh -b -f -p /usr/local
cd ../../
conda env create -f requirements.yml
USER=$(whoami)
source /home/$USER/miniconda3/bin/activate DeepLineDP_env

echo "Preprocessing dataset"
cd ../../
python export_data_for_line_level_baseline.py

cd ./script/line-level-baseline/

echo "Generating predictions for N-gram lile-level baseline..." 
cd ./ngram/
javac n_gram.java
java n_gram
cp -r ./n_gram_result/ ../../../output/

echo "Generating predictions fot ErrorProne line-level baseline..."
cd ../ErrorProne/
jupyter run run_ErrorProne.ipynb
cp -r ./ErrorProne_result/ ../../../output/
