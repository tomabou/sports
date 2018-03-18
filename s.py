#!/usr/bin/env python
import sys
import os

filename = 'main.cpp'

inital_code = '''
#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;
using ll = long long;

int main(){

}
'''


def init():
    print("** init **")
    try:
        f = open(filename,'w')
        f.write(inital_code)
        f.close
    except:
        print("error in init")
        return
    print("init success")
    os.system('code .')


def run(fn):
    print("compile "+fn)
    os.system('g++ -std=c++14 '+fn)
    print("run program \n")
    os.system('./a.out')


if __name__ == "__main__":
    print("this is atcoder supporter")

    argvs = sys.argv
    n = len(argvs)
    if n==1:
        print("コマンドライン引数が必要です")
    elif argvs[1] == "init":
        init()
    elif argvs[1] == "run":
        if n==2:
            fn = filename
        else:
            fn = argvs[2]
        run(fn)