# -*- coding:utf-8 -*-
"""
    Japan's Population Dashboard on PyQt5 Python3.80
    System Development A 2022/05/20

    quote :
            regex :
"""
import math
import pprint
import statistics  # for median
import re
import sys

def fetchAllPref():
    """
    人口データCSVファイルから都道府県レベルでの人口データを抽出し, 各都道府県の人口を返す

    CSVの1行 : エリアコード 01000,エリア名,総人口,男性人口,女性人口
    :return : 都道府県別人口データ)[[都道府県コード,都道府県名,総人口,男性人口,女性人口],...]:: List[List[str,str,int,int,int],...]

    """
    _prefs = []  # 都道府県別人口レコードの集合
    f = open('FEH_00200521_220610143730.csv', 'r', encoding="utf-8")
    records = f.readlines()  # CSVファイルの内容を 1行毎に改行コードありで取得
    f.close()
    #print("records : ", records)

    # 正規表現パターンで エリアコード上2桁が01～47 かつ 残りの3桁が000の行を表現する
    # 全国及び都道府県の人口レコードのみ抽出
    ptn = re.compile(r'\d{2}(000)')  # 任意の数字2桁の直後に000が続く文字列にマッチ
    for p in records:
        #print("line: ", p)
        # CSVファイル内の1行ずつに対して処理
        flg = re.search(ptn, p)
        #print("flag: ", flg)
        if flg is not None:
            _prefs.append(p)  # 都道府県レコードであれば 追加し保持しておく
        #print(_prefs)

    if records is None:
        print("Error : Couldn't find the prefectures\' records", file=sys.stderr)

    del(_prefs[0])  # "全国の人口"のデータレコード prefs[0]を削除 -> # index: 北海道[0],...,沖縄県[46] <- '01000,北海道,"5,224,614","2,465,088","2,759,526"\n',...

    #print(_prefs)
    p = ''
    prefs =[[0 for m in range(5)] for n in range(47)]   # 整形した都道府県別人口レコード
    i = 0
    for p in _prefs:
        """
        _pref :: [str \n,str \n,...]
        p :: str
        各都道府県レコードを次の形式に整形 : 
        [[都道府県コード,都道府県名,総人口,男性人口,女性人口],...]
        [["01000","北海道",5224614,2465088,2759526],["02000","青森県",...],...]
        :: List[List[str,str,int,int,int]]
        """
        nameptn = re.compile(r',.*?(都|道|府|県),')
        popptn = re.compile(r',\".*?("\n$)')
        ppops = re.search(popptn, p)

        pcode = re.search(ptn,p)
        #print('pcode:', pcode.group())
        prefs[i][0] = pcode.group()  # 都道府県コード
        prefs[i][1] = re.search(nameptn, p).group().strip(',')  # 都道府県名
        if ppops is not None:
            ppops = ppops.group().lstrip(',\"').rstrip('\"\n').split('\",\"')  # 先頭の,"及び 末尾の"\nを除去し セパレタ","でリスト化
            #print(ppops)  # ['5,224,614', '2,465,088', '2,759,526']
            prefs[i][2] = int(ppops[0].replace(',', ''))  # 総人口 5,224,614' -> カンマ除去して intへ str -> int
            prefs[i][3] = int(ppops[1].replace(',', ''))  # 男性人口 str -> int
            prefs[i][4] = int(ppops[2].replace(',', ''))  # 女性人口 str -> int
        i += 1  # 0 - 46 :: int 都道府県別人口レコード 生成用


    #print("fetched: ", prefs)

    return prefs  # [[都道府県コード,都道府県名,総人口,男性人口,女性人口],...]:: List[List[str,str,int,int,int],...]


def getPops(prefs):
    """
    都道府県別人口のみからなるListを返す
    :param prefs:都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]]
    :return:都道府県別人口のみからなるList [0]～[46]
    """
    pops = []
    for i in prefs:
        pops.append(i[2])  # 都道府県別総人口のみからなるList生成 :: List[int]
    n = len(pops)  # 対象データの個数
    return pops




def avg(prefs):
    """
    47都道府県別人口の相加平均を返す
    :param prefs:都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの相加平均値 :: float
    """
    pops = getPops(prefs)
    n = len(pops)

    sum = 0
    if n == 47:
        for i in pops:
            sum += i
        return sum / n


def median(prefs):
    """
    47都道府県別人口の中央値を返す (データ数47であるため, 中央値は確実に原データ中に存在する)
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの中央値 :: float
    """
    pops = getPops(prefs)
    n = len(pops)

    med = statistics.median(pops)  # 標準ライブラリ statisticsを用いて 中央値 求める
    return med

def popmax(prefs):
    """
    47都道府県別人口中の 最大値 を返す
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの最大値 :: float
    """
    pops = getPops(prefs)

    return max(pops)





def popmin(prefs):
    """
    47都道府県別人口の 最小値 を返す
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの最小値 :: float
    """
    pops = getPops(prefs)

    return min(pops)


