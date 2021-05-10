# -*- coding:utf-8 -*-
import subprocess
import chardet
import sys
import re
import time
try:
    from dingding_robot import config
except:
    import config

def encrypt(env,encrypt_data,return_dict,num=0,jar_method="encrypt"):
    """加密数据
       param: env
       type: str
       value: rc or pro
       param：encrypt_data
       type: str
    """    
    if env.lower() == "rc":
        encryptPassword = config.RC_EncryptPassword
    elif env.lower() == "pro" or env.lower() == "prod" or env == "生产":
        encryptPassword = config.PRO_EncryptPassword
    else:
        print("[ERROR] 请输入环境和需要加密的数据\n python %s [rc or pro] [encrypt_data]" % (sys.argv[0]))
        return False

    command = "java -jar"
    jar_path = config.EncryptJar
    cmd = [command, jar_path, jar_method,encrypt_data, encryptPassword]    
    new_cmd = " ".join(cmd)    
    stdout,stderr = subprocess.Popen(new_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()    
    encoding = chardet.detect(stdout)["encoding"]
    if not encoding :
        encoding = "utf-8"
    re_pattern = r'\n(.*?)\n'
    if not stderr:        
        result = stdout.decode(encoding)
        result = re.findall(re_pattern, result)[0]
        print("%d 加密字段 %s，加密后 ENC(%s)"%(num + 1,encrypt_data,result))
        return_dict[num] = [encrypt_data,result]
        return "ENC(" + result + ")"
    else:
        result = stderr.decode(encoding)
        print("%s 错误 %s" % (jar_method,result))
    
    

if __name__ == '__main__':
    now_time = time.time()
    try:
        if len(sys.argv) == 4:
            print("[%s] result: ENC(%s)" % (sys.argv[3],encrypt(sys.argv[1],sys.argv[2],sys.argv[3])))
        else:
            encrypt(sys.argv[1],sys.argv[2])
        print("耗时：%.2fs" % (time.time()-now_time))
    except:
        print(sys.argv)
        print("[ERROR] 请输入环境和需要加密的数据。")
        print("python %s [rc or pro] [encrypt_data]" % (sys.argv[0]))




