def load_sys_prompt():
    prompt =  ''
    
    with open('./resources/system_prompt.txt', 'r') as prompt_file:
        prompt = prompt_file.read()

    return prompt
