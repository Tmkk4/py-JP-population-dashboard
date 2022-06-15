# -*- coding:utf-8 -*-
"""
    Japan's Population Dashboard on PyQt5 Python3.80
    System Development A 2022/05/20

    quote :
            regex :
"""
import math
import statistics  # for median
import re
import sys

def fetchAllPref():
    """
    人口データCSVファイルから都道府県レベルでの人口データを抽出し, 各都道府県の人口を返す

    CSVの1行 : エリアコード 01000,エリア名,総人口,男性人口,女性人口
    :return : 都道府県別人口データ) :: list[str] : '01000,北海道,"5,224,614","2,465,088","2,759,526"\n', ..
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


    print("fetched: ", prefs)

    return prefs  # [[都道府県コード,都道府県名,総人口,男性人口,女性人口],...]:: List[List[str,str,int,int,int],...]



def avg(prefs):
    """
    47都道府県別人口の相加平均を返す
    :param prefs:都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの相加平均値 :: float
    """
    pops = []
    for i in prefs:
        pops.append(i[2])  # 都道府県別総人口のみからなるList生成 :: List[int]
    n = len(pops)  # 対象データの個数
    sum = 0
    if n == 47:
        for i in pops:
            sum += i
        return sum / n
    else:
        return "< 47 data"  # データが不完全

def median(prefs):
    """
    47都道府県別人口の中央値を返す (データ数47であるため, 中央値は確実に原データ中に存在する)
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの中央値 :: float
    """
    pops = []
    for i in prefs:
        pops.append(i[2])  # 都道府県別総人口のみからなるList生成 :: List[int]
    n = len(pops)  # 対象データの個数

    med = statistics.median(pops)  # 標準ライブラリ statisticsを用いて 中央値 求める
    return med

def popmax(prefs):
    """
    47都道府県別人口中の 最大値 を返す
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの最大値 :: float
    """
    pops = []
    for i in prefs:
        pops.append(i[2])  # 都道府県別総人口のみからなるList生成 :: List[int]
    n = len(pops)  # 対象データの個数

    return max(pops)





def popmin(prefs):
    """
    47都道府県別人口の 最小値 を返す
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの最小値 :: float
    """
    pops = []
    for i in prefs:
        pops.append(i[2])  # 都道府県別総人口のみからなるList生成 :: List[int]
    n = len(pops)  # 対象データの個数

    return min(pops)


def var(prefs):
    """
    47都道府県別人口の 分散値を返す
    :param prefs: 都道府県別人口レコード :: List[List[str(都道府県コード),str(都道府県名),int(総人口),int(男性人口),int(女性人口)]
    :param pops: 原データリスト :: List[int]
    :return:原データリストの分散値 :: float
    """
    pops = []
    for i in prefs:
        pops.append(i[2])  # 都道府県別総人口のみからなるList生成 :: List[int]
    n = len(pops)  # 対象データの個数

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


def mkRanking(prefs, option):
    """
    指標ごとの 都道府県別人口ランキング順位を返す; 指標 : 最多,最少,中間...
    :param prefs: 都道府県別人口データレコード
    :param option: ランキングリストのオプション: 降順(既定):0,昇順:1
    :return: 都道府県別人口ランキング順位 :: list[int]
    """





if __name__ == '__main__':
    # main()
    #fetchAllPref()
    print(avg(fetchAllPref()))
    print(var(fetchAllPref()))
    print(stddev(fetchAllPref()))
    print(median(fetchAllPref()))
    print(popmax(fetchAllPref()))
    print(popmin(fetchAllPref()))