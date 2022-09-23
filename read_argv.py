import sys

if __name__ == "__main__":
    args = sys.argv

    if len(args) < 3:
        print("コマンドライン引数が不足しています。")
        sys.exit()

    print(args[0])

    print(args[1])

    print(args[2])
