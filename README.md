On Improving Line-Level Defect Prediction: An Evaluation and Enhancement of the DeepLineDP Model Using the Defectors Dataset
============================================================================================================================

Authors 
-------

Patrycja Kałużna (252864)

Jakub Walaszek (252897)

Reasons
-------

The topic was chosen because of:
- availability of source code of models which gives a possibility to reproduce and develop research,
- availability of datasets on which models were trained which also gives a possibility to reproduce research,
- availability of scripts and an instruction of how to use these scripts to reproduce research. 

Articles 
--------

DeepLineDP model: https://ieeexplore.ieee.org/document/9689967

Defectors dataset: https://arxiv.org/abs/2303.04738

DeepLineDP model's GitHub
-------------------------

https://github.com/awsm-research/DeepLineDP

Defectors dataset's source
--------------------------

https://zenodo.org/record/7708984


Trello
------

https://trello.com/b/tYlTMYCg/main

Overleaf
--------

https://www.overleaf.com/project/6401cc2de33881644150cd5f

Google Colaboratory
-------------------

For generating research reproduction's results:

https://colab.research.google.com/drive/139uWve5H07uM0SIKZSuevsi-dEjWeK9P?usp=sharing

For generating figures representing research questions' answers:

https://colab.research.google.com/drive/1rglM2qt-w5JA-PXk2WnGHK_eAml3Wqae?usp=sharing

Leadership's schedule
---------------------
https://politechnikawroclawska-my.sharepoint.com/:x:/g/personal/252864_student_pwr_edu_pl/EZkkBqJQHCROlh3e_fCDmbABqrCMpqgz_4aZvHR55gZ14A?e=RNPHLI

Research reproduction steps
---------------------------
1. Click on link to Google Colaboratory environment which contains Jupyter Notebook that allows of downloading required files, configuring required environment and reproducing research for DeepLineDP model and file-level baselines.
   
    https://colab.research.google.com/drive/139uWve5H07uM0SIKZSuevsi-dEjWeK9P?usp=sharing

2. Click on consecutive field's arrow signs to download required files, configure required environments and reproduce research.

**Note:** Google Colaboratory environment session can last up to 12 hours but can end before this time unexpectedly. It is important to remember to save results outside of this environment from time to time. At the end of the Jupyter Notebook there are 2 fields which alows of exporting and importing all data that is in the environment to and from Google Drive.

3. To reproduce research for line-level baselines on Windows machine:
    1. Install Java and Python if they are not installed,
    2. Run `DeepLineDP_line_level_baselines_local_reproduction.bat` script from `M8/Reproduction` folder.

Research reproduction's results can be found in `M8/Reproduction/DeepLineDP/output` directory:
- `/content/M8/Reproduction/DeepLineDP/output/model/DeepLineDP/<PROJECT_NAME>` - contains trained models for \<PROJECT_NAME\> project,
- `/content/M8/Reproduction/DeepLineDP/output/loss/DeepLineDP/<PROJECT_NAME>-loss_record.csv` - contains training and validations loss for \<PROJECT_NAME\> project,
- `/content/M8/Reproduction/DeepLineDP/output/prediction/DeepLineDP/within-release` - contains projects releases' within-release predictions,
- `/content/M8/Reproduction/DeepLineDP/output/prediction/DeepLineDP/cross-project/<PROJECT_NAME>` - contains \<PROJECT_NAME\> project's cross-projects predictions, 
- `/content/M8/Reproduction/DeepLineDP/output/model/<FILE-LEVEL_BASELINE_NAME>/<PROJECT_NAME>` - contains trained models for \<FILE-LEVEL_BASELINE_NAME\> file-level baseline and \<PROJECT_NAME\> project,
- `/content/M8/Reproduction/DeepLineDP/output/loss/<FILE-LEVEL_BASELINE_NAME>/<PROJECT_NAME>-<FILE-LEVEL_BASELINE_NAME>-loss_record.csv` - contains training and validation loss for \<FILE-LEVEL_BASELINE_NAME\> file-level baseline and \<PROJECT_NAME\> project,
- `/content/M8/Reproduction/DeepLineDP/output/prediction/<FILE-LEVEL_BASELINE_NAME>` - contains predictions for \<FILE-LEVEL_BASELINE_NAME\> file-level baseline,
- `M8/Reproduction/DeepLineDP/output/n_gram_result` - contains results for N-gram line-level baseline,
- `M8/Reproduction/DeepLineDP/output/ErrorProne_result` - contains results for ErrorProne line-level baseline.

Where \<PROJECT_NAME\> can be one of following: activemq, camel, derby, groovy, hbase, hive, jruby, lucene, wicket and where \<FILE-LEVEL_BASELINE_NAME\> can be one of following: Bi-LSTM, CNN, DBN, BoW.

4. Click on link to Google Colaboratory environment with R runtime type which contains Jupter Notebook that allows of downloading research reproduction results, installing required R libraries and generating figures representing research questions' answers. 

    https://colab.research.google.com/drive/1rglM2qt-w5JA-PXk2WnGHK_eAml3Wqae?usp=sharing

5. Click on consecutive field's arrow signs to download research reproduction results, install required R libraries and generate figures.

Figures representing research question's answers can be found in `M8/Reproduction/DeepLineDP/output/figure` directory.

**Note**: This Google Colaboratory environment and Jupyter Notebook allows of generating figures representing research questions' answers for 2 of 4 research questions. It is because get_evaluation_result.R script provided by researchers has bugs and we have not been able to correct all of them yet.
