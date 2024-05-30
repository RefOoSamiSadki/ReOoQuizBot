import requests
def get_questions(grade_level, num_questions,topic):
    cookies = {
        'wordpress_sec_51743bf02438f6aa43cdbbcc069a735a': 'raafatsami%7C1712077231%7C25Wzq9UMcN54R72Cw2J0NOt07qNNHbXHeQ4W2wYGY65%7C2f9b6e532c1f47ae106a4d182d627928d2f65c278161c2c5bf7abd3e0869c763',
        'pmpro_visit': '1',
        '_gid': 'GA1.2.1472611423.1710866018',
        'holler-closed-popups': ',782,782,782',
        '_ga': 'GA1.1.1988653857.1710866017',
        'wordpress_test_cookie': 'WP%20Cookie%20check',
        'wordpress_logged_in_51743bf02438f6aa43cdbbcc069a735a': 'raafatsami%7C1712077231%7C25Wzq9UMcN54R72Cw2J0NOt07qNNHbXHeQ4W2wYGY65%7C89b4c64386c6feac381bbbd2bdd1c6efcb8f2939debc8e76fa91ba5226166fcd',
        '_ga_1C2DFTEWC3': 'GS1.1.1710866017.1.1.1710867633.0.0.0',
        '_ga_W3ZBX8XGDE': 'GS1.1.1710866017.1.1.1710867633.0.0.0',
        'holler-popup-views': '{"782":3,"786":1}',
        'holler-page-views': '8',
    }

    headers = {
        'authority': 'mcqgenerator.com',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://mcqgenerator.com',
        'referer': 'https://mcqgenerator.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action': 'gpt_generate_mcqs',
        'content': str(topic),
        'number': str(num_questions),
        'diff': str(grade_level),
    }
    response = requests.post('https://mcqgenerator.com/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data, timeout=1200)
    return response.json()
    # s = requests.Session()
    # headers = {
    #     'authority': 'auth.magicschool.ai',
    #     'accept': '*/*',
    #     'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    #     'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRudXB6eGZqcnVrc3VsdmZ5YW5sIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODIwNTIzNzIsImV4cCI6MTk5NzYyODM3Mn0.NxmabzXOOYo4zMqwJpEtNDewILVImuIxWZSPIuRaE2o',
    #     'content-type': 'application/json;charset=UTF-8',
    #     'origin': 'https://app.magicschool.ai',
    #     'referer': 'https://app.magicschool.ai/',
    #     'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-site',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    #     'x-client-info': 'supabase-js-web/2.38.4',
    # }

    # params = {
    #     'grant_type': 'password',
    # }

    # json_data = {
    #     'email': 'raafatsami101@gmail.com',
    #     'password': 'Ref@osami826491375',
    #     'gotrue_meta_security': {},
    # }

    # response = s.post('https://auth.magicschool.ai/auth/v1/token', params=params, headers=headers, json=json_data)
    # headers = {
    #     'authority': 'app.magicschool.ai',
    #     'accept': '*/*',
    #     'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    #     'authorization': 'Bearer ' + response.cookies['sb-access-token'],
    #     'content-type': 'application/json',
    #     'origin': 'https://app.magicschool.ai',
    #     'referer': 'https://app.magicschool.ai/tools/mc-assessment',
    #     'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    # }

    # json_data = {
    #     'id': 'mc-assessment',
    #     'gradeLevel': str(grade_level),
    #     'numQuestions': str(num_questions),
    #     'topic': str(topic),
    #     'locale': 'en-us',
    #     'role': 'teacher',
    # }

    # response = s.post('https://app.magicschool.ai/api/generations',headers=headers, json=json_data)
    