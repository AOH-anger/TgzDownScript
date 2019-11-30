# TgzDownScript
Tgz文件自动下载/解压

## 功能
* 支持从远程服务器下载到本地
* 自动解压
* 源/解压文件放入同一个文件夹

## 运行
* python scritp.py

## 注意事项
1. 自定义源文件名称
    - _file_name() 
2. 自定义源文件目录 注：最后的 / 要带上
    - file_src_dre = '/home/ubuntu/'                        
3. 自定义文件下载目录 注：最后的 / 要带上
    - file_target_dre = "/Users/apple/Documents/"           
4. 文件解压到这里
    - file_release_dre = file_target_dre + file2dir_name()  
5. 服务器host
    - file_src_host = "xxx"                                 
6. 服务器name
    - file_src_username = "xxx"                             
7. 服务器password
    - file_src_pwd = "xxx"                                  


## ERROR INFO
1. 输出 <class 'pexpect.exceptions.EOF'> 
    - 请确认注意事项中需要自定义的信息是否填写以及填写是否正确