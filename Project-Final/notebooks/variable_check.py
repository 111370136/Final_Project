import os
import pandas as pd

# 設定資料路徑（根據你的目錄架構，從專案根目錄出發的相對路徑）
data_path = os.path.join("data", "raw", "YRBS_2007 .csv")

try:
    # 讀取 CSV 資料集
    df = pd.read_csv(data_path)
    
    print("=" * 50)
    print(f" 成功讀取資料集！檔案路徑: {data_path}")
    print(f" 資料集維度 (列數, 欄數): {df.shape}")
    print("=" * 50)
    
    # 1. 列出所有變數名稱
    columns_list = df.columns.tolist()
    print(f"\n【此資料集共包含 {len(columns_list)} 個變數】:")
    for i, col in enumerate(columns_list, start=1):
        print(f"  {i:02d}. {col}")
        
    print("\n" + "=" * 50)
    
    # 2. 顯示前 3 筆資料的預覽，方便確認型態
    print("【前 3 筆資料預覽】:")
    print(df.head(3))
    print("=" * 50)

except FileNotFoundError:
    print(f"❌ 錯誤：找不到檔案，請確認你執行的位置是否在專案根目錄，且路徑為: {data_path}")
except Exception as e:
    print(f"❌ 發生其他錯誤: {e}")