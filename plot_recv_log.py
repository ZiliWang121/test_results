import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 创建输出文件夹
os.makedirs("plots", exist_ok=True)

# 读取日志文件
df = pd.read_csv("recv_log.csv")

# 文件名预处理（如 8MB.file -> 8MB）
df['File'] = df['File'].str.replace('.file', '', regex=False)
df['File_MB'] = df['File'].str.replace('KB', 'KB').str.replace('MB', 'MB')

# -------------------------------
# 图 1：Application Delay (Boxplot)
# -------------------------------
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='File_MB', y='AvgDelay(ms)', hue='Scheduler')
plt.title("Application Delay by Scheduler and File Size")
plt.ylabel("Application Delay (ms)")
plt.xlabel("File Size")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="Scheduler", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("plots/plot_delay_boxplot.png")
plt.close()

# -------------------------------
# 图 2：Goodput (Grouped Bar)
# -------------------------------
# 计算平均 Goodput
grouped_goodput = df.groupby(['File_MB', 
'Scheduler'])['Goodput(KB/s)'].mean().reset_index()
pivot_goodput = grouped_goodput.pivot(index='File_MB', 
columns='Scheduler', values='Goodput(KB/s)')

# 绘制柱状图
pivot_goodput.plot(kind='bar', figsize=(10, 6))
plt.title("Average Goodput by Scheduler and File Size")
plt.ylabel("Goodput (KB/s)")
plt.xlabel("File Size")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="Scheduler", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("plots/plot_goodput_bar.png")
plt.close()

# -------------------------------
# 图 3：Completion Time (Line per File)
# -------------------------------
grouped_time = df.groupby(['File_MB', 
'Scheduler'])['DownloadTime(s)'].mean().reset_index()
file_sizes = grouped_time['File_MB'].unique()

# 为每种文件大小生成一张折线图
for f in file_sizes:
    plt.figure(figsize=(6, 4))
    subset = grouped_time[grouped_time['File_MB'] == f]
    plt.plot(subset['Scheduler'], subset['DownloadTime(s)'], marker='o', 
color='orange')
    plt.title(f"Completion Time ({f})")
    plt.xlabel("Scheduler")
    plt.ylabel("Completion Time (s)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    # 用干净的文件名防止路径错误
    safe_f = f.replace('/', '_').replace(' ', '_')
    plt.savefig(f"plots/plot_completion_time_{safe_f}.png")
    plt.close()
