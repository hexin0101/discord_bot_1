import matplotlib.pyplot as plt
import matplotlib

# 設定中文字體
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用系統上已安裝的字體
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 生成一個圓餅圖示例
def generate_pie_chart(votes, options):
    fig, ax = plt.subplots()
    ax.pie(votes, labels=options, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # 保存圓餅圖到檔案
    chart_filename = 'vote_results.png'
    plt.savefig(chart_filename)
    plt.close()

# 示例數據
options = ['選項一', '選項二', '選項三']
votes = [10, 20, 15]

generate_pie_chart(votes, options)
