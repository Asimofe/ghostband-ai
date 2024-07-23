import pickle

def read_pickle_file(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        print(data)

read_pickle_file('infer_test.bin')

