import pyarrow.parquet as pq
import pandas as pd
import os, re, sys
import numpy as np
import dask.dataframe as dd
import fastparquet
import csv

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

def get_all_training_files_from(directory):
  files = []
  for filename in os.listdir(directory):
      filepath = os.path.join(directory, filename)
      if os.path.isfile(filepath):
        if "train" in filepath and "parquet.gzip" in filepath:
          files.append(fastparquet.ParquetFile(filepath))
      elif os.path.isdir(filepath):
          files.extend(get_all_training_files_from(filepath))
  return files

def preprocess_data():

  parquet_files = get_all_training_files_from(path_to_dataset_catalog)
  print(parquet_files)

  chunk_size = 18000
  outcome_csv_index = 0

  all_files = 0
  all_files_with_bugs = 0
  all_files_without_bugs = 0
  all_rejected_files = 0

  for parquet_file in parquet_files:

    for group in parquet_file.iter_row_groups():

      list_df = [group[i:i+chunk_size] for i in range(0, len(group), chunk_size)]
      print(len(list_df))

      for chunk_df in list_df:

        chunk_files = 0
        files_with_bugs = 0
        files_without_bugs = 0
        rejected_files = 0

        preprocessed_df_list = []

        for idx, row in chunk_df.iterrows():

          all_files += 1
          chunk_files += 1

          if idx == 0:
            continue

          try:
            SRC = row.content.decode('UTF-8')
          except:
            all_rejected_files += 1
            rejected_files += 1
            continue

          path = row.filepath
          line = row.lines

          if not np.size(line):
            bug = False
            all_files_without_bugs += 1
            files_without_bugs += 1
          else:
            bug = True
            all_files_with_bugs += 1
            files_with_bugs += 1

          data = {"File": path, "Bug": bug, "SRC": SRC}

          filename = data['File']

          if '.py' not in filename:
            all_rejected_files += 1
            rejected_files += 1
            continue

          code = data['SRC']
          label = data['Bug']

          code_df = create_code_df(code, filename)
          code_df['file-label'] = [label]*len(code_df)
          code_df['line-label'] = [False]*len(code_df)

          if len(code_df) > 0:
              preprocessed_df_list.append(code_df)

        all_df = pd.concat(preprocessed_df_list)
        all_df.to_csv(f"{path_to_outcome_catalog}result_{outcome_csv_index}.csv", index=False)

        print(f"Pliki dla chunk {outcome_csv_index}: {chunk_files}")
        print(f"Pliki z błędami: {files_with_bugs}")
        print(f"Pliki bez błędów: {files_without_bugs}")
        print(f"Odrzucone pliki: {rejected_files}")

        chunk_files = 0
        files_with_bugs = 0
        files_without_bugs = 0
        rejected_files = 0

        outcome_csv_index += 1
        preprocessed_df_list = []
        del(chunk_df)

      del(list_df)
      del(group)

  print(f"Wszystkie pliki: {all_files}")
  print(f"Wszystkie pliki z błędami: {all_files_with_bugs}")
  print(f"Wszystkie pliki bez błędów: {all_files_without_bugs}")
  print(f"Wszystkie odrzucone pliki: {all_rejected_files}")

preprocess_data()
print("DONE")
