import pandas as pd
import os, re
import numpy as np

path_to_data_root_dir = '/home/kuba/Desktop/ProjektBadawczoRozwojowy/'
path_to_save_dir = "/home/kuba/Desktop/ProjektBadawczoRozwojowy/"

char_to_remove = ['+','-','*','/','=','++','--','\\','<str>','<char>','|','&','!']

def is_comment_line(code_line, comments_list):
    '''
        input
            code_line (string): source code in a line
            comments_list (list): a list that contains every comments
        output
            boolean value
    '''

    code_line = code_line.strip()

    if len(code_line) == 0:
        return False
    elif code_line.startswith('//'):
        return True
    elif code_line.startswith('#'):
        return True
    elif code_line.startswith('"""'):
        return True
    elif code_line in comments_list:
        return True
    
    return False

def is_empty_line(code_line):
    '''
        input
            code_line (string)
        output
            boolean value
    '''

    if len(code_line.strip()) == 0:
        return True

    return False

def preprocess_code_line(code_line):
    '''
        input
            code_line (string)
    '''

    code_line = re.sub("\'\'", "\'", code_line)
    code_line = re.sub("\".*?\"", "<str>", code_line)
    code_line = re.sub("\'.*?\'", "<char>", code_line)
    code_line = re.sub('\b\d+\b','',code_line)
    code_line = re.sub("\\[.*?\\]", '', code_line)
    code_line = re.sub("[\\.|,|:|;|{|}|(|)]", ' ', code_line)

    for char in char_to_remove:
        code_line = code_line.replace(char,' ')

    code_line = code_line.strip()

    return code_line

def create_code_df(code_str, filename):
    '''
        input
            code_str (string): a source code
            filename (string): a file name of source code

        output
            code_df (DataFrame): a dataframe of source code that contains the following columns
            - code_line (str): source code in a line
            - line_number (str): line number of source code line
            - is_comment (bool): boolean which indicates if a line is comment
            - is_blank_line(bool): boolean which indicates if a line is blank
    '''

    df = pd.DataFrame()

    code_lines = code_str.splitlines()
    
    preprocess_code_lines = []
    is_comments = []
    is_blank_line = []


    comments = re.findall(r'("""[\s\S]*?""")|\'\'\'[\s\S]*?\'\'\'',code_str,re.DOTALL)
    comments_str = '\n'.join(comments)
    comments_list = comments_str.split('\n')
    
    for index, comment in enumerate(comments_list):
        comments_list[index] = comment.lstrip()

    for l in code_lines:
        l = l.strip()
        is_comment = is_comment_line(l,comments_list)
        is_comments.append(is_comment)
        # preprocess code here then check empty line...

        if not is_comment:
            l = preprocess_code_line(l)
            
        is_blank_line.append(is_empty_line(l))
        preprocess_code_lines.append(l)

    if 'test' in filename:
        is_test = True
    else:
        is_test = False

    df['filename'] = [filename]*len(code_lines)
    df['is_test_file'] = [is_test]*len(code_lines)
    df['code_line'] = preprocess_code_lines
    df['line_number'] = np.arange(1,len(code_lines)+1)
    df['is_comment'] = is_comments
    df['is_blank'] = is_blank_line

    return df

def preprocess_data():
    
    file_level_data = pd.read_csv(path_to_data_root_dir + 'test.csv', encoding='latin')
    file_level_data = file_level_data.fillna('')

    preprocessed_df_list = []

    for idx, row in file_level_data.iterrows():

        filename = row['File']

        if '.py' not in filename:
            continue

        code = row['SRC']
        label = row['Bug']

        code_df = create_code_df(code, filename)
        code_df['file-label'] = [False]*len(code_df)
        code_df['line-label'] = [False]*len(code_df)
                
        if len(code_df) > 0:
            preprocessed_df_list.append(code_df)

        all_df = pd.concat(preprocessed_df_list)
        all_df.to_csv(path_to_save_dir + "result.csv",index=False)

        
preprocess_data()
print("DONE")

