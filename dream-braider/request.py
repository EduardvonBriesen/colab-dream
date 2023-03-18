import helper.settings_parser as Parser

def video_request(prompt, pwd=''):
    if pwd != '':
        print('pwd: ', pwd)
        string_array = Parser.load_file_to_array(path=pwd + '/struct/video.json')
    else: string_array = Parser.load_file_to_array(path='struct/video.json')   

    # add style specifying keywords
    prompt = Parser.modify_prompt_randomly(input=prompt)

    # 2D or 3D
    string_array[7] = '"3D",'

    # images per prompt
    string_array[8] = '20,'

    # tranZ
    string_array[14] = '"0: (3*(sin(3.141*t/50)**3)+.75)",'

    # rotX
    string_array[15] = '"0: (0.25*sin(2*3.141*t/250))",'

    # rotY
    string_array[16] = '"0: (0.25*sin(2*3.141*t/250))",'

    # rotZ
    string_array[17] = '"0: (0.5*sin(2*3.141*t/250))",'

    # strength
    string_array[24] = '"0: (-0.13*(cos(3.141*t/13)**100)+0.63)",'


    string_array[73] = '"{' + r"\"0\": \"" + f'{prompt}' + r'\"' + '}",'

    # steps
    string_array[85] = '20,'

    # output folder
    string_array[93] = '"dream",'

    # skip video stiching: true or false
    string_array[114] = 'true,'

    # FPS
    string_array[115] = '8,'

    request_string = "\n".join(string_array)

    with open(pwd + '/struct/request.json', 'w') as file:
        file.write(request_string)
