#!/usr/bin/env python
import sys
import os
import requests
from bs4 import BeautifulSoup
import json

filename = 'main.cpp'

inital_code = '''#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;
using ll = long long;

int main(){

}
'''

def login_test():
    f = open("./password.json",'r')
    account = json.load(f)
    s = requests.session()
    URL = "https://beta.atcoder.jp/login"
    r = s.get(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    csrftoken = (soup.find_all("input")[0]["value"])



    data = {
        "csrf_token":csrftoken,
        "password":account["password"],
        "username":account["username"]
    }

    r = s.post(URL,data)


    URL = "https://beta.atcoder.jp/contests/arc091/submissions/me"
    r = s.get(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup)

def init_with_contests(contest):
    tests = dict()
    f = open('./tests/'+contest+'.json','w')
    problem_index =[]
    if contest[:3] == 'arc':
        problem_index = ['a','b','c','d']

    for x in problem_index:
        target_url = 'https://beta.atcoder.jp/contests/'+contest +'/tasks/'+contest+'_'+x
        r = requests.get(target_url)
        soup = BeautifulSoup(r.text, 'lxml')
        pres = soup.find_all('pre')
        n = len(pres)
        assert(n % 4 == 2)
        samples = pres[1:n//2]

        t = dict()
        for i in range(len(samples)//2):
            t["input {}".format(i)] = samples[i*2].string
            t["output {}".format(i)] = samples[i*2+1].string

        tests["problem "+x] = t

    json.dump(tests,f,indent=4)


    print("finish download tests")
    try:
        for x in problem_index:

            f = open(filename[:-4]+'_'+x+'.cpp','w')
            f.write(inital_code)
            f.close
    except:
        print("error in creating initial cpp file")
        return
    print("init success")
    os.system('code .')


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
        if n==2:
            init()
        else:
            init_with_contests(argvs[2])
    elif argvs[1] == "run":
        if n==2:
            fn = filename
        else:
            fn = argvs[2]
        run(fn)

    elif argvs[1] == 'test':
        login_test()