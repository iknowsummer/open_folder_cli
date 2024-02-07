import subprocess
import os, glob, csv
import jaconv

# path_dir = r"\\192.168.1.199\product\その他"
# dir_list = os.listdir(path_dir)

# csvファイルを設定
csv_file_name = "dir_list.csv"

# pyファイルのフォルダを取得
# current_file_path = os.path.abspath(__file__)
# current_dir = os.path.dirname(current_file_path)
# csv_file_path = os.path.join(current_dir, csv_file_name)
csv_file_path = csv_file_name

path_dirs = [
    r"\\192.168.1.199\product\その他",
    r"\\192.168.1.199\product\印刷関係",
    r"\\192.168.1.199\product\個人",
    r"\\192.168.1.199\web"
]

def main():
    while True:
        targets = input('フォルダ顧客名？').split()

        #入力が1桁数字なら別対応
        if len(targets[0]) == 1 :
            #入力が0～8なら指定を開く
            # if targets[0].isdigit():
            if targets[0] in '012345678':
                pickNo = int(targets[0])
                opendir = output_dirs[pickNo][1]
                openDir(opendir)
                break
            #9が入力されたらcsv再作成
            if targets[0] == "9":
                print("9が入力されました。リストを再作成します。\n")
                make_dir_list()
                continue

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
    #対象9個以下ならリスト。それ以上なら羅列
    print('')
    if len(dir_fill) < 9:
        for i,dir in enumerate(dir_fill):
            print(i,dir[0],'【' + dir[1].split('\\')[-2] + '】')
    else:
        for dir in dir_fill:
            print(dir[0],end=' / ')
    print('')


def read_dir_list():
    dir_list = []
    if os.path.exists(csv_file_path):
        # CSVファイルを開いてデータを読み込む
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                dir_list.append(row)
    else:
        print("リストが見つかりませんでした")
    return dir_list



def make_dir_list():
    #対象ディレクトリを全てリスト化
    dir_list = []
    for path_dir in path_dirs:
        for item in os.listdir(path_dir):
            dir_list.append([item,os.path.join(path_dir,item)])

    # csvとして保存
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dir_list)

def getTargets(targets):

    #出力用（この処理不要……？）
    dir_out = read_dir_list()

    for target in targets:
        target = jaconv.z2h(target,digit=True,ascii=True, kana=False)

        #キーワードごとに絞込み
        dir_fill = []
        for dir in dir_out:
            if target.lower() in dir[0].lower(): ##小文字に変換して比較（表記ゆれ対策）
                dir_fill.append(dir)

        #AND検索用に絞込みリストを戻す
        dir_out = [item for item in dir_fill]

    #対象が無かった場合、csv再作成を促す
    if dir_out == []:
        print("見つかりませんでした。リストを再作成する場合は「9」を入力してください")

    return dir_out

def openDir(opendir):
    subprocess.Popen(['explorer',opendir],shell=True)
    print(opendir,'\n')


if __name__ == "__main__":
    main()