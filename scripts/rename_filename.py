import os;
from googletrans import Translator; 

translator = Translator(); 
path = 'c:\\Users\\EDY\\workspace\\traeproject\\fly\\downloads'; 
for filename in os.listdir(path): 
    name, ext = os.path.splitext(filename); 
    # 修改为异步调用或同步处理
    # 如果是异步方法，使用异步调用
    # loop = asyncio.get_event_loop()
    # translated = loop.run_until_complete(translator.translate(name, dest='en')).text
    # 修改为同步请求
    translated = translator.translate(name, dest='en').text
    # 如果想使用同步方式，可考虑使用其他同步翻译库
    new_name = translated.replace(' ', '_') + ext; 
    os.rename(os.path.join(path, filename), os.path.join(path, new_name))