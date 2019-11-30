# -*- coding: utf-8 -*-
import os
import sys
import shutil
import tarfile
import pexpect
import datetime


# ----------------------日志文件下载/解压/关键字筛选脚本----------------------->
# author HAO
# slogan：花一点前期时间，之后就不用多次重复一个行程
# 注意 使用前要替换成对应的文件目录，不然会报 pexpect.EOF 错误
# -------------------------------------------------------------------------<


# tgz文件名称
def _file_name(default_=True):
    if default_:
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        file_name="log.%s.tar.gz"%yesterday # 当天分析昨天的日志
        return file_name
    else:
        return file_name  # 自定义文件名称

# 解压后文件存放的文件夹名称
def file2dir_name():
    # log.2019-11-21.tar.gz --> log.2019-11-21
    return _file_name()[:-7]

# 检查文件路径是否存在
def path_check(path=None):
    return True if path and os.path.exists(path) else False

# 检查是否是文件
def file_check(file=None):
    return True if file and os.path.isfile(file) else False

# 检查是否是文件夹
def dir_check(dir=None):
    return True if dir and os.path.isdir(dir) else False

# 获取文件夹中的文件名
def get_dir_file_name(dir_path=None):
    dir_file = os.listdir(dir_path) if dir_file else []
    return dir_file

# 创建文件夹/文件 注意是否有写入的权限
def dir_create(path=None):
    if path:
        os.makedirs(path)


file_src_dre = '/home/ubuntu/'                        # 源文件目录在这里 注：最后的 / 要带上
file_target_dre = "/Users/apple/Documents/"              # 文件下载到这里 注：最后的 / 要带上
file_release_dre = file_target_dre + file2dir_name()        # 文件解压到这里
file_src_host = "xxx"                             # 服务器host
file_src_username = "xxx"                                  # 服务器name
file_src_pwd = "xxx"                                   # 服务器 password
    
# 文件下载
class FileDownLoad(object):

    def __init__(self):
        self.log_name = _file_name()
        self.host=file_src_host
        self.username=file_src_username
        self.pwd=file_src_pwd
        self.src_file=file_src_dre
        self.dest_file=file_target_dre
        self.full_path="scp %s@%s:%s%s %s"%(self.username, self.host, self.src_file, self.log_name, self.dest_file)

    def run(self):

        try:
            print '(o__o) download start: >>>>>>'
            # 要执行的命令
            child = pexpect.spawn(self.full_path)
            # 日志指向标准输出
            child.logfile = sys.stdout
            # 执行命令后需要匹配的结果
            child.expect('.*password:')
            # 匹配成功后发送命令
            child.sendline(self.pwd)

            while 1:
                index = child.expect(['.*100%.*', pexpect.EOF, pexpect.TIMEOUT])  # 这里执行完成匹配的参数根据实际情况定
                if index == 0:
                    break
                elif index == 1:
                    print pexpect.EOF   
                    pass
                elif index == 2:
                    pass
            child.sendline('exit')
            child.sendcontrol('c')
            child.interact()
            print '(o__o) download end: <<<<<<'
            return (True, ok)
        except Exception as e:
            print e
            if 'Input/output error' in e:
                return (True, e)
            else:
                return (False, 'ERROR: %s'%e)


# tgz 文件解压
class TgzFileRelease(object):

    def __init__(self):
        self.file_path = file_target_dre
        self.file_release_path = file_release_dre
        if not path_check(self.file_release_path):
            dir_create(self.file_release_path)

        self.file_name = _file_name()
        self.file_dress = '%s%s'%(self.file_path, self.file_name)

    def run(self):
        try:
            print '(o__o) file-release start >>>>>>'
            t = tarfile.open(self.file_dress)
            # 解压后需要放到一个新文件夹
            t.extractall(path=self.file_release_path)
            # 把源文件也移动到新文件夹
            shutil.move(self.file_dress, self.file_release_path)
            print '(o__o) file-release end <<<<<<'
            return (True, 'ok')
        except Exception as e:
            return (False, e)


if __name__ == '__main__':

    l = FileDownLoad()   # 文件下载
    if l.run()[0]:
        t = TgzFileRelease()    # 文件解压
        if t.run()[0]:
            print 'info 解压成功'
        else:
            print 'info 解压失败'
    else:
        print 'info 下载失败'
