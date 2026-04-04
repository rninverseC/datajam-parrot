# Two-Sample t-Test Plan For Our Project

## Topic

We want to study which business and financial occupations may be more advantageous in the future as AI adoption increases.

For the formal statistical test, we will compare two occupation groups:
- `judgment-intensive`
- `process-driven`

## State

We will use a `two-sample t-test for a difference in means`.

Let:
- `mu_1` = the true mean projected job growth percentage for `judgment-intensive` business and financial occupations
- `mu_2` = the true mean projected job growth percentage for `process-driven` business and financial occupations

### Hypotheses

Directional version:
- `H0: mu_1 - mu_2 = 0`
- `Ha: mu_1 - mu_2 > 0`

This means:
- null hypothesis: there is no difference in mean projected growth
- alternative hypothesis: judgment-intensive occupations have higher mean projected growth

If a non-directional test is required instead:
- `H0: mu_1 - mu_2 = 0`
- `Ha: mu_1 - mu_2 != 0`

## Plan

We will perform a `two-sample t-test for a difference in means`.

### Variables

- Group 1: `judgment-intensive` occupations
- Group 2: `process-driven` occupations
- Quantitative response variable: `projected job growth %`

This test fits because:
- we are comparing `two independent groups`
- the variable being compared is `quantitative`
- we want to test whether the `mean` projected growth differs between the groups

## Conditions To Check

### 1. Independent Groups

This condition is met if:
- each occupation is placed in only one group
- the occupations are not paired or repeated

In our project:
- each occupation will be labeled either `judgment-intensive` or `process-driven`, not both

### 2. 10% Condition

For a t-test, each sample should be less than 10% of the population it comes from.

In our project:
- we are using occupations, not individual people
- this condition is not as clean as in a standard random sample setting
- it is more defensible if we use a broader set of business and financial occupations instead of only a tiny hand-picked subset

### 3. Normal / Nearly Normal Condition

We check one of the following:
- the population is approximately normal, or
- each sample size is at least 30, or
- the sample distributions show no extreme outliers and no strong skewness

In our project:
- if each group has fewer than 30 occupations, we should examine boxplots or histograms
- if there are no major outliers and no strong skewness, the condition is more reasonable

## Important Note

The `machine learning` part does **not** prove the t-test conditions.

The t-test conditions are checked using:
- study design
- how the occupations are grouped
- graphs such as boxplots or histograms
- sample size and outlier/skewness checks

The ML part is separate:
- ML helps with the predictive side of the project
- the t-test helps with the formal hypothesis-testing side

## Recommended Test Setup

- Test: `two-sample t-test`
- Response variable: `projected job growth %`
- Group variable: `judgment-intensive` vs `process-driven`

## Conclusion Template

Since the p-value is `above/below` the significance level `alpha`, we `fail to reject/reject` `H0`.

There is `not convincing/convincing` evidence that the mean projected job growth for judgment-intensive business and financial occupations is `different from / greater than` the mean projected job growth for process-driven occupations.

