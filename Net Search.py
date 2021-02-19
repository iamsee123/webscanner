'''
    @author: iamsee123
    @Description 简单网站后台扫描器
'''

from multiprocessing.dummy import Pool as ThreadPool
import requests
import argparse

'''
    函数功能：命令行输入处理
    输入：无
    输出：所要完成的任务
'''

def arg_handle():
    parser = argparse.ArgumentParser(description='Net Search')
    parser.add_argument("-u","--url",help = 'Target URL',dest='url')
    parser.add_argument('-d','--dic',help = 'Dictionary path',dest='dic')
    parser.add_argument('-n','--num',help = 'Thread number,default number is 5',type = int,dest='num',default=5)
    parser.add_argument('-t','--time',help = 'Timeout,default 5',type = int,dest='timeout',default=5)
    opts = parser.parse_args()
    return opts

'''
    函数功能：多线程
    输入：url，dic的列表,线程数
    输出:多线程执行的结果
'''
def multi_handler(urls,thread_num):
    pool = ThreadPool(processes=thread_num)
    res = pool.map(check_url,urls)
    pool.close()
    pool.join()
    return res

'''
    函数功能：后台扫描
    输入：目标URL和字典
    输出：有返回的链接
'''
def check_url(target_list):
    urls,dir = target_list
    if dir.startswith('/'):
        dir = dir[1:] #有些开头有/，统一处理
    dir = dir.replace("\r\n","")
    final_url = urls + "/" + dir
    try:
        req = requests.head(final_url,timeout = TIMEOUT)
        if req.status_code not in [404,500]:
            return final_url
    except Exception as e:
        print(e)
    return ""

'''
    函数功能：开场动画
    输入：无
    输出：无
'''
def open_anime():
    print('''
    
  o              o                 o                  o__ __o                                                                         
 <|>            <|>               <|>                /v     v\                                                                        
 / \            / \               / >               />       <\                                                                       
 \o/            \o/    o__  __o   \o__ __o         _\o____            __o__    o__ __o/  \o__ __o   \o__ __o     o__  __o   \o__ __o  
  |              |    /v      |>   |     v\             \_\__o__     />  \    /v     |    |     |>   |     |>   /v      |>   |     |> 
 < >            < >  />      //   / \     <\                  \    o/        />     / \  / \   / \  / \   / \  />      //   / \   < > 
  \o    o/\o    o/   \o    o/     \o/      /        \         /   <|         \      \o/  \o/   \o/  \o/   \o/  \o    o/     \o/       
   v\  /v  v\  /v     v\  /v __o   |      o          o       o     \\         o      |    |     |    |     |    v\  /v __o   |        
    <\/>    <\/>       <\/> __/>  / \  __/>          <\__ __/>      _\o__</   <\__  / \  / \   / \  / \   / \    <\/> __/>  / \       
    
    ''')


def main():
    opts = arg_handle()
    url = opts.url
    if not url:
        print("lack url")
        return 0
    if url.startswith("http") is False:
        print("Strat with http is a better option")
        url = "http://" + url;
    if url.endswith("/"):
        url = url[:-1]
    num = opts.num
    dic_path = opts.dic or "small.txt"
    global TIMEOUT
    TIMEOUT = opts.timeout
    try:
        f = open(dic_path,encoding='utf-8').read()
    except IOError as e:
        print(e)
    else:
        links = f.split("\n")
        pair_url_dir = []
        for link in links:
            link.strip()
            pair_url_dir.append((url,link))
        res = multi_handler(pair_url_dir,num)
    print("find links" , [x for x in res if x])

if __name__ ==  "__main__":
    open_anime()
    main()


