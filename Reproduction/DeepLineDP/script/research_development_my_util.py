import re
import torch
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd

max_seq_len = 50

all_train_releases = {'dataset_RQ1': 'dataset_RQ1_train', 
                      'dataset_RQ2': 'dataset_RQ2_train', 
                      'dataset_RQ3': 'dataset_RQ3_train', 
                      'dataset_RQ4': 'dataset_RQ4_train', 
                      'dataset_RQ5': 'dataset_RQ5_train'}

all_eval_releases = {'dataset_RQ1': ['dataset_RQ1_eval_1', 'dataset_RQ1_eval_2'], 
                     'dataset_RQ2': ['dataset_RQ2_eval_1', 'dataset_RQ2_eval_2'], 
                     'dataset_RQ3': ['dataset_RQ3_eval_1', 'dataset_RQ3_eval_2'], 
                     'dataset_RQ4': ['dataset_RQ4_eval_1', 'dataset_RQ4_eval_2'], 
                     'dataset_RQ5': ['dataset_RQ5_eval_1', 'dataset_RQ5_eval_2']}

all_releases = {'dataset_RQ1': ['dataset_RQ1_train', 'dataset_RQ1_eval_1', 'dataset_RQ1_eval_2'], 
                'dataset_RQ2': ['dataset_RQ2_train', 'dataset_RQ2_eval_1', 'dataset_RQ2_eval_2'], 
                'dataset_RQ3': ['dataset_RQ3_train', 'dataset_RQ3_eval_1', 'dataset_RQ3_eval_2'], 
                'dataset_RQ4': ['dataset_RQ4_train', 'dataset_RQ4_eval_1', 'dataset_RQ4_eval_2'], 
                'dataset_RQ5': ['dataset_RQ5_train', 'dataset_RQ5_eval_1', 'dataset_RQ5_eval_2']}

all_projs = list(all_train_releases.keys())

file_lvl_gt = '../datasets/preprocessed_data/'

word2vec_dir = '../output/Word2Vec_model/' 

def get_df(rel, is_baseline=False):

    if is_baseline:
        df = pd.read_csv('../'+file_lvl_gt+rel+".csv")

    else:
        df = pd.read_csv(file_lvl_gt+rel+".csv")

    df = df.fillna('')

    df = df[df['is_blank']==False]
    df = df[df['is_test_file']==False]

    return df

def prepare_code2d(code_list, to_lowercase = False):
    '''
        input
            code_list (list): list that contains code each line (in str format)
        output
            code2d (nested list): a list that contains list of tokens with padding by '<pad>'
    '''
    code2d = []

    for c in code_list:
        c = re.sub('\\s+',' ',c)

        if to_lowercase:
            c = c.lower()

        token_list = c.strip().split()
        total_tokens = len(token_list)
        
        token_list = token_list[:max_seq_len]

        if total_tokens < max_seq_len:
            token_list = token_list + ['<pad>']*(max_seq_len-total_tokens)

        code2d.append(token_list)

    return code2d
    
def get_code3d_and_label(df, to_lowercase = False):
    '''
        input
            df (DataFrame): a dataframe from get_df()
        output
            code3d (nested list): a list of code2d from prepare_code2d()
            all_file_label (list): a list of file-level label
    '''

    code3d = []
    all_file_label = []

    for filename, group_df in df.groupby('filename'):

        file_label = bool(group_df['file-label'].unique())

        code = list(group_df['code_line'])

        code2d = prepare_code2d(code, to_lowercase)
        code3d.append(code2d)

        all_file_label.append(file_label)

    return code3d, all_file_label

def get_w2v_path():

    return word2vec_dir

def get_w2v_weight_for_deep_learning_models(word2vec_model, embed_dim):
    word2vec_weights = torch.FloatTensor(word2vec_model.wv.syn0).cuda()
    
    # add zero vector for unknown tokens
    word2vec_weights = torch.cat((word2vec_weights, torch.zeros(1,embed_dim).cuda()))

    return word2vec_weights

def pad_code(code_list_3d,max_sent_len,limit_sent_len=True, mode='train'):
    paded = []
    
    for file in code_list_3d:
        sent_list = []
        for line in file:
            new_line = line
            if len(line) > max_seq_len:
                new_line = line[:max_seq_len]
            sent_list.append(new_line)
            
        
        if mode == 'train':
            if max_sent_len-len(file) > 0:
                for i in range(0,max_sent_len-len(file)):
                    sent_list.append([0]*max_seq_len)

        if limit_sent_len:    
            paded.append(sent_list[:max_sent_len])
        else:
            paded.append(sent_list)
        
    return paded

def get_dataloader(code_vec, label_list,batch_size, max_sent_len):
    y_tensor =  torch.cuda.FloatTensor([label for label in label_list])
    code_vec_pad = pad_code(code_vec,max_sent_len)
    tensor_dataset = TensorDataset(torch.tensor(code_vec_pad), y_tensor)

    dl = DataLoader(tensor_dataset,shuffle=True,batch_size=batch_size,drop_last=True)
    
    return dl

def get_x_vec(code_3d, word2vec):
    x_vec = [[[word2vec.wv.vocab[token].index if token in word2vec.wv.vocab else len(word2vec.wv.vocab) for token in text]
         for text in texts] for texts in code_3d]
    
    return x_vec