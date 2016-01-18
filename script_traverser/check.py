# -*- coding: utf-8 -*-
'''
authored by albert zhao
NJU dislab
partially imported from ' HARparser/url_process.py ' by albert zhao
'''
import re
import os
import sys

#PATH = 'E:\0.正在处理ing\forFun\check_fft\target_code'
PATH = 'target_code/'
TARGET_WORD = r'fft|FFT|Fourier|ft|FT|mesh'
PATH = '/home/albert/Documents/CODE&PROJECT/GIT_launch_platform/lorcon-old'
#TARGET_WORD = r'wtinj_open\(|tx80211_mac80211_init\(|tx80211_resolvecard\(|tx80211_init\(|tx80211_open\(|tx80211_initpacket\(|tx80211_radiotap_header'
TARGET_WORD = r'authored by albert Z'
N = 10

def traverse_file( path):
    files = os.listdir(path)
    for fi in files:
        tmp = path+'/'+fi
        if os.path.isfile( tmp):
            f = open( tmp)
            text = f.read()
#            result = re.findall(TARGET_WORD, text)
            result = get_urlSet_from_text( text, TARGET_WORD, N)
            if( len(result) != 0):
                print "FILE_NAME:",tmp
                print result,"\n"
        elif os.path.isdir( tmp):
            traverse_file( tmp)
            
def get_urlSet_from_text( data, pattern, n=10):
    '''
    input: response content, pattern
    output: urls extracted from the content
    '''
    pos = 0
    res_arr = []
    mat=re.search( pattern, data)
    while mat != None:
        start = pos+ mat.start()
        end = pos+ mat.end()
        res_arr.append( data[ start-n: end+n])
        pos = pos + mat.end()
        mat = re.search( pattern, data[pos:])
    return res_arr
            
if __name__ == '__main__':
    if len( sys.argv)>0:
        print "TARGET WORDS:"
        flag = 0
        for i in range(1,len(sys.argv)):
            if '-n'==sys.argv[i]:
                N = int(sys.argv[i+1])
                flag = 1
                continue
            if flag ==1:
                flag = 0
                continue
            if '-p' ==sys.argv[i]:
                PATH = sys.argv[i+1]
                flag = 1
            TARGET_WORD = TARGET_WORD + r'|'+ sys.argv[i]
            print sys.argv[i]
        print "===================================================\n"
    traverse_file( PATH)