import pandas as pd

data = pd.read_csv("../../Data/soybean.csv")
cols = data.columns
new_df_dict = {}

final_list = []
for col in cols:
    col_vals = data[col]
    new_col_vals = []
    for i in range(len(col_vals)):
        new_col_vals.append(col_vals[i].strip())
    
    final_list.append(new_col_vals)

for i in range(len(cols)):
    col_name = cols[i]
    if col_name not in new_df_dict:
        new_df_dict[col_name] = final_list[i]

new_df = pd.DataFrame(new_df_dict)
print(new_df)
new_df.to_csv("../../Data/soybean_new.csv", index=False)