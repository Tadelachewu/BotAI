PS C:\Users\Tadele.Mesfin\BotAI> python botWithAiLanguageSelection.py
Traceback (most recent call last):
  File "C:\Users\Tadele.Mesfin\BotAI\botWithAiLanguageSelection.py", line 423, in <module>
    from flask import Flask, request
PS C:\Users\Tadele.Mesfin\BotAI> # Create virtual environment
>> python -m venv venv
>>
>> # Activate it (Windows)
>> venv\Scripts\activate
>>
>> # Upgrade pip with SSL verification disabled
>> python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org     
>>
>> # Now try installing
>> pip install flask python-dotenv pyTelegramBotAPI requests fpdf2
                                                                  s.pythonhosted.org\x0a\x0a# Now try installing\x0apip install flask python-dotenv pyTelegramBotAPI requests fpdf2;ce44e847-ea57-45eb-884a-f5910dRequirement already satisfied: pip in c:\users\tadele.mesfin\botai\venv\lib\site-packages (25.1.1)
Collecting flask
  Using cached flask-3.1.1-py3-none-any.whl.metadata (3.0 kB)
Collecting python-dotenv
  Using cached python_dotenv-1.1.1-py3-none-any.whl.metadata (24 kB)
Collecting pyTelegramBotAPI
  Using cached pytelegrambotapi-4.27.0-py3-none-any.whl.metadata (48 kB)
Collecting requests
  Using cached requests-2.32.4-py3-none-any.whl.metadata (4.9 kB)
Collecting fpdf2
  Using cached fpdf2-2.8.3-py2.py3-none-any.whl.metadata (69 kB)
Collecting blinker>=1.9.0 (from flask)
  Using cached blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting click>=8.1.3 (from flask)
  Using cached click-8.2.1-py3-none-any.whl.metadata (2.5 kB)
Collecting itsdangerous>=2.2.0 (from flask)
  Using cached itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting jinja2>=3.1.2 (from flask)
  Using cached jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting markupsafe>=2.1.1 (from flask)
  Using cached MarkupSafe-3.0.2-cp313-cp313-win_amd64.whl.metadata (4.1 kB)
Collecting werkzeug>=3.1.0 (from flask)
  Using cached werkzeug-3.1.3-py3-none-any.whl.metadata (3.7 kB)
Collecting charset_normalizer<4,>=2 (from requests)
  Using cached charset_normalizer-3.4.2-cp313-cp313-win_amd64.whl.metadata (36 kB)
Collecting idna<4,>=2.5 (from requests)
  Using cached idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting urllib3<3,>=1.21.1 (from requests)
  Using cached urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests)
  Using cached certifi-2025.7.9-py3-none-any.whl.metadata (2.4 kB)
Collecting defusedxml (from fpdf2)
  Using cached defusedxml-0.7.1-py2.py3-none-any.whl.metadata (32 kB)
Collecting Pillow!=9.2.*,>=6.2.2 (from fpdf2)
  Using cached pillow-11.3.0-cp313-cp313-win_amd64.whl.metadata (9.2 kB)
Collecting fonttools>=4.34.0 (from fpdf2)
  Using cached fonttools-4.58.5-cp313-cp313-win_amd64.whl.metadata (109 kB)
Collecting colorama (from click>=8.1.3->flask)
  Using cached colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
Using cached flask-3.1.1-py3-none-any.whl (103 kB)
Using cached python_dotenv-1.1.1-py3-none-any.whl (20 kB)
Using cached pytelegrambotapi-4.27.0-py3-none-any.whl (287 kB)
Using cached requests-2.32.4-py3-none-any.whl (64 kB)
Using cached charset_normalizer-3.4.2-cp313-cp313-win_amd64.whl (105 kB)
Using cached idna-3.10-py3-none-any.whl (70 kB)
Using cached urllib3-2.5.0-py3-none-any.whl (129 kB)
Using cached fpdf2-2.8.3-py2.py3-none-any.whl (245 kB)
Using cached blinker-1.9.0-py3-none-any.whl (8.5 kB)
Using cached certifi-2025.7.9-py3-none-any.whl (159 kB)
Using cached click-8.2.1-py3-none-any.whl (102 kB)
Using cached fonttools-4.58.5-cp313-cp313-win_amd64.whl (2.2 MB)
Using cached itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Using cached jinja2-3.1.6-py3-none-any.whl (134 kB)
Using cached MarkupSafe-3.0.2-cp313-cp313-win_amd64.whl (15 kB)
Using cached pillow-11.3.0-cp313-cp313-win_amd64.whl (7.0 MB)
Using cached werkzeug-3.1.3-py3-none-any.whl (224 kB)
Using cached colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Using cached defusedxml-0.7.1-py2.py3-none-any.whl (25 kB)
Installing collected packages: urllib3, python-dotenv, Pillow, markupsafe, itsdangerous, idna, fonttools, defusedxml, colorama, charset_normalizer, certifi, blinker, werkzeug, requests, jinja2, fpdf2, click, pyTelegramBotAPI, flask
   ━━━━━━━━━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━  6/19 [fonttools]