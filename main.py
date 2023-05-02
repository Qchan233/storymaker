# -*- coding: utf-8 -*-
import openai
import os
import re

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def txt_to_dict(filename):
  # 创建一个空的字典
  result = {}
  # 打开文件
  with open(filename, "r", encoding='utf-8') as f:
    # 遍历每一行
    for line in f:
      # 去掉换行符
      line = line.strip()
      # 如果行不为空
      if line:
        # 用冒号分割key和value
        key, value = line.split("：")
        # 把key和value加入字典
        result[key] = value
  # 返回字典
  return result
    

api_key = input("请输入你的API key: ")
openai.api_key = api_key

messages =  [  
{'role':'system', 'content':'请担任一名游戏主持人。先等待玩家输入游戏的设定信息，其中会包括背景、角色、名字、描述和主题。你根据这些信息逐步生成一个故事，要详细描述情节、人物和场景。情节要惊险刺激，玩家会遇到很多危险。\
 在关键时刻提供给玩家3-4个选项，用数字标号。根据玩家的选择，玩家可以通过数字选择或者描述自己的选择。你要根据选择和合理程度来判断是否成功，过于危险或者不合理的行为会导致游戏失败。推进故事直到结局。当游戏结束，你需要在文本后加入<end>标记.'},    
{'role':'assistant', 'content':'欢迎来到我们的角色扮演游戏，我是你的游戏主持人！首先，请告诉我游戏的背景设定以及你想扮演的角色。例如，游戏背景可以是一个奇幻世界、科幻宇宙或者是现代城市。角色可以是勇敢的骑士、聪明的侦探或者其他任何你感兴趣的角色。请向我描述你的设想，我会根据你的选择编织一个故事。'},
]
print('-'*50+'\n')
# background = input('请输入故事背景：')
# character = input('请输入人物：')
# name = input('请输入人物名字：')
# description = input('(可选)请输入人物描述：')

# infos = {'背景': background, '人物': character, '名字': name}
# messages.append({'role':'user', 'content':str(infos)})
# if description:
#     infos['描述'] = description

result = txt_to_dict('infos.txt')
print(result)

messages.append({'role':'user', 'content':str(result)})
response = get_completion_from_messages(messages, temperature=0.1)
print(response)
messages.append({'role':'assistant', 'content':response})

end_pattern = re.compile(r'<end>')

while(True):
    option = input('请输入选项或者描述你的选择：')
    messages.append({'role':'user', 'content':option})
    response = get_completion_from_messages(messages, temperature=0.1)
    print('-'*50+'\n')
    print(response)
    messages.append({'role':'assistant', 'content':response})

    match = end_pattern.search(response)
    if match:
      print('-'*50+'\n')
      break

input('按任意键退出')