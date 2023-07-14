# -*- coding: utf-8 -*-

import xlrd, xlwt
from xlutils.copy import copy


def get_excelData(sheetName, startCol, endCol, resValueCol, expValueCol):
    """

    :param sheetName: sheet名
    :param startCol: 开始行，从1开始数
    :param endCol: 结束行
    :param resValueCol: 请求体，列从0开始数
    :param expValueCol: 预期响应，列从0开始数
    :return:
    """
    excelDir = '../Data/运单相关接口.xls'
    workBook = xlrd.open_workbook(excelDir, formatting_info=True)
    workSheet = workBook.sheet_by_name(sheetName)
    res_list = []
    for cnt in range(startCol - 1, endCol):
        res_value = workSheet.cell_value(cnt, resValueCol)
        exp_value = workSheet.cell_value(cnt, expValueCol)
        res_list.append((res_value, exp_value))
    return res_list


def write_excelData(sheet_index, x, y, data):
    '''
    :param sheet_index: sheet序号
    :param x: 行
    :param y: 列
    :param data: 写入数据
    :return:
    '''
    try:
        excelDir = '../Data/运单相关接口.xls'
        workBook = xlrd.open_workbook(excelDir, formatting_info=True)
        workBook = copy(workBook)
        workSheet = workBook.get_sheet(sheet_index)
        workSheet.write(x, y, data)
        workBook.save(excelDir)
    except Exception as e:
        print(e)


if __name__ == "__main__":

    # data = {
    #     "blBase64": "0",
    #     "printType": "2",
    #     "waybillCodeSet": [111, 222]
    # }
    # value = write_excelData(0, 4, 5, str(data))
    # print(value)


   res_list = get_excelData('揽件接口用例',2,3,1,2)
   print(res_list)



