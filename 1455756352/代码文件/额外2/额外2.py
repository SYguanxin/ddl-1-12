import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fileNameStr = 'C:/Users/初心的北宅/Desktop/102204117陈上铭/导出excel/_fzu.xlsx'  # 文件路径,考核测试时请更改
fzuDf = pd.read_excel(fileNameStr, sheet_name='fzu', dtype=str)

# 附件下载次数和通知人关系
subfzuDf = fzuDf.loc[:, ['通知人', '附件下载次数']]
subfzuDf = subfzuDf.dropna(subset=['附件下载次数'], how='any')

# 附件下载次数分割
dataser = []
for value in subfzuDf['附件下载次数']:
    dstr = value.split(';')
    for i in range(len(dstr)):
        dstr[i] = eval(dstr[i])
    dataser.append(dstr)
subfzuDf['附件下载次数'] = dataser
subfzuDf = subfzuDf.sort_values(by='通知人', ascending=True).reset_index(drop=True)
time_sum = {}
time_d = {}
for index, row in subfzuDf.iterrows():
    tsum, d = 0, 0
    for i in row['附件下载次数']:
        tsum += i
        d += 1
    if row['通知人'] not in time_sum.keys():
        time_sum[row['通知人']] = tsum
        time_d[row['通知人']] = d
    else:
        time_sum[row['通知人']] += tsum
        time_d[row['通知人']] += d
for key in time_sum.keys():
    time_sum[key] = time_sum[key]/time_d[key]

print(time_sum)


# 通知时间和通知数关系
atfzuDf = fzuDf.loc[:, ['通知时间']]
dataser = []
for value in atfzuDf['通知时间']:
    dstr = value.split(' ')[0]
    dataser.append(dstr)
atfzuDf['通知时间'] = dataser
atfzuDf['通知时间'] = pd.to_datetime(atfzuDf['通知时间'],
                                     format='%Y-%m-%d',
                                     errors='coerce')
atfzuDf = atfzuDf.sort_values(by='通知时间', ascending=True).reset_index(drop=True)

time_dir = {
    '通知人': time_sum.keys(),
    '附件点击次数': time_sum.values()
}
notice = pd.DataFrame(time_dir,columns=['通知人', '附件点击次数'])

plt.rc("font", family='MicroSoft YaHei', weight="bold")  # 设置字体

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,6))

axes[0].title.set_text('每个部门平均每个附件点击次数')
ax0 = axes[0].bar(x=notice['通知人'], height=notice['附件点击次数'].astype('int'), color='#BC8F8F', alpha=0.5)
axes[0].bar_label(ax0, label_type='edge')

axes[1].title.set_text('每段时间的通知数')
sns.histplot(x='通知时间', data=atfzuDf, kde=True, ax=axes[1])
plt.show()