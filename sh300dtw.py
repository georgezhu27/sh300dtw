#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""用DTW算法找到沪深300指数
历史行情与最近10天走势最相似的一段
"""

__author__ = 'yzlnew'

import tushare as ts
from numpy.linalg import norm
import matplotlib.pyplot as plt
from dtw import dtw


def GetData(start_date, end_date):
    raw_data = ts.get_k_data('000300', index=True,
                             start=start_date, end=end_date)
    selected_data = raw_data.loc[:, ['date', 'close']]
    data = selected_data.set_index('date')
    return data


def DtwDist(series1, series2):
    dist, cost, acc, path = dtw(
        series1, series2, dist=lambda x, y: norm(x - y, ord=1))
    return dist


def main():
    ten_day_data = GetData('2017-05-18', '2017-06-02')
    ten_day_data_array = ten_day_data.values / ten_day_data.values.max()
    historydata = GetData('2005-04-08', '2017-05-17')

    pos = 0  # 记录在历史行情记录里的位置
    min_dist = 1  # 最小的距离
    min_array = []  # 最相似的序列

    for x in range(len(historydata.index) - 10):
        current_data = historydata[x:x + 10]
        current_array = current_data.values / current_data.values.max()
        current_dist = DtwDist(ten_day_data_array, current_array)
        if current_dist < min_dist:
            min_dist = current_dist
            min_array = current_array
            pos = x

    print historydata[pos:pos + 10]
    plt.plot(ten_day_data_array, label='The last 10 days')
    plt.plot(min_array, label='Match')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
