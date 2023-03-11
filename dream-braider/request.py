import helper.settings_parser as Parser

def video_request(prompt):
    string_array = Parser.load_file_to_array(path='struct/video.json')

    string_array[73] = '"{' + r"\"0\": \"" + f'{prompt}' + r'\"' + '}",'

    request_string = "\n".join(string_array)

    with open('struct/request.json', 'w') as file:
        file.write(request_string)

    # return request_string

# output = video_request('House on the street')
# print(output)