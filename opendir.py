import os, csv
import jaconv

# csvファイル
FILES_CSV = "dir_list.csv"
DIRS_PATH_CSV = "dirs_path.csv"

# dir_list を all_dirs と filtered_dirs に分けると
# 引数と関数の整理ができそう

# 起動時にリスト作成に変更

# リスト再作成のコマンド変更 cmd -rとか

def main(files_csv,dirs_path):

    while True:
        targets = input('フォルダ顧客名？').split()

        #入力が1桁数字ならコマンド実行
        if len(targets[0]) == 1:
            comand_num = targets[0]
            #入力が0～8なら指定フォルダを開く
            if comand_num in '012345678':
                pickNo = int(comand_num)
                opendir = dir_list[pickNo][1]
                openDir(opendir)

            #9が入力されたらcsv再作成
            elif comand_num == '9':
                print("9が入力されました。リストを再作成します。\n")
                make_dirs_csv(dirs_path,files_csv)
        else:
            #ワードごとに対象抜き出し。結果をファイルリストに戻すループ。
            dir_list = dir_filter(targets,files_csv)

            #リスト抽出し出力？？？
            printPickList(dir_list)

            #対象1個なら開く
            if len(dir_list) == 1:
                openDir(dir_list[0][1])


def printPickList(dir_fill):
    print('')
    if len(dir_fill) < 9:
        for i,dir in enumerate(dir_fill):
            print(i,dir[0],'【' + dir[1].split('\\')[-2] + '】')
    else:
        for dir in dir_fill:
            print(dir[0],end=' / ')
    print('')


def read_dir_list(files_csv):
    dir_list = []
    if os.path.exists(files_csv):
        # CSVファイルを開いてデータを読み込む
        with open(files_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                dir_list.append(row)
    else:
        print("リストが見つかりませんでした")
    return dir_list


def make_dirs_csv(dirs_path,files_csv):
    #対象ディレクトリを全てリスト化
    dir_list = []
    for path_dir in dirs_path:
        for item in os.listdir(path_dir):
            dir_list.append([item,os.path.join(path_dir,item)])

    # csvとして保存
    with open(files_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dir_list)


def dir_filter(targets,files_csv):
    dir_list = read_dir_list(files_csv)

    for target in targets:
        target = jaconv.z2h(target,digit=True,ascii=True, kana=False)

        #キーワードごとに絞込み
        dir_fill = []
        for dir in dir_list:
            if target.lower() in dir[0].lower(): ##小文字に変換して比較（表記ゆれ対策）
                dir_fill.append(dir)

        #AND検索用に絞込みリストを戻す
        dir_list = [item for item in dir_fill]

    #対象が無かった場合、csv再作成を促す
    if dir_list == []:
        print("見つかりませんでした。リストを再作成する場合は「9」を入力してください")

    return dir_list


def openDir(opendir):
    os.startfile(opendir)
    print(opendir,'\n')

def load_dirs_path(csv_path):
    dirs = []
    with open(csv_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                dirs.append(line)
    return dirs

if __name__ == "__main__":
    dirs_path = load_dirs_path(DIRS_PATH_CSV)
    main(FILES_CSV,dirs_path)