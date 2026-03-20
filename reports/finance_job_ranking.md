# Finance AI Job Ranking

This first-pass ranking uses O*NET occupation features plus the Felten-Raj-Seamans AIOE score.
BLS bulk download files were blocked, so wage and growth values were manually copied from official BLS Occupational Outlook Handbook pages for the shortlist where available.

## Ranked Finance Occupations

| Rank | SOC | Occupation | Group | AI Exposure | Enhancement Score | Median Wage 2024 | Growth 2024-34 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | 13-2052 | Personal Financial Advisors | analytical | 1.401 | 0.822 | 102,140 | 10% |
| 2 | 13-2051 | Financial and Investment Analysts | analytical | 1.381 | 0.689 | 101,350 | 6% |
| 3 | 13-2011 | Accountants and Auditors | analytical | 1.482 | 0.499 | 81,680 | 5% |
| 4 | 13-2031 | Budget Analysts | analytical | 1.503 | 0.423 | 87,930 | 1% |
| 5 | 13-2041 | Credit Analysts | analytical | 1.345 | 0.264 | 80,970 | -4% |
| 6 | 13-2072 | Loan Officers | routine | 1.386 | 0.049 | 74,180 | 2% |
| 7 | 13-2053 | Insurance Underwriters | routine | 1.327 | -0.164 | 79,880 | -3% |
| 8 | 13-1031 | Claims Adjusters, Examiners, and Investigators | routine | 1.274 | -0.179 | 76,790 | -5% |
| 9 | 13-2054 | Financial Risk Specialists | analytical |  |  | 106,000 | 7% |

## Notes

- The `ai_enhancement_score` is a heuristic ranking, not a causal estimate.
- Higher scores reflect stronger AI exposure combined with more analytical and higher-complexity signals.
- Occupations missing the AIOE exposure value are left unranked in this first pass.

## Official BLS Source Pages Used For Manual Metrics

- https://www.bls.gov/ooh/business-and-financial/personal-financial-advisors.htm
- https://www.bls.gov/ooh/business-and-financial/financial-analysts.htm
- https://www.bls.gov/ooh/business-and-financial/accountants-and-auditors.htm
- https://www.bls.gov/ooh/business-and-financial/budget-analysts.htm
- https://www.onetonline.org/link/summary/13-2041.00
- https://www.bls.gov/ooh/business-and-financial/loan-officers.htm
- https://www.bls.gov/ooh/business-and-financial/insurance-underwriters.htm
- https://www.bls.gov/ooh/business-and-financial/claims-adjusters-appraisers-examiners-and-investigators.htm
- https://www.onetonline.org/link/localtrends/13-2054.00
