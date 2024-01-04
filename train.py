import pandas as pd
from sklearn.linear_model import LinearRegression

# 读取CSV文件
file_path = 'dz.csv'
earthquake_data = pd.read_csv(file_path)

# 选择特征
features = ['经度', '纬度', '震级']

# 提取特征和目标变量
X = earthquake_data[features]
y = earthquake_data['震级']

# 初始化线性回归模型
linear_reg_model = LinearRegression()

# 训练模型
linear_reg_model.fit(X, y)

# 从CSV文件中提取一行作为新的预测数据
new_data = X.iloc[0:1]  # 假设选择第一行作为新数据点，你可以根据需要调整
# 输出训练得到的模型参数
print("模型参数:")
print("斜率（系数）:", linear_reg_model.coef_)
print("截距:", linear_reg_model.intercept_)
# 使用训练好的模型进行预测
predicted_value = linear_reg_model.predict(new_data)

# 输出预测的震级
print("\n预测下一场地震的震级:")
print(f"预测震级: {predicted_value[0]}")


def main():
    return None