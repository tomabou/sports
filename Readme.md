## Atcoder サポーター

atcoderの補助ツールです。

## 実行環境
python3
g++
ubuntuでしか試していませんが、python3の環境があれば動くと思います

## How to use
まずcloneします。
```
git clone https://github.com/tomabou/sports.git
```
cloneしたディレクトリで、
```
./s.py init agc023
```
とするとテストケースをダウンロードし、ソースコードの雛形を作ります。

```
./s.py login
```
でatcoderにloginします。（初回だけpasswordを入力してください）

```
./s.py run agc023 a
```
とするとa問題をコンパイルして実行して、テストを通るとsubmitします（通らなくてもsubmit出来ます）

```
agcのc問題はURLを見ると分かるようにa問題として処理しているので注意してください。(arcはa,b,c,d問題があるとして処理しています)