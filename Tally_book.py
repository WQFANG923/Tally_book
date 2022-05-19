import json
import datetime
import PySimpleGUI as sg

'''项目开发编写步骤：
1. 建立数据文件
2. 读取数据函数
3. 写入数据函数
4. 编写界面
5. 账单显示函数
6. 总收入计算函数
7. 总支出计算函数
8. 增加账目函数
9. 结合界面调用函数实现项目内容
'''
# 使用git啦

# d ='[{"时间": "2022/05/17 21:41:20", "项目": "收到货款", "金额": 20000, "分类": "收入"}]'
# with open(r'data.txt', 'w') as f:
#     f.write(d)

def readData(): #读取数据
    with open(r'data.txt', 'r') as f:
        jsonData = f.read()
        dataList = json.loads(jsonData)
        return dataList

def writeData(dataList): #写入数据
    jsonData = json.dumps(dataList, ensure_ascii=False)
    with open(r'data.txt', 'w') as f:
        jsonData = f.write(jsonData)
        sg.popup('账单录入成功')

def showData(): #展示数据
    data = readData()
    dataLists = []
    for d in data:
        if d["分类"] == "收入":
            dataList = [d["时间"], d["项目"], d["金额"], d["分类"]]
            dataLists.append(dataList)
        else:
            dataList = [d["时间"], d["项目"], -1*d["金额"], d["分类"]]
            dataLists.append(dataList)
    return dataLists

def sumin(): #总收入计算
    sumin = 0
    data = readData()
    for d in data:
        if d["分类"] == "收入":
            sumin += d["金额"]
    return sumin

def sumout(): #总支出计算
    sumout = 0
    data = readData()
    for d in data:
        if d["分类"] == "支出":
            sumout += d["金额"]
    return sumout

def addData(content, amount, cla): #增加账目数据
    dataLists = readData()
    t= datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    data = {"时间": t, "项目": content, "金额": amount, "分类": cla}
    dataLists.append(data)
    writeData(dataLists)


def main():
    list=showData()
    layout=[
        [sg.T("账目清单： ")],
        [sg.Table(list, headings=["时间", "项目", "金额", "分类"],
                  key = "-show-",
                  justification = "c",
                  auto_size_columns = False,
                  def_col_width = 15
                  )],
        [sg.T("总收入{}元， 总支出{}元，结余{}元".format(str(sumin()), str(sumout()), str(sumin()-sumout())), key="-text-")],
        [sg.T("请输入账单项目："), sg.In(key="-content-")],
        [sg.T("请输入账单金额："), sg.In(key="-amount-")],
        [sg.T("请输入账单分类：")]+[sg.Radio(i, group_id=1, key=i) for i in ["收入", "支出"]],
        [sg.B("确认提交")]
    ]

    window = sg.Window("记账本", layout)
    while True:
        event, values = window.read()
        if event == "确认提交":
            content = values["-content-"]
            amount = float(values["-amount-"])
            for k, v in values.items():
                if v == True:
                    cla = k
                    addData(content, amount, cla)
                    list = showData()
                    text = "总收入{}元， 总支出{}元，结余{}元".format(str(sumin()), str(sumout()), str(sumin()-sumout()))
                    window["-show-"].update(values=list)
                    window["-text-"].update(value=text)
                    window["-content-"].update("")
                    window["-amount-"].update("")

        if event == None:
            break
    window.close()

main()