def var(prefs):
    """
    47都道府県別人口の 分散値を返す
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの分散値 :: float
    """
    pops = getPops(prefs)
    n = len(pops)

    devsum = 0  # 偏差の2乗和
    av = avg(prefs)  # 相加平均
    for i in pops:
        devsum += (i - av)**2  # 偏差の2乗和
    var = devsum / n
    return var



def stddev(prefs):
    """
    47都道府県別人口の 標準偏差値を返す
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :return:標準偏差値 :: float
    """
    # 標準偏差 = 分散の平方根
    sigma = math.sqrt(var(prefs))
    return sigma  # 標準偏差値








def calcStat():
    """
    都道府県別人口から,基本統計量を返す

    :return: 全国47都道府県の 平均人口,中央値,最大値,最小値,分散,標準偏差 :: dict[str,float]
    """
    prefs_data = fetchAllPref()
    result = {"avg": avg(prefs_data), "median": median(prefs_data), "max": popmax(prefs_data), "min": popmin(prefs_data), "variance": var(prefs_data),
              "std_dev": stddev(prefs_data)}
    # 基本統計量) avg:平均, median:中央値, max:最大, min:最小, variance:分散, std_dev:標準偏差(standard deviation) :: dict{str:float}

    return result


def mkRanking(option):
    """
    都道府県別人口ランキング順位を返す; 指標 : 最多,最少,中間...も示す
    :param option: ランキングリストのオプション: 降順:"1",昇順:"2"
    :return: 都道府県別人口ランキングリスト :: List[List[str,str,int,int,int],...]
    """
    prefsPops = fetchAllPref()  # :: List[List[str,str,int,int,int],...]  # 都道府県別人口レコードリスト
    sortedPops = sorted(prefsPops, key = lambda x: x[2])  # 都道府県別人口によって昇順にてソート

    if option == "2":
        return sortedPops  # 昇順でソートされた都道府県別人口リスト :: List[List[str,str,int,int,int],...]; min -> max
    elif option == "1":
        sortedPops.reverse()
        return sortedPops  # 降順でソートされた都道府県別人口リスト :: List[List[str,str,int,int,int],...]; max -> min


def showRanking(option):
    """
    都道府県別人口ランキング をCLI出力
    :param option:ランキングリストのオプション: 降順:"1",昇順:"2"
    :return: None
    """
    ranking = mkRanking(option)  # 指定された順序による都道府県別人口ランキングを生成
    print("   都道府県名,    総人口,    内男性,    内女性")
    rank = 1  #  ランキング順位 表示用
    fontcol = ['', '']  # ランキングレコード表示フォントの色
    for p in ranking:

        if option == "1":
            # 降順(#1:最大, #47:最小)
            if rank == 1:
                # 降順なら1位は最大値
                # 1位はフォント色変更
                fontcol = '\033[31m[最大]'  # 赤色文字
            elif rank == 47:
                # 降順なら47位は最小値
                # 47位はフォント色変更
                fontcol = '\033[34m[最小]'  # 青色文字
            else:
                fontcol = '\033[0m     '  # 色RESET
        elif option == "2":
            # 昇順(#1:最小, #2：最大)
            if rank == 1:
                # 昇順なら1位は最小値
                fontcol = '\033[34m[最小]'  # 青色文字
            elif rank == 47:
                # 昇順なら最大値
                fontcol = '\033[31m[最大]'  # 赤色文字
            else:
                fontcol = '\033[0m     '  # 色RESET
        if rank == 24:
            #  中央値
            fontcol = '\033[35m[中央値]'  # マゼンタ(MAGENTA)

        # ランキング表示部
        print(f"{fontcol}#{rank} : ", end='')
        for c in p[1:5]:
            print(c, end='    ')

        print('')
        rank += 1












if __name__ == '__main__':
    # main()
    #fetchAllPref()
    print("--- 日本全国の都道府県別人口 ---")
    result = calcStat()
    print(f"""平均値 : {result["avg"]} \n中央値 : {result["median"]} \n--- \n最大値 : {result["max"]} \n最小値 : {result["min"]} \n--- \n分散値 : {result["variance"]}\n標準偏差値 : {result["std_dev"]}\n------""")

    while 1:
        opt = input("\033[0m都道府県別人口ランキングを表示\n表示順を選択 1:降順(>) 2:昇順(<) 終了:9 >> ")  # フォント色RESETして表示
        if opt == "1":
            # 降順(上が最大, 下が最小)で表示
            print("--- 降順で表示 ---")
            #pprint.pprint(mkRanking(opt))
            showRanking(opt)

            print("--- -------- ---")
        elif opt == "2":
            # 昇順(上が最小, 下が最大)で表示
            print("--- 昇順で表示 ---")
            showRanking(opt)
            print("--- -------- ---")
        elif opt == "9":
            print("終了...")
            sys.exit()
        else:
            print("正しく選択してください")
