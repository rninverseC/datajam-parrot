# DataJam Proposal Revised Draft

**School Name:** Canyon Crest Academy

**Team Number:** #05

**Team Name:** Parrots

**Team Member Names & Personal Email Addresses:**
- Stephen Ye - yeyao.notes@gmail.com
- Jaxon Sawhney - jaxonsawhney@gmail.com
- Nevinh Do - nevinhdo@gmail.com
- Dylan Lam -

### Project Title
Which Business and Financial Occupations Are Most Likely to Be Enhanced by AI?

### Problem
Within business and financial operations occupations, which specific jobs are most likely to be enhanced, rather than replaced, by AI adoption over the next decade?

### Why Is It Important?
Artificial intelligence is changing the workplace quickly, and many students are unsure which careers will benefit from AI and which may become more automated. Instead of studying the entire workforce, this project focuses on business and financial operations, a specific job area with many different roles that range from highly analytical work to more routine, process-based work. Understanding which finance-related occupations are most likely to be enhanced by AI can help students make more informed career choices, help educators think about which skills will matter most, and help employers understand where AI is most likely to support workers rather than replace them.

### Hypothesis
More analytical finance occupations such as financial and investment analysts, personal financial advisors, budget analysts, and accountants or auditors will be more strongly enhanced by AI than more routine or rule-based occupations such as loan officers, claims adjusters, and insurance underwriters. Analytical finance jobs depend more on judgment, interpretation, and decision-making, so AI is more likely to improve worker productivity in those roles rather than fully replace them.

### Data Required
We plan to analyze the following datasets:

- O*NET Database: https://www.onetcenter.org/database.html
- BLS Occupational Employment Projections Data: https://www.bls.gov/emp/data/occupational-data.htm
- BLS Skills Data: https://www.bls.gov/emp/data/skills-data.htm
- BLS Occupational Employment and Wage Statistics: https://www.bls.gov/oes/tables.htm
- AIOE occupation exposure dataset: https://github.com/AIOE-Data/AIOE

These datasets provide occupation-level information related to skills, tasks, wages, employment, projected growth, and AI exposure. We will focus on business and financial operations occupations, especially finance-related jobs such as financial and investment analysts, personal financial advisors, accountants, budget analysts, loan officers, insurance underwriters, and claims adjusters. Some of our data, especially employment projections and AI exposure measures, involve modeled or projected outcomes rather than direct observations of the future, so our conclusions will be presented as evidence about likely trends rather than certain predictions.

### Analysis Plan
We will clean and join the datasets by occupation code, then filter to business and financial operations occupations. Within that area, we will compare several finance-related jobs using variables connected to AI enhancement, including AI exposure, skill complexity, education level, wages, projected employment growth, and job openings. Rather than using a broad label such as finance without definition, we will analyze specific occupations first and then compare them to see which roles appear most likely to benefit from AI.

We also plan to calculate summary statistics, examine correlations between important variables, and build a simple model to estimate how strongly each factor is associated with AI enhancement. One possible outcome variable is an AI enhancement score based on a combination of exposure to AI, high skill requirements, and positive projected labor-market outcomes. Our goal is to rank occupations within this area and identify which finance jobs are most likely to use AI as a productivity tool. When presenting results, we will clearly note that some findings depend on projected or modeled data.

### Visualizations
- Bar chart comparing estimated AI enhancement across finance occupations
- Scatter plot of AI exposure versus projected job growth
- Box plot comparing analytical finance jobs with more routine finance jobs
- Correlation heatmap of the most important variables
- Regression plot showing the strongest relationship in the data
