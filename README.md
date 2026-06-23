# Project-Final
## Student Information
- Name:詹濬誌
- Student ID:111370136
## Project Repository
https://github.com/111370136/Final_Project.git
## Presentation Video
https://youtu.be/43KnNPmp2II
## Dataset
- Raw data: `YRBS_2007.csv`
- Processed data used across notebooks: `cleaned_school_safety.csv`
## Selected Project Question
- Do students of different grades who feel sad have the same average campus safety score, and what are their demographic characteristics?
## Variables:
- Grade, Sad_Hopeless, Weapon_School, Fight_Total, Fight_School, Injected_Drug, Drug_School
### 1. Demographic & Grouping Variable
- `Grade`:Represents the student's current grade level (9th - 12th). This serves as a core control variable in the Two-Way ANOVA.
- `Sad_Hopeless`: Coding Logic `0` = No (did not feel sad/hopeless), `1` = Yes (felt sad/hopeless).
### 2. Primary Behavioral Variables
- `Weapon_School` (Number of days carrying a weapon on school property):
    Coding Logic: `1` = 0 days, `2` = 1 day, `3` = 2-3 days, `4` = 4-5 days, `5` = 6 or more days.
- `Fight_Total` (Number of times involved in a physical fight over the past 12 months):
    Coding Logic: Frequency-scaled question where `1` = 0 times, and values greater than 1 indicate occurrence.
- `Fight_School` (Number of times involved in a physical fight on school property over the past 12 months):
    Coding Logic: Frequency-scaled question where `1` = 0 times. It specifically captures violent behaviors occurring within the school environment.
### 3. Data Integrity & Logic-Check Variables (Ever Use Experience)
- `Injected_Drug` and `Drug_School`, `Fight_Total` and `Fight_School`:If it was previously shown as not used but recently shown as used in some parts, that data will be removed.
## Key Methodology & Analytical Pipeline
- First, preprocess the data and create a school safety index based on variables like `Weapon_School`, `Fight_Total`, `Fight_School`, `Injected_Drug`, and `Drug_School`. Then, run an ANOVA with `Grade` and `Sad_Hopeless`. After that, identify the common features of the group that has a high school safety risk index.
## Final conclusion
- Compared to older grades, there are more high-risk students in the lower grades, and psychologically, half of the students are   - in the sadness group.
- So, besides controlling weapons and drugs, counseling interventions are also needed to achieve the best results.

