import numpy as np
import pandas as pd


prototypes=np.ones((100, 512))#用长度为512的全1向量分别初始化ART的100个神经元
prototypes=np.around(prototypes, decimals=3)#将数值保留到小数点后3位
print(prototypes)



# 保存prototypes

# 将prototypes转换为DataFrame
df = pd.DataFrame(prototypes)
# 保存为CSV文件，不包含标题行，每行之间没有空行
df.to_csv('prototypes.csv', index=False, header=False)
