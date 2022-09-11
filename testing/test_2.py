import re
txt = '123_ewq httpss (https://taxcom.ru/proverka-kontragentov/search/?query=7841437264&utm_sourcehttps=ofd&utm_medium=receipt&utm_campaign=receipt_ads&utm_content=receipt_link)'
print(re.findall(r'http\S+', txt))