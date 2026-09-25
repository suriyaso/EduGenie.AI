import requests
payload = {'text': 'What is Python?', 'level': 'beginner'}
for path in ['/qa', '/explain', '/quiz', '/summarize', '/learn/recommendations']:
    try:
        r = requests.post('http://127.0.0.1:8000' + path, json=payload, timeout=20)
        print('PATH', path)
        print('STATUS', r.status_code)
        print(r.text[:1200])
        print('---')
    except Exception as e:
        print('PATH', path, 'ERROR', repr(e))
