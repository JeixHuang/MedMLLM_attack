def log_to_file(file_path, data):
    with open(file_path, 'a') as file:
        file.write(data + '\n')
