# -*- coding:utf-8 -*-
"""
    Japan's Population Dashboard on PyQt5 Python3.80
    System Development A 2022/05/20

    quote :
    Window : https://www.sejuku.net/blog/75467, https://teratail.com/questions/150883
    Widgets,Graphics :https://qiita.com/kenasman/items/73d01df973a25ae704e4
    MsgBox : https://webbibouroku.com/Blog/Article/qgis3-python-messagebox , https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMessageBox.html
"""
import re

def fetchAllPref():
    """
    人口データCSVファイルから都道府県レベルでの人口データを抽出し, 各都道府県の人口を返す

    CSVの1行 : エリアコード 01000,エリア名,総人口,男性人口,女性人口
    :return:
    """
    prefs = []  # 都道府県別人口レコードの集合
    f = open('FEH_00200521_220610143730.csv','r')
    records = f.readlines() # CSVファイルの内容を 1行毎に改行コードありで取得

    # 正規表現パターンで エリアコード上2桁が01～47 かつ 残りの3桁が000の行を表現する
    # 全国及び都道府県の人口レコードのみ抽出
    ptn = re.compile(r'/d{2}(000)')  # 任意の数字2桁の直後に000が続く文字列にマッチ
    for p in records:
        # CSVファイル内の1行ずつに対して処理
        flg = re.search(ptn, p)
        if flg is not None:
            prefs += p  # 都道府県レコードであれば 追加し保持しておく

    print(prefs)