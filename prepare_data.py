import os
import json


def get_file_list(data_dir):
    # get all the folder names in the dataset directory
    target_values = os.listdir(data_dir)
    # ignore the .DS_Store file
    target_values = [f for f in target_values if f != '.DS_Store']
    target_values.sort()
    return target_values


def format_data(data_path, is_lyrics):
    # create content from each files
    data = {}
    content = {}
    target_json = {}
    target_value_json = {}
    file_name = {}
    i = 0
    for idx, target in enumerate(target_values):
        for file in os.listdir(data_path + target):
            with open(data_path + target + '/' + file, 'r', encoding='utf-8', errors='ignore') as f:
                content[str(i)] = f.read()
                target_json[str(i)] = str(idx)
                target_value_json[str(i)] = target
                if is_lyrics:
                    file_name[str(i)] = file.split('.txt')[0]
                i+=1
    data['content'] = content
    data['target'] = target_json
    data['target_value'] = target_value_json
    if is_lyrics:
        data['file_name'] = file_name
    return data


if __name__ == '__main__':
    data_dir = ['data/20news-18828/', 'data/lyrics/']
    file_name_json = ['data/dataset.json', 'data/lyrics.json']
    dataset = ['newsgroup', 'lyrics']
    for idx, data in enumerate(data_dir):
        print(f'***** Preparing {dataset[idx]} dataset *****')
        is_lyrics = 'lyrics' in data_dir[idx]
        target_values = get_file_list(data)
        # get the total count of the files present from each directory
        total_count = 0
        for target in target_values:
            total_count += len(os.listdir(data + target))
        print(f'Total number of files: {total_count}')
        formatted_data = format_data(data_path=data, is_lyrics=is_lyrics)
        # save the data to a json file
        with open(file_name_json[idx], 'w') as f:
            json.dump(formatted_data, f)

    print('***** Data preparation completed *****')
