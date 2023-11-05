import helper.settings_parser as Parser

def video_request(prompt, pwd='', settings=None):
    if pwd != '':
        print('pwd: ', pwd)
        string_array = Parser.load_file_to_array(path=pwd + '/struct/request_warszawa.json')
    else: string_array = Parser.load_file_to_array(path='struct/request_warszawa.json')   

    # add style specifying keywords
    prompt = Parser.modify_prompt_randomly(input=prompt)
    prompt = "masterpiece, visually specific, high resolution, 4k, 8k, high res, clarity, well balanced contrast, strong contrast" + prompt

    # get last image of previous prompt
    # TODO integrate settings from config file
    if settings is not None:
        first_run, init_image = Parser.get_init_image(folder=settings['APP']['path_dreams'])
    else: first_run, init_image = Parser.get_init_image(folder="/workstation/stable-diffusion-webui/outputs/img2img-images/dream")

    # 2D or 3D
    string_array[36] = '"animation_mode": "2D",'

    # images per prompt
    string_array[37] = '"max_frames": 120,'

    # tranZ
    string_array[43] = '"translation_z": "0: (3*(sin(3.141*t/50)**3)+.75)",'

    # rotX
    string_array[46] = '"rotation_3d_x": "0: (0.25*sin(2*3.141*t/250))",'

    # rotY
    string_array[47] = '"rotation_3d_y": "0: (0.25*sin(2*3.141*t/250))",'

    # rotZ
    string_array[48] = '"rotation_3d_z": "0: (0.5*sin(2*3.141*t/250))",'

    # strength
    string_array[55] = '"strength_schedule": "0: (-0.13*(cos(3.141*t/13)**100)+0.63)",'

    # cadence: 2 - 4
    string_array[96] = '"diffusion_cadence": 4,'

    # string_array[33] = '"prompts": '+ '"{' + r"\"0\": \"" + f'{prompt}' + r'\"' + '}",'
    string_array[33] = f'"prompts": {{"0": "{prompt}"}},'
    # string_array[33] = '"prompts": '+ '"{' + '": "' + f'{prompt}' + '"' + '}",'

    # steps
    string_array[11] = '"steps": 15,'

    # output folder
    string_array[12] = '"batch_name": "dream",'

    # use init image: true or false
    # first run does not have an init image
    if first_run: string_array[15] = '"use_init": false,'
    else: string_array[15] = '"use_init": false,'

    # init image strength
    # TODO check if other values are more suitable
    string_array[16] = '"strength": 0.5,'

    # init image file
    if first_run: string_array[18] = '"init_image": null,'
    else: string_array[18] = f'"init_image": "{init_image}",'

    # skip video stiching: true or false
    string_array[234] = '"skip_video_creation": false,'

    # FPS
    string_array[235] = '"fps": 5,'

    string_array[252] = '"sd_model_name": "mdjrny-v4.ckpt",'

    request_string = "\n".join(string_array)

    with open(pwd + '/struct/request.json', 'w') as file:
        file.write(request_string)
