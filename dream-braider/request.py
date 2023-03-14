import helper.settings_parser as Parser

def video_request(prompt, pwd=''):
    if pwd != '':
        print('pwd: ', pwd)
        string_array = Parser.load_file_to_array(path=pwd + '/struct/video.json')
    else: string_array = Parser.load_file_to_array(path='struct/video.json')    

    string_array[73] = '"{' + r"\"0\": \"" + f'{prompt}' + r'\"' + '}",'

    request_string = "\n".join(string_array)

    with open(pwd + '/struct/request.json', 'w') as file:
        file.write(request_string)
