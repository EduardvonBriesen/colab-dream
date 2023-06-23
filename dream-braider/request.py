import helper.settings_parser as Parser

def video_request(prompt, pwd='', settings=None):
    if pwd != '':
        print('pwd: ', pwd)
        string_array = Parser.load_file_to_array(path=pwd + '/struct/video.json')
    else: string_array = Parser.load_file_to_array(path='struct/video.json')   

    # add style specifying keywords
    prompt = Parser.modify_prompt_randomly(input=prompt)

    # get last image of previous prompt
    # TODO integrate settings from config file
    if settings is not None:
        first_run, init_image = Parser.get_init_image(folder=settings['APP']['path_dreams'])
    else: first_run, init_image = Parser.get_init_image(folder="/home/ubuntu/stable-diffusion-webui/outputs/img2img-images/dream")

    # 2D or 3D
    string_array[7] = '"3D",'

    # images per prompt
    string_array[8] = '170,'

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

    # cadence: 2 - 4
    string_array[53] = '4,'

    string_array[73] = '"{' + r"\"0\": \"" + f'{prompt}' + r'\"' + '}",'

    # steps
    string_array[85] = '20,'

    # output folder
    string_array[93] = '"dream",'

    # use init image: true or false
    # first run does not have an init image
    if first_run: string_array[97] = 'false,'
    else: string_array[97] = 'true,'

    # init image strength
    # TODO check if other values are more suitable
    string_array[100] = '0.6,'

    # init image file
    if first_run: string_array[101] = '"",'
    else: string_array[101] = f'"{init_image}",'

    # skip video stiching: true or false
    string_array[114] = 'true,'

    # FPS
    string_array[115] = '8,'

    request_string = "\n".join(string_array)

    with open(pwd + '/struct/request.json', 'w') as file:
        file.write(request_string)
