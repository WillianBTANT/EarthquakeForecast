import tkinter as tk
from tkinter import ttk
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point

# 读取csv文件。
df = pd.read_csv('dz.csv')
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values(by='日期')

# 数据框（DataFrame）是df
# 首先，将 '时间' 列转换为日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')
# 按照日期进行排序
df_sorted = df.sort_values(by='日期')
# 创建一个颜色映射，可以根据需要选择不同的颜色映射
cmap = plt.get_cmap('viridis')
colors = cmap(1 - df_sorted['震级'] / df_sorted['震级'].max())
# 绘制散点图
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df_sorted['日期'], df_sorted['震级'], c=df_sorted['震级'], cmap='viridis', marker='o')
plt.title('Earthquake Magnitude Over Time (Sorted by Date)')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.colorbar(label='Data Point Index')
plt.grid(True)
plt.show()

# 统计每个城市的地震次数
city_counts = df['地点'].value_counts().reset_index()
city_counts.columns = ['城市', '地震次数']

# 绘制柱状图
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示
plt.figure(figsize=(50, 5))
plt.bar(city_counts['城市'], city_counts['地震次数'], color='skyblue')
most_affected_city = city_counts.iloc[0]['城市']
most_affected_count = city_counts.iloc[0]['地震次数']
plt.annotate(f'{most_affected_city}\n地震次数: {most_affected_count}',
             xy=(1, 1), xycoords='axes fraction',
             xytext=(-10, -10), textcoords='offset points',
             ha='right', va='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.xlabel('城市')
plt.ylabel('地震次数')
plt.title('每个城市的地震次数统计')
plt.xticks(rotation=90, fontsize=9)  # 调整刻度标签的字体大小为8
plt.tight_layout()
# plt.savefig('earthquake_city_counts.pdf', format='pdf')
plt.show()

# # 根据经纬度将地震数据与大陆板块合并
# gdf_earthquakes = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['经度'], df['纬度']))
# merged_data = gpd.sjoin(gdf_earthquakes, plates, how='left', op='within')
#
# # 绘制countplot
# plt.figure(figsize=(12, 8))
# sns.countplot(x='continent', data=merged_data, palette='viridis')
# plt.title('各大陆板块中的地震频次统计')
# plt.xlabel('大陆板块')
# plt.ylabel('地震频次')
# plt.show()

# 创建带有点几何的 GeoDataFrame
geometry = [Point(xy) for xy in zip(df['经度'], df['纬度'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)
# 读取世界地图数据
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# 根据地震级别定义标记颜色
def get_marker_color(magnitude):
    if magnitude >= 6:
        return 'red'
    elif 4 <= magnitude < 6:
        return 'orange'
    else:
        if 3.1 <= magnitude < 4:
            return 'yellow'
        else:
            return 'grey'
            # 根据需要调整其他震级的颜色


# 绘制世界地图和不同颜色的地震标记
fig, ax = plt.subplots(figsize=(10, 6))
world.plot(ax=ax, color='lightgray')
# 根据 '地震级别' 列应用标记颜色
gdf['marker_color'] = gdf['震级'].apply(get_marker_color)
gdf.plot(ax=ax, marker='o', color=gdf['marker_color'], markersize=10)
plt.show()

# 处理城市数据和风险评估
root = tk.Tk()
root.title("城市地震风险评估")
weight_magnitude = 0.4
weight_depth = 0.3
weight_longitude = 0.1  # 经度权重
weight_latitude = 0.1  # 纬度权重

# 计算聚合的城市数据
city_data = df.groupby('地点').agg({
    '经度': 'mean',  # 每个城市的平均经度
    '纬度': 'mean',  # 每个城市的平均纬度
    '深度': 'mean',  # 每个城市的平均深度
    '震级': 'max',  # 每个城市的最大震级
    '时间': 'count'  # 发生时间
}).reset_index()


def calculate_risk(city_name):
    city_subset = city_data[city_data['地点'] == city_name]

    if not city_subset.empty:
        risk_score = (
                weight_magnitude * city_subset['震级'].values[0] +
                weight_depth * city_subset['深度'].values[0] +
                weight_longitude * city_subset['经度'].values[0] +
                weight_latitude * city_subset['纬度'].values[0]
        )
        return risk_score
    else:
        return 0  # 或者其他默认值


# 点击按钮时评估风险的函数
def evaluate_risk():
    selected_city = city_var.get()

    try:
        risk_score = calculate_risk(selected_city)
        result_label.config(text=f"{selected_city}的地震风险评分为: {risk_score:.2f}")
    except Exception as e:
        result_label.config(text=f"发生错误: {str(e)}")


# 桌面程序
city_var = tk.StringVar()
city_dropdown = ttk.Combobox(root, textvariable=city_var)
city_dropdown['values'] = tuple(city_data['地点'])
city_dropdown.grid(row=0, column=0, padx=10, pady=10)

evaluate_button = tk.Button(root, text="评估风险", command=evaluate_risk)
evaluate_button.grid(row=0, column=1, padx=10, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()


def main():
    return None
