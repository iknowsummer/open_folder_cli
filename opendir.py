import os, csv
import jaconv

# csvファイル
FILES_CSV = "dir_list.csv"
DIRS_PATH_CSV = "dirs_path.csv"

def main(files_csv,dirs_path):
    make_dirs_csv(dirs_path,files_csv)
    all_dirs = read_dir_list(files_csv)
    filtered_dirs = all_dirs.copy()

    while True:
        keywords = input('フォルダ顧客名？').split()

        if not keywords:
            continue

        #入力が1桁数字なら指定フォルダを開く動作
        if keywords[0].isdigit() and len(keywords[0]) == 1:
            pickNo = int(keywords[0])
            if 0 <= pickNo < len(filtered_dirs):
                openDir(filtered_dirs[pickNo])
            else:
                print("指定番号が範囲外です\n")

        #refreshコマンド
        elif keywords[0] == 'cmd' and len(keywords) > 1:
            if keywords[1] in ('-r', 'refresh'):
                print("コマンドrefresh。リストを再作成します。\n")
                make_dirs_csv(dirs_path,files_csv)
                #全てのディレクトリをリスト化
                all_dirs = read_dir_list(files_csv)
                filtered_dirs = all_dirs
        else:
            #ワードで対象フォルダをフィルタ
            filtered_dirs = dir_filter(keywords,all_dirs)

            #フィルタ結果を出力
            print_folders(filtered_dirs)

            #対象1個なら開く
            if len(filtered_dirs) == 1:
                openDir(filtered_dirs[0])


def print_folders(folders):
    """
    フォルダリストを出力する関数
    フォルダ数が10個まで番号を付与して出力（選択用）
    それ以上なら番号なしを1行で出力
    """
    print('')
    if len(folders) <= 10:
        for i,folder in enumerate(folders):
            folder_name = os.path.basename(folder)
            folder_parent = os.path.basename(os.path.dirname(folder))
            print(f"{i} {folder_name}【{folder_parent}】")
    else:
        for folder in folders:
            folder_name = os.path.basename(folder)
            print(folder_name,end=' / ')

        print("\n")
        print(f"{len(folders)}件のフォルダが見つかりました。")
        print("選択不可のため10個以下になるよう絞込んでください")
    print("")


def read_dir_list(files_csv):
    dir_list = []
    if os.path.exists(files_csv):
        # CSVファイルを開いてデータを読み込む
        with open(files_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                dir_list.append(row[0])
    else:
        print("リストが見つかりませんでした")
    return dir_list


def make_dirs_csv(dirs_path,files_csv):
    #対象ディレクトリを全てリスト化
    dir_list = []
    for path_dir in dirs_path:
        for item in os.listdir(path_dir):
            dir_list.append([os.path.join(path_dir,item)])

    # csvとして保存
    with open(files_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dir_list)


def dir_filter(keywords,all_dirs):

    filtered_dirs = all_dirs

    for keyword in keywords:
        keyword = jaconv.z2h(keyword,digit=True,ascii=True, kana=False)

        #キーワードごとに絞込み
        filtered_dirs = [
            dir for dir in filtered_dirs
            if keyword.lower() in dir.lower() ##小文字に変換して比較（表記ゆれ対策）
        ]

    #対象が無かった場合、csv再作成を促す
    if not filtered_dirs:
        print("見つかりませんでした。リストを再作成する場合は「cmd -r（またはrefresh）」を入力してください")

    return filtered_dirs


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