# -*- coding:utf-8 -*-
"""
    Japan's Population Dashboard on PyQt5 Python3.80
    System Development A 2022/05/20

    quote :
            regex :
"""
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

def avg(pops):
    """
    与えられたデータ群の相加平均を返す
    :param pops: 原データリスト :: List[int]
    :return:原データリストの相加平均値 :: float
    """
    n = len(pops)  # 対象データの個数
    sum = 0
    for i in pops:
        sum += i
    return sum / n





def calcStat(prefs):
    """
    都道府県別人口を受け取り,基本統計量を返す
    :param prefs: 都道府県別人口レコード :: List[List[str,str,int,int,int],...] :
    :return: 全国47都道府県の 平均人口,中央値,最大値,最小値,分散,標準偏差 :: dict[str,float]
    """
    result = {"avg": 0, "median": 0, "max": 0, "min": 0, "variance": 0, "std_dev": 0}
    # 基本統計量) avg:平均, median:中央値, max:最大, min:最小, variance:分散, std_dev:標準偏差(standard deviation) :: dict{str:float}

    result["avg"] = pref# 平均

    return result
def doRanking(prefs, option):
    """
    指標ごとの 都道府県別人口ランキング順位を返す; 指標 : 最多,最少,中間...
    :param prefs: 都道府県別人口データレコード
    :param option: ランキングリストのオプション: 降順(既定):0,昇順:1
    :return: 都道府県別人口ランキング順位 :: list[int]
    """





if __name__ == '__main__':
    # main()
    fetchAllPref()
    print(avg([1,99]))