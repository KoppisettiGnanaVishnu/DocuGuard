def load_document(file_path):

    with open(file_path, "r") as file:

        text = file.read()

    return text