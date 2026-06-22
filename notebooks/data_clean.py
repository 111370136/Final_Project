import os
import numpy as np
import pandas as pd

# 1. 設定資料路徑
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
if os.path.basename(current_dir) == "notebooks":
    base_dir = os.path.dirname(current_dir)
else:
    base_dir = current_dir

data_path = os.path.join(base_dir, "data", "raw", "YRBS_2007 .csv")

try:
    # 讀取原始資料
    df = pd.read_csv(data_path)
    print(f"原始資料總筆數: {len(df)} 筆")

    # 檢查資料集是用全名還是原始代號
    full_names = ['InWhatGradeAreYou', 'WeaponCarryingAtSchool', 'PhysicalFighting', 
                  'PhysicalFightingAtSchool', 'SadOrHopeless', 'IllegalInjectedDrugUse', 'IllegalDrugsAtSchool']
    
    if all(col in df.columns for col in full_names):
        df_sub = df[full_names].copy()
        df_sub.columns = ['Grade', 'Weapon_School', 'Fight_Total', 'Fight_School', 'Sad_Hopeless', 'Injected_Drug', 'Drug_School']
    else:
        target_columns = {
            'Q4': 'Grade',
            'Q14': 'Weapon_School',
            'Q18': 'Fight_Total',
            'Q20': 'Fight_School',
            'Q23': 'Sad_Hopeless',
            'Q56': 'Injected_Drug',
            'Q57': 'Drug_School'
        }
        df_sub = df[list(target_columns.keys())].copy()
        df_sub.rename(columns=target_columns, inplace=True)

    print("=" * 60)
    print("【步驟一：處理遺失值 (Missing Values)】")
    df_clean = df_sub.dropna().copy()
    print(f"刪除缺失值後剩餘資料: {len(df_clean)} 筆")

    print("=" * 60)
    print("【步驟二：年級篩選 (Grade Recoding)】")
    df_clean = df_clean[df_clean['Grade'].isin([1, 2, 3, 4])].copy()
    print(f"保留 9~12 年級後剩餘資料: {len(df_clean)} 筆")

    print("=" * 60)
    print("【步驟三：打架行為矛盾分析 (Logical Consistency Edits)】")
    # 矛盾：總打架次數為 0次(選項1)，但在校打架 > 0次(選項 > 1)
    contradiction_condition = (df_clean['Fight_Total'] == 1) & (df_clean['Fight_School'] > 1)
    df_clean = df_clean[~contradiction_condition].copy()
    print(f"排除矛盾資料後剩餘: {len(df_clean)} 筆")

    print("=" * 60)
    print("【步驟四：自訂分數映射與校園安全風險指數計算】")
    df_clean['Sad_Hopeless'] = df_clean['Sad_Hopeless'].map({1: 1, 2: 0})
    # --- 定義你給予的自訂分數映射表 (選項: 分數) ---
    weapon_map = {1: 0, 2: 50, 3: 70, 4: 90, 5: 100}
    fight_map = {1: 0, 2: 20, 3: 30, 4: 50, 5: 70, 6: 80, 7: 90, 8: 100}
    injected_map = {1: 0, 2: 50, 3: 100}
    drug_school_map = {1: 100, 2: 0} # 1=Yes(100分), 2=No(0分)

    # 將原始選項轉換為 0~100 的基礎得分
    weapon_base = df_clean['Weapon_School'].map(weapon_map)
    fight_total_base = df_clean['Fight_Total'].map(fight_map)
    fight_school_base = df_clean['Fight_School'].map(fight_map)
    injected_base = df_clean['Injected_Drug'].map(injected_map)
    drug_school_base = df_clean['Drug_School'].map(drug_school_map)

    # 乘以各自的權重比例 (基礎得分 * 權重百分比)
    base_score = (
        weapon_base * 0.30 +
        fight_total_base * 0.10 +
        fight_school_base * 0.15 +
        injected_base * 0.20 +
        drug_school_base * 0.25
    )
    
    # 攜帶武器另外額外懲罰分數：只要不是選項 1 (有攜帶武器天數 > 0)，直接額外外加 30 分
    penalty_score = df_clean['Weapon_School'].apply(lambda x: 30 if x > 1 else 0)
    # 最終加總總分
    df_clean['Safety_Score'] = base_score + penalty_score
    

    print("=" * 60)
    print("【步驟五：風險等級分級 (Risk Grouping)】")
    # 0–30：低風險 | 31–60：中風險 | 61–100 以上：高風險
    def assign_risk_label(score):
        if score <= 30:
            return 'Low'
        elif score <= 60:
            return 'Medium'
        else:
            return 'High'

    df_clean['Risk_Level'] = df_clean['Safety_Score'].apply(assign_risk_label)

    print("\n【資料清洗與自訂權重映射完成！】")
    print(f"最終有效可用資料筆數: {len(df_clean)} 筆")
    
    print("\n【前 5 筆資料預覽】:")
    print(df_clean[['Grade', 'Sad_Hopeless', 'Safety_Score', 'Risk_Level']].head())
    
    print("\n【各風險等級學生人數統計】:")
    print(df_clean['Risk_Level'].value_counts())

    # 6. 匯出乾淨資料
    output_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cleaned_school_safety.csv")
    df_clean.to_csv(output_path, index=False)
    print(f"\n✅ 乾淨的資料已成功匯出至: {output_path}")

except Exception as e:
    print(f"❌ 執行過程中發生錯誤: {e}")