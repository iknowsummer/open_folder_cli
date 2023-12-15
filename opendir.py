import subprocess
import os, glob
import jaconv

# path_dir = r"\\192.168.1.199\product\その他"
# dir_list = os.listdir(path_dir)

path_dirs = [
    r"\\192.168.1.199\product\その他",
    r"\\192.168.1.199\product\印刷関係",
    r"\\192.168.1.199\product\個人",
    r"\\192.168.1.199\web"
]

def main():
    while True:
        targets = input('フォルダ顧客名？').split()

        #入力が1桁数字なら絞込み→開く
        if len(targets[0]) == 1 and targets[0].isdigit():
            pickNo = int(targets[0])
            opendir = output_dirs[pickNo][1]
            openDir(opendir)
            break

        #ワードごとに対象抜き出し。結果をファイルリストに戻すループ。
        output_dirs = getTargets(targets)

        #リスト抽出し出力？？？
        printPickList(output_dirs)

        #対象1個なら強制的に開く
        if len(output_dirs) == 1:
            opendir = output_dirs[0][1]
            openDir(opendir)
            break


#############################
#############################
#############################

def printPickList(dir_fill):
    #対象10個以下ならリスト。それ以上なら羅列
    print('')
    if len(dir_fill) < 10:
        for i,dir in enumerate(dir_fill):
            print(i,dir[0],'【' + dir[1].split('\\')[-2] + '】')
    else:
        for dir in dir_fill:
            print(dir[0],end=' / ')
    print('')


def getTargets(targets):

    #対象ディレクトリを全てリスト化
    dir_all = []
    for path_dir in path_dirs:
        for item in os.listdir(path_dir):
            dir_all.append([item,os.path.join(path_dir,item)])

    #出力用（この処理不要……？）
    dir_out = dir_all

    for target in targets:
        target = jaconv.z2h(target,digit=True,ascii=True, kana=False)

        #キーワードごとに絞込み
        dir_fill = []
        for dir in dir_out:
            if target.lower() in dir[0].lower(): ##小文字に変換して比較（表記ゆれ対策）
                dir_fill.append(dir)

        #AND検索用に絞込みリストを戻す
        dir_out = [item for item in dir_fill]
        
    return dir_out

def openDir(opendir):
    subprocess.Popen(['explorer',opendir],shell=True)
    print(opendir,'\n')


if __name__ == "__main__":
    main()