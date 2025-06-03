import os, csv
import jaconv

# csvファイル
FOLDERS_CSV = "folders.csv"
SOURCE_PATHS_CSV = "source_paths.csv"

def main(folders_csv,source_paths):
    make_folders_csv(source_paths,folders_csv)
    all_folders = read_folders(folders_csv)
    filtered_folders = all_folders.copy()

    while True:
        keywords = input('フォルダ顧客名？').split()

        if not keywords:
            continue

        # 入力が1桁数字なら指定フォルダを開く
        if keywords[0] in "0123456789":
            open_select_folder(keywords[0],filtered_folders)
        # cmdコマンド
        elif keywords[0] == 'cmd' and len(keywords) > 1:
            execution_commands(keywords[1],folders_csv)
        #ワードで対象フォルダをフィルタ
        else:
            filtered_folders = folder_filter(keywords,all_folders)

            #フィルタ結果を出力
            print_folders(filtered_folders)

            #対象1個なら開く
            if len(filtered_folders) == 1:
                open_folder(filtered_folders[0])

def open_select_folder(select_num_str,folders):
    """
    選択した番号のフォルダを開く
    """
    pickNo = int(select_num_str)
    if 0 <= pickNo < len(folders):
        open_folder(folders[pickNo])
    else:
        print("指定番号が範囲外です\n")

def execution_commands(command,folders_csv):
    """
    コマンド実行関数
    cmdの後に続くコマンドを実行する
    """
    if command in ('-r', 'refresh'):
        print("コマンドrefresh。リストを再作成します。\n")
        make_folders_csv(source_paths,folders_csv)

    if command == 'exit':
        print("終了します。")
        exit()

def print_folders(folders):
    """
    フォルダリストを出力する関数
    フォルダ数が10個まで番号を付与して出力（選択用）
    それ以上なら番号なしを1行で出力
    """
    print('')
    if len(folders) <= 10:
        for i,folder in enumerate(folders):
            path_parts = folder.split('\\')

            folder_name = path_parts[-1]
            folder_parent = path_parts[-2] if len(path_parts) >= 2 else ''

            folder_parent_print = f"【{folder_parent}】" if folder_parent else ''

            print(f"{i} {folder_name} {folder_parent_print}")

    else:
        for folder in folders:
            folder_name = os.path.basename(folder)
            print(folder_name,end=' / ')

        print("\n")
        print(f"{len(folders)}件のフォルダが見つかりました。")
        print("選択不可のため10個以下になるよう絞込んでください")
    print("")


def read_folders(folders_csv):
    folders = []
    if os.path.exists(folders_csv):
        # CSVファイルを開いてデータを読み込む
        with open(folders_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                folders.append(row[0])
    else:
        print("リストが見つかりませんでした")
    return folders


def make_folders_csv(source_paths,folders_csv):
    """
    対象ディレクトリ内のフォルダを全てリスト化し
    csvファイルとして保存する
    """

    folders = []
    for path_folder in source_paths:
        for item in os.listdir(path_folder):
            if os.path.isdir(os.path.join(path_folder, item)):
                folders.append([os.path.join(path_folder,item)])

    # csvとして保存
    with open(folders_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(folders)


def folder_filter(keywords,all_folders):

    filtered_folders = all_folders

    for keyword in keywords:
        keyword = jaconv.z2h(keyword,digit=True,ascii=True, kana=False)

        #キーワードごとに絞込み
        filtered_folders = [
            folder for folder in filtered_folders
            if keyword.lower() in folder.lower() ##小文字に変換して比較（表記ゆれ対策）
        ]

    #対象が無かった場合、csv再作成を促す
    if not filtered_folders:
        print("見つかりませんでした。リストを再作成する場合は「cmd -r（またはrefresh）」を入力してください")

    return filtered_folders


def open_folder(folder):
    """
    指定されたフォルダを開く
    """
    print('\n',f"open: {folder}",'\n')
    os.startfile(folder)

def load_source_paths(csv_path):
    source_paths = []
    with open(csv_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                source_paths.append(line)
    return source_paths

if __name__ == "__main__":
    source_paths = load_source_paths(SOURCE_PATHS_CSV)
    main(FOLDERS_CSV,source_paths)