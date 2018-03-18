#!/usr/bin/env python
import sys
import os
import requests
from bs4 import BeautifulSoup
import pickle
import json
import subprocess

inital_code = '''#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;
using ll = long long;

int main(){

}
'''
def get_ploblem_index(contest):
    if contest[:3] == 'arc':
        return ['a','b','c','d']
    else: 
        print('undefind')
        return []


def login():
    f = open("./.password.json",'r')
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
    with open('.session.pickle', 'wb') as fp:
        pickle.dump(s, fp)

def download_test(contest):
    tests = dict()
    f = open('./tests/'+contest+'.json','w')
    problem_index = get_ploblem_index(contest)

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
            t["input {}".format(i)] = samples[i*2].string.replace('\r','')
            t["output {}".format(i)] = samples[i*2+1].string.replace('\r','')

        tests["problem "+x] = t

    json.dump(tests,f,indent=4)

    print("finish download tests")

def create_inital_cppfiles(contest):
    
    problem_index = get_ploblem_index(contest)
    try:
        for x in problem_index:
            f = open('./src/main_'+x+'.cpp','w')
            f.write(inital_code)
            f.close
    except:
        print("error in creating initial cpp file")
        return

def run_editor():
    os.system('code .')


def init():
    print("** init **")
    try:
        f = open("./src/main.cpp",'w')
        f.write(inital_code)
        f.close
    except:
        print("error in init")
        return
    print("init success")


def run(fn):
    print("compile "+fn)
    os.system('g++ -std=c++14 '+fn)
    print("run program \n")
    os.system('./a.out')

def build_and_test(contest,problem):
    filename = "./src/main_"+problem+".cpp"

    print("compile "+filename)
    os.system('g++ -std=c++14 '+filename)
    print("test program \n")

    f = open("./tests/"+contest + ".json" ,'r')
    test = json.load(f)
    test = test["problem "+problem]
    i = 0
    while ("input {}".format(i) in test):
        f = open("temp.txt" ,'w')
        
        print("-------------------------------")
        test_in = test["input {}".format(i)]
        f.write(test_in)
        f.close()
        f = open("temp.txt",'r')
        print("input {}".format(i))
        res = subprocess.run("./a.out",stdin = f, stdout=subprocess.PIPE)
        f.close()
        res = res.stdout
        if(test["output {}".format(i)].encode() == res):
            print("OK!")
        else:
            print(res)
            print(test["output {}".format(i)].encode())
        
        i = i+1

    os.system("rm temp.txt")

if __name__ == "__main__":
    print("this is atcoder supporter")
    if not os.path.exists("./src"):
        os.mkdir("./src")
    if not os.path.exists("./tests"):
        os.mkdir("./tests")

    argvs = sys.argv
    n = len(argvs)
    if n==1:
        print("コマンドライン引数が必要です")
    elif argvs[1] == "init":
        if n==2:
            init()
            run_editor()
        else:
            download_test(argvs[2])
            create_inital_cppfiles(argvs[2])
            run_editor()
    elif argvs[1] == "run":
        if n==2:
            fn = "./src/main.cpp"
            run(fn)
        else:
            build_and_test(argvs[2],argvs[3])

    elif argvs[1] == "load":
        if n==2:
            print("コンテスト名を入力してください")
        else:
            download_test(argvs[2])
    elif argvs[1] == "login":
        login()

    elif argvs[1] == 'test':
        login()