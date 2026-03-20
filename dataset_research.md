# Dataset Research For Finance Focus

## Chosen Area

We are narrowing the project to `Business and Financial Operations Occupations`, which maps to the BLS major occupation group `13-0000`.

This is a good fit because it is:
- specific enough for the instructor's feedback
- broad enough to include many distinct finance-related jobs
- available in official occupation-level datasets that can be joined together

## Best Finance-Related Occupations To Start With

These are good candidate jobs inside the area:
- Accountants and Auditors (`13-2011`)
- Budget Analysts (`13-2031`)
- Credit Analysts (`13-2041`)
- Financial and Investment Analysts (`13-2051`)
- Personal Financial Advisors (`13-2052`)
- Insurance Underwriters (`13-2053`)
- Financial Examiners (`13-2061`)
- Loan Officers (`13-2072`)
- Tax Examiners and Collectors, and Revenue Agents (`13-2081`)
- Claims Adjusters, Examiners, and Investigators (`13-1031`)
- Compliance Officers (`13-1041`)

This gives us a mix of:
- more analytical finance jobs
- more rule-based or process-heavy finance jobs

That is useful for comparing which roles are more likely to be enhanced by AI.

## Recommended Core Datasets

### 1. O*NET 30.2 Database
- Source: O*NET Resource Center
- Link: https://www.onetcenter.org/database.html
- Direct download: https://www.onetcenter.org/dl_files/database/db_30_2_excel.zip
- Why it helps:
  - Gives occupation-level features such as skills, abilities, knowledge, work activities, tasks, job zones, and technology skills.
  - This is the strongest feature source for modeling which finance jobs are likely to benefit from AI.
- How to use it for this project:
  - Filter to occupations in the `13-0000` family, then keep the detailed finance-related occupations we want to study.
- Join key:
  - `O*NET-SOC` occupation code

### 2. BLS Occupational Employment Projections Data
- Source: U.S. Bureau of Labor Statistics
- Link: https://www.bls.gov/emp/data/occupational-data.htm
- Direct download, all occupational tables: https://www.bls.gov/emp/ep_table_102024.xlsx
- Direct download, National Employment Matrix: https://www.bls.gov/emp/ind-occ-matrix/matrix.xlsx
- Why it helps:
  - Adds projected employment, growth, openings, wages, education, and training information for detailed occupations.
  - This gives us the projected labor-market outcome side of the project.
- How to use it for this project:
  - Keep only the `13-xxxx` occupations or the narrower finance-focused subset listed above.
- Join key:
  - `SOC` occupation code

### 3. BLS Skills Data
- Source: U.S. Bureau of Labor Statistics
- Link: https://www.bls.gov/emp/data/skills-data.htm
- Direct download: https://www.bls.gov/emp/skills/public-skills-data.xlsx
- Why it helps:
  - Adds standardized skill measures that are already aligned to the employment projections system.
  - Useful if we want a cleaner ML feature table than the full raw O*NET release.
- Join key:
  - National Employment Matrix occupation code
- Important note:
  - Use the BLS occupational data page crosswalk to connect this file to O*NET-SOC when needed.

### 4. BLS Occupational Employment and Wage Statistics (OEWS), May 2024
- Source: U.S. Bureau of Labor Statistics
- Link: https://www.bls.gov/oes/tables.htm
- Direct download, national table: https://www.bls.gov/oes/special-requests/oesm24nat.zip
- Direct download, all data: https://www.bls.gov/oes/special-requests/oesm24all.zip
- Why it helps:
  - Adds current employment and wage estimates.
  - This gives us present-day labor-market information to compare with projected outcomes.
- How to use it for this project:
  - Filter to the detailed `13-xxxx` occupations we select.
- Join key:
  - `SOC` occupation code

### 5. AIOE Occupation Exposure Dataset
- Source: Felten, Raj, and Seamans AIOE repository
- Link: https://github.com/AIOE-Data/AIOE
- File page: https://github.com/AIOE-Data/AIOE/blob/main/AIOE_DataAppendix.xlsx
- Why it helps:
  - Adds an occupation-level AI exposure score.
  - This is one of the clearest ways to estimate how much each finance occupation overlaps with current AI capabilities.
- How to use it for this project:
  - Join the AI exposure score onto each finance occupation, then compare that score with growth, wages, and skill complexity.
- Join key:
  - `SOC` occupation code

## Supporting Reference Sources

These are helpful for defining scope and interpreting results, even if they are not the main ML table:

### 6. Occupational Outlook Handbook: Business and Financial Occupations
- Source: U.S. Bureau of Labor Statistics
- Link: https://www.bls.gov/ooh/business-and-financial/home.htm
- Why it helps:
  - Gives official occupation descriptions, typical education, pay, and outlook.
  - Useful for choosing which specific finance jobs to include in the final project.

### 7. BLS AI Case Study Article
- Source: Monthly Labor Review, U.S. Bureau of Labor Statistics
- Link: https://www.bls.gov/opub/mlr/2025/article/incorporating-ai-impacts-in-bls-employment-projections.htm
- Why it helps:
  - Shows that BLS is already thinking about how AI may affect occupations.
  - The article specifically includes examples from `Business and Financial Operations`, such as financial and investment analysts and personal financial advisors.

## Best Dataset Stack For This Project

If we want the strongest version of the finance project, the best stack is:

1. O*NET for occupation features
2. AIOE for AI exposure
3. BLS Employment Projections for projected outcomes
4. BLS OEWS for current wages and employment
5. BLS Skills Data if we want a simpler feature table

This stack is stronger than relying only on simulated Kaggle datasets because it combines:
- official U.S. labor data
- occupation-level features
- a published AI exposure measure
- both current and projected job-market information

## How This Fits The Finance Project

This version now matches the narrower scope better:
- We are focusing on one official occupation family instead of the whole economy.
- We can compare specific jobs inside finance instead of broad labels like "business."
- We can help students think about which finance jobs are more likely to use AI as a tool rather than be heavily automated.

## Modeling Direction

One practical target is to build an `ai_enhancement_score` for finance occupations using some combination of:
- higher AI exposure
- higher skill complexity
- higher education or job-zone level
- stronger projected growth or openings
- stronger wages

Then we can:
- rank finance occupations by likely AI enhancement
- compare analytical finance jobs with more routine finance jobs
- build a simple regression or classification model to predict enhancement likelihood

## Recommended First Pass

The cleanest first version of the project would focus on these occupations:
- Financial and Investment Analysts
- Personal Financial Advisors
- Credit Analysts
- Budget Analysts
- Accountants and Auditors
- Insurance Underwriters
- Loan Officers
- Claims Adjusters, Examiners, and Investigators

That is a manageable set with clear differences in analysis, judgment, routine process work, and projected AI usefulness.
