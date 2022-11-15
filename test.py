import requests
import os
import json

# path = os.path('/attachments/file1.html')
# print(path)
# path = os.path.abspath("attachments/file1.html")
# # path_new = "http://" + path
# # print(path_new)
# receive = requests.get('http://127.0.0.1:5500/attachments%20/file1.html')
# print(receive.headers)

import os
cwd = os.getcwd()
path = cwd + "/attachments/file1.html"
# path_new = "/Users/anishdhandore/Documents/CSUSM/Courses /7 Fall 2022/CS 436/FinalProject_Networking/attachments /file1.html"
print(path)
print(os.path.exists(path))
# /Users/anishdhandore/Documents/CSUSM/Courses /7 Fall 2022/CS 436/FinalProject_Networking/attachments /file1.html