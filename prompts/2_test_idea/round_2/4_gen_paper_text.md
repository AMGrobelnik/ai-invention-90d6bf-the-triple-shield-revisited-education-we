# gen_paper_text — test_idea

> Phase: `invention_loop` · round 2 · `gen_paper_text`
> Run: `run_9gq-UFm593U6` — The Triple Shield Revisited: Education, Welfare State Institutions, and the Inequality-Democratic Resilience Link in Post-1990 Democratizers
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-06-22 13:12:33 UTC

````
<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

# The Triple Shield: How Education and Welfare State Institutions Jointly Buffer the Inequality-Democratic Backsliding Link in Post-1990 Democratizers

## Introduction

The relationship between income inequality and democratic backsliding has emerged as a central concern in comparative political economy. Recent work by Rau and Stokes (2024) provides robust evidence that income inequality is a strong predictor of democratic erosion across advanced democracies and democratizers [1]. Yet, as Carothers and Hartnett (2024) note, the inequality-backsliding link is far from deterministic: many high-inequality democracies have not backslid, while some relatively equal societies have [2]. What accounts for this variation?

This paper tests a specific institutional explanation: that the inequality-democratic backsliding link is conditioned by a two-level protective mechanism rooted in Acemoglu and Robinson's (2006) distinction between de facto and de jure political power [3]. The central hypothesis—which I call the 'Triple Shield' hypothesis—is that:

1. **Education** increases citizens' de facto political capacity to resist elite capture by enhancing cognitive skills, organizational capacity, and norm internalization about democratic accountability.
2. **Welfare state institutions** impose de jure constraints on executive predation by creating institutionalized expectations, resource dependencies, and veto players that raise the costs of backsliding.
3. **The protective effect is joint**: the inequality-democracy relationship becomes non-significant only when both education levels AND welfare state spending are above median, but remains negative and significant when either or both are below median.

[FIGURE:fig1]

The Triple Shield hypothesis makes three contributions to the literature on inequality and democratic backsliding. First, it provides a nuanced, interaction-based account that matches Acemoglu's de jure/de facto power framework [3], moving beyond simple main-effect models of inequality and backsliding [1]. Second, it has direct policy implications: democratizers may need BOTH human capital development AND social protection to withstand inequality pressures. Third, it speaks to contemporary debates about why some post-1990 democratizers (e.g., Poland, Czechia) succeeded while others (e.g., Hungary, Turkey) backslid.

This paper reports a confirmatory test of the Triple Shield hypothesis using panel data from 50 post-1990 democratizers spanning 1990–2022. The analysis uses fixed-effects regression with triple interaction terms, following the methodological guidance of Brambor, Clark, and Golder (2006) for interpreting interaction effects in political science [7].

**Summary of Findings.** The key result is that the triple interaction term is positive as hypothesized (beta = 0.007, SE = 0.005, p = 0.18) but does not reach conventional significance thresholds (p < 0.05). The 95% confidence interval for the triple interaction is [–0.003, 0.017], which includes zero. Under a strict null hypothesis significance testing framework, the hypothesis is not confirmed. However, the point estimate is substantively meaningful in standardized units: a one-standard-deviation increase in the triple interaction term is associated with a 0.007-standard-deviation increase in democratic quality, holding other factors constant. I discuss the implications of these findings for future research on inequality and democratic resilience.

## Theoretical Framework

### De Facto and De Jure Political Power

Acemoglu and Robinson (2006) distinguish between de jure political power (allocated by institutions) and de facto political power (emerging from collective action capacity) [3]. In their framework, elites can offset losses in de jure power by investing in de facto power (e.g., through coercion or co-optation), leading to institutional persistence even when formal institutions are not inclusive.

The Triple Shield hypothesis applies this framework to the inequality-democratic backsliding link. Income inequality increases the political influence of economic elites, who may use their resources to capture the democratic process [1]. However, two institutional factors can offset this elite capture:

1. **Education as de facto power**: Education enhances citizens' ability to organize, monitor elites, and demand accountability. Research consistently shows that education increases political participation, with effects strongest when democracy is threatened [4, 10]. In the language of Acemoglu and Robinson, education increases citizens' de facto political capacity to resist elite predation.
2. **Welfare state institutions as de jure constraints**: Welfare state institutions impose formal constraints on executive authority by creating institutionalized expectations (citizens demand social protection), resource dependencies (governments require revenue that is conditional on tax compliance), and veto players (welfare bureaucracies, beneficiary organizations) [5, 6]. Orenstein (2008) shows that post-communist democracies with stronger welfare states maintained better social protection, while autocracies and defective democracies scored lower on welfare effort [5].

### The Triple Interaction

The key theoretical claim is that the protective effects of education and welfare spending are **joint**, not additive. When citizens have high de facto power (education) but weak de jure constraints (low welfare spending), elites can still capture the democratic process through institutional maneuvering. Conversely, when de jure constraints are strong (high welfare spending) but citizens lack de facto power (low education), elites may co-opt or bypass institutional constraints. Only when BOTH conditions are present does the inequality-democracy link become non-significant.

Formally, let Y_it denote democratic quality in country i at time t, G_it denote income inequality (Gini coefficient), E_it denote education (mean years of schooling), and W_it denote welfare state spending (% GDP). The triple interaction model is:

Y_it = beta_0 + beta_1 G_it + beta_2 E_it + beta_3 W_it + beta_4 (G_it * E_it) + beta_5 (G_it * W_it) + beta_6 (E_it * W_it) + beta_7 (G_it * E_it * W_it) + beta_8 Z_it + alpha_i + gamma_t + epsilon_it

where Z_it is a vector of controls (GDP per capita, natural resource rents, population), alpha_i are country fixed effects, gamma_t are year fixed effects, and epsilon_it is the error term.

The Triple Shield hypothesis predicts beta_7 > 0: the negative effect of inequality on democratic quality is weakened (the coefficient on inequality becomes less negative) when both education and welfare spending are high.

## Data and Methods

### Sample

The sample includes all countries that transitioned to electoral democracy between 1990 and 1999 and remained sovereign through 2022. The list of post-1990 democratizers was constructed using V-Dem electoral democracy index thresholds (electoral democracy index >= 0.5 in at least one year during 1990–1999, and not above 0.5 prior to 1990). This yielded 50 countries with a combined 1,641 country-year observations spanning 1990–2022 [ARTIFACT:art_0hVluVdTtxOI].

Countries in the sample include post-communist states (e.g., Poland, Hungary, Czech Republic), Latin American cases completing transitions (e.g., Brazil, Argentina), and sub-Saharan African democratizers in the 1990s (e.g., Ghana, South Africa).

[FIGURE:fig2]

### Variables

**Outcome**: V-Dem Electoral Democracy Index (v2x_egaldem), a continuous index (0–1) measuring the extent to which political leaders are elected under comprehensive suffrage in free and fair elections with freedom of expression and association [12]. The index is constructed via a Bayesian measurement model aggregating five indicators: electoral process, suffrage, clean elections, registration, and freedom of expression.

**Inequality**: Gini coefficient from the World Bank Poverty and Inequality Platform (PIP) via Our World in Data [13]. The Gini coefficient ranges from 0 (perfect equality) to 1 (perfect inequality).

**Education**: Mean years of schooling (aged 15+) from the Barro-Lee dataset via Our World in Data [13]. This variable captures the average number of years of formal education completed by the adult population.

**Welfare state spending**: Social protection spending (% of GDP) from the OECD Social Expenditure Database (SOCX) via Our World in Data [13]. This variable captures total public social spending on old age, survivors, incapacity, health, family, active labor market policies, unemployment, housing, and other social policy areas.

**Controls**: GDP per capita (constant 2015 US$), natural resource rents (% of GDP), and population (log-transformed), all from World Bank Development Indicators via Our World in Data.

### Descriptive Statistics

Table 1 reports descriptive statistics for the analysis sample (complete cases on all key variables, N = 391 country-year observations from 34 countries).

[FIGURE:fig3]

The mean V-Dem electoral democracy index in the analysis sample is 0.62 (SD = 0.22), reflecting that the sample includes both stable democracies and cases of backsliding. The mean Gini coefficient is 2.84 (this is the Gini/100, SD = 8.82), the mean years of schooling is 7.57 (SD = 1.67), and mean social protection spending is 9.63% of GDP (SD = 7.22).

Correlations among the key variables show that social protection spending has the strongest bivariate correlation with democratic quality (r = 0.69), followed by education (r = 0.23) and inequality (r = 0.18).

### Missing Data

Missing data is a significant challenge. The full dataset (N = 1,641) has 54% missing on Gini, 34% missing on education, and 52% missing on social spending. The analysis sample (N = 391) represents complete cases on all four key variables. To address potential selection bias from listwise deletion, I report robustness checks using multiple imputation in the Appendix.

### Estimation Strategy

The main specification is a fixed-effects panel regression with clustered standard errors (clustering by country to account for serial correlation). All continuous variables are standardized (mean = 0, SD = 1) to facilitate interpretation of interaction effects [7].

Following Brambor, Clark, and Golder (2006), I include all lower-order terms when specifying the triple interaction [7]. I also report marginal effects at different values of the moderating variables to interpret the substantive magnitude of the triple interaction.

## Results

### Main Results

Table 2 reports the fixed-effects regression results for three nested models.

[FIGURE:fig4]

**Model 1** includes only main effects. The coefficient on inequality (Gini, standardized) is positive but not statistically significant (beta = 0.006, SE = 0.007, p = 0.39). This null finding for the main effect of inequality is consistent with Carothers and Hartnett's (2024) argument that inequality is not a deterministic predictor of backsliding [2].

**Model 2** adds two-way interactions between inequality and education, inequality and welfare spending, and education and welfare spending. None of the two-way interactions are statistically significant at p < 0.05, though the inequality-education interaction is marginally significant (beta = 0.006, SE = 0.005, p = 0.20).

**Model 3** adds the triple interaction term. The triple interaction is positive as hypothesized (beta = 0.007, SE = 0.005, p = 0.18). The 95% confidence interval is [–0.003, 0.017]. Under a two-tailed test at alpha = 0.05, the null hypothesis that the triple interaction equals zero cannot be rejected.

### Marginal Effects Analysis

To interpret the substantive magnitude of the triple interaction, I follow the recommendation of Brambor et al. (2006) and compute marginal effects of inequality on democratic quality at different values of education and welfare spending [7].

Figure 3 displays the marginal effect of inequality (Gini) on democratic quality (V-Dem index) across the range of education and welfare spending values. When both education and welfare spending are one standard deviation below their means, the marginal effect of inequality is negative (beta = –0.020, SE = 0.012, p = 0.10). When both are one standard deviation above their means, the marginal effect is positive but not significant (beta = 0.008, SE = 0.010, p = 0.42). The difference between these two marginal effects is the triple interaction, which is positive as hypothesized but does not reach statistical significance.

### Robustness Checks

I report four robustness checks:

1. **Alternative inequality measure**: Using the P90/P10 income ratio (available for a subset of countries) yields similar point estimates but with larger standard errors due to reduced sample size.
2. **Alternative outcome**: Using the V-Dem liberal democracy index (which adds constraints on executive authority, freedom of expression, and freedom of association) as the outcome variable yields a larger triple interaction coefficient (beta = 0.012, SE = 0.008, p = 0.14), though still not significant at p < 0.05.
3. **Lagged dependent variable model**: Including a one-year lag of the V-Dem index reduces the triple interaction coefficient by approximately 30% and increases the p-value to 0.35, suggesting that persistence in democratic quality may attenuate the interaction effect.
4. **Multiple imputation**: Using chained equations to impute missing values on Gini, education, and social spending increases the analysis sample to N = 1,203 observations. The triple interaction coefficient in the imputed sample is beta = 0.004 (SE = 0.004, p = 0.31).

## Discussion

### Interpreting the Null Result

The key finding of this paper is that the triple interaction between inequality, education, and welfare spending is positive as hypothesized but does not reach conventional significance thresholds. There are several possible interpretations:

1. **Type II error**: The sample size for the triple interaction analysis (N = 391) may be underpowered. As noted by power analysis guidelines for three-way interactions, detecting a triple interaction requires approximately 8 times the sample size of a main effect for equivalent power [14]. With 391 observations and 34 entities, the analysis may simply lack the statistical power to detect a real but small effect.
2. **Measurement error**: The key variables—Gini coefficient, mean years of schooling, and social protection spending—all have substantial measurement error, particularly for developing countries in the 1990s and 2000s. Attenuation bias from measurement error would bias the interaction estimates toward zero.
3. **The hypothesis is wrong**: It is possible that education and welfare spending do not interact to buffer the inequality-democracy link. The theoretical mechanism may be misspecified. For example, education may increase de facto political capacity only under certain conditions (e.g., when the media is free), and welfare spending may create de jure constraints only when certain institutional conditions are met (e.g., when the rule of law is established).

### Comparison with Prior Literature

The null result for the triple interaction stands in tension with two strands of prior literature. First, Rau and Stokes (2024) find a robust main effect of inequality on democratic erosion [1]. The current analysis does not find a significant main effect of inequality, which may reflect differences in sample composition (post-1990 democratizers vs. all democracies), time period (1990–2022 vs. 1995–2020), or model specification (panel FE vs. discrete-time survival analysis).

Second, the education-welfare interaction mechanism finds some support in the case study literature. Orenstein (2008) shows that post-communist democracies with stronger welfare states maintained better democratic quality [5], and Haggard and Kaufman (2021) argue that welfare provision creates democratic resilience by meeting fundamental needs [6]. The current analysis cannot rule out the possibility that education and welfare spending matter for democratic resilience through channels not captured by the triple interaction specification.

### Limitations

This paper has several limitations that should be acknowledged:

1. **Missing data**: The analysis sample (N = 391) is a small fraction of the full dataset (N = 1,641) due to listwise deletion of missing data. While multiple imputation partially addresses this, the extent of missing data—particularly on the Gini coefficient—remains a concern.
2. **Sample size**: The sample of post-1990 democratizers (50 countries) is necessarily limited, which constrains statistical power for detecting triple interactions.
3. **Endogeneity**: The regression specification includes country and year fixed effects, which absorb time-invariant confounders and common time trends. However, time-varying confounders (e.g., economic crises, external shocks) may still bias the estimates.
4. **External validity**: The findings apply to post-1990 democratizers and may not generalize to other groups of countries (e.g., advanced industrial democracies, authoritarian regimes).

## Conclusion

This paper presented a confirmatory test of the Triple Shield hypothesis: that education and welfare state institutions interact to buffer the inequality-democratic backsliding link in post-1990 democratizers. Using fixed-effects panel regression with triple interaction terms, I found that the triple interaction is positive as hypothesized but does not reach statistical significance at conventional thresholds (p < 0.05).

These findings should be interpreted in light of the methodological challenges of testing triple interactions in panel data with limited sample sizes. The point estimate is consistent with the hypothesized buffering effect, but the confidence interval includes zero. Future research with larger samples, better measurement, and alternative identification strategies is needed to provide a definitive test of the Triple Shield hypothesis.

More broadly, this paper contributes to the literature on inequality and democratic backsliding by specifying and testing a conditional hypothesis that moves beyond simple main-effect models. The theoretical framework—rooted in Acemoglu and Robinson's de facto/de jure power distinction—provides a foundation for future research on the institutional conditions under which inequality threatens (or does not threaten) democratic quality.

</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

- [MAJOR] (rigor) CRITICAL DATA ERROR: The Gini coefficient variable in the dataset has a mean of 2.84 and standard deviation of 8.82. This is not consistent with valid Gini coefficient scaling. The Gini coefficient should range from 0-1 (0-100%) with typical values between 0.25-0.65 (25-65%). The actual values in analysis_sample.json range from 0.207 to 46.3. A Gini of 46.3 is impossible (max is 1.0 or 100%). This suggests the Gini variable was incorrectly transformed during data construction (possibly multiplied by 10 or another factor). This error would invalidate ALL regression results in the paper. The paper's description ('this is the Gini/100') is also incorrect - if Gini/100, mean should be ~0.28, not 2.84.
  Action: Immediately check the data generation code (download_owid_csv.py, merge_datasets.py, etc.) to see how the Gini variable was processed. The Gini values in the dataset are incorrect and must be fixed before any results can be trusted. Re-download the Gini data from OWID/World Bank PIP, verify the values are on the correct scale (0-1 or 0-100), and re-run all regressions. This is a critical blocking issue that must be resolved before the paper can proceed.
- [MAJOR] (evidence) The analysis sample (N=391) represents only 24% of the full dataset (N=1,641) due to listwise deletion of missing data. This creates severe selection bias concerns. The paper acknowledges this issue but only reports multiple imputation as a robustness check (which also yields null results, p=0.31). The 76% missing data rate on the triple interaction variable suggests that the analysis is severely underpowered and potentially biased. Countries with missing data are likely poorer countries with weaker statistical systems.
  Action: Make multiple imputation the primary analysis method rather than a robustness check. Use chained equations (MICE) with 50+ imputations and report fraction of information (FI) for each coefficient. Alternatively, use the SWIID (Standardized World Income Inequality Database) which provides imputed Gini coefficients for most countries and years. If the imputed results consistently show null effects, this should be the main finding, not buried in a robustness section.
- [MAJOR] (methodology) The R-squared for Model 3 is only 0.035, meaning the model explains only 3.5% of the variation in democratic quality. This is extremely low for a panel fixed-effects model, suggesting that the key variables (inequality, education, welfare spending) explain very little variation in democratic backsliding. The country and year fixed effects may be absorbing most of the explainable variation, leaving little for the substantive variables of interest. Alternatively, the low R-squared may reflect model misspecification.
  Action: Consider alternative model specifications: (1) Use first differences instead of fixed effects; (2) Use a binary erosion measure with logit fixed-effects or discrete-time survival analysis (as in Rau & Stokes 2024); (3) Include additional control variables that may explain more variation (e.g., polarization, ethnic fractionalization, trade openness).
- [MAJOR] (evidence) The triple interaction coefficient (beta=0.007, p=0.18) does not reach statistical significance at conventional levels. The 95% CI [-0.003, 0.017] includes zero. The paper acknowledges this but frames it as a 'null result' that may be due to Type II error. However, even if the Gini error is fixed, the current analysis is underpowered for a triple interaction with N=391 and 34 entities.
  Action: After fixing the Gini error, re-run the analysis with a larger sample (less missing data) or alternative model specification. If the triple interaction remains null, consider framing this as a valuable null result that contradicts theoretical priors. Alternatively, explore heterogeneity in sub-samples.
- [MINOR] (scope) The sample is limited to post-1990 democratizers, which excludes advanced industrial democracies and authoritarian regimes. The external validity of the findings is therefore limited. Additionally, the sample of 50 countries is small for a triple interaction analysis.
  Action: Acknowledge the scope limitation more explicitly. Discuss whether the Triple Shield hypothesis should apply to other country groups. Alternatively, expand the sample to include all countries with V-Dem data (~180 countries) to increase statistical power.
- [MINOR] (clarity) The paper mentions figures (fig1, fig2, fig3, fig4) but the figures are not included in the text. The figure captions are placeholders without detailed descriptions. This makes it difficult to evaluate whether the visualizations would effectively communicate the results.
  Action: Generate the figures or provide detailed figure descriptions. For a paper on interactions, the marginal effects plots are crucial. Figure 3 (marginal effect of inequality across education and welfare values) is particularly important and should be included.
- [MINOR] (novelty) While the 'Triple Shield' hypothesis is novel in its specific formulation, the component ideas are well-established. The novelty is in the interaction, but the paper does not cite closely related work on conditional effects of inequality.
  Action: Add a more thorough literature review on interaction effects in the inequality-democracy literature. Cite work on 'democratic resilience' (e.g., Lührmann & Lindberg 2019) which may use similar frameworks.
- [MINOR] (methodology) The paper uses the V-Dem Electoral Democracy Index as a continuous outcome. However, democratic backsliding is often conceptualized as a discrete event. The continuous measure may reduce statistical power if backsliding is episodic rather than gradual.
  Action: Consider using a binary erosion measure (as in Rau & Stokes 2024) in addition to the continuous V-Dem index. The V-Dem project provides coding of 'episodes of autocratization' which could be used to create a binary or count outcome.
</reviewer_feedback>

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

kind: hypothesis
title: >-
  The Triple Shield: Revisiting How Education and Welfare State Institutions Buffer the Inequality-Democratic Backsliding
  Link in Post-1990 Democratizers
hypothesis: >-
  In post-1990 democratizers, we investigate whether income inequality's effect on democratic quality (V-Dem electoral democracy
  index) is conditioned by education levels and welfare state spending. The original triple interaction hypothesis predicted
  that inequality threatens democracy only when both education AND welfare spending are low, but preliminary analysis with
  erroneous Gini data and severe missing data (76% exclusion rate, N=391) yielded a non-significant triple interaction (p=0.18).
  After correcting data errors and addressing missing data through multiple imputation, we now hypothesize more cautiously:
  (1) Social protection spending has a positive main effect on democratic quality, consistent with de jure constraints on
  executive predation; (2) Education has a positive main effect on democratic quality, consistent with de facto political
  capacity; (3) The inequality-democracy relationship may be buffered by high levels of EITHER education OR welfare spending
  (two-way interactions), but the specific triple interaction (requiring BOTH simultaneously) is difficult to detect with
  available data quality and sample sizes. The revised hypothesis prioritizes data quality verification, uses multiple imputation
  for missing data (SWIID Gini preferred), and tests two-way interactions before attempting triple interaction. If the triple
  interaction remains non-significant after data correction, this constitutes a valuable null result suggesting that institutional
  protections may operate independently rather than synergistically.
motivation: >-
  Despite extensive research on inequality and democratic backsliding (Acemoglu & Robinson 2006, Carothers & Hartnett 2024),
  existing work treats education and welfare states as separate protective factors. This hypothesis matters because: (1) it
  provides a nuanced, interaction-based account of democratic resilience that matches Acemoglu's de jure/de facto power framework;
  (2) it has direct policy implications—suggesting that democratizers need BOTH human capital development AND social protection
  to withstand inequality pressures; (3) it speaks to contemporary debates about why some post-1990 democratizers (e.g., Poland,
  Czechia) succeeded while others (e.g., Hungary, Turkey) backslid; (4) using OWID panels ensures reproducibility and accessibility
  of findings.
assumptions:
- >-
  V-Dem electoral democracy index adequately captures democratic quality in post-1990 democratizers
- >-
  Gini coefficient adequately measures income inequality relevant to political behavior
- >-
  Mean years of schooling captures the relevant dimension of education for political capacity
- Social protection spending as % of GDP captures welfare state generosity
- >-
  The sample of post-1990 democratizers can be meaningfully analyzed as a group despite regional differences
investigation_approach: >-
  Use Our World in Data (OWID) panel data (1990-2022) for all countries that transitioned to electoral democracy 1990-1999
  and remained sovereign through 2022. Main variables: (1) Outcome: V-Dem Electoral Democracy Index (variable 1209753); (2)
  Inequality: Gini coefficient (variable 1014857); (3) Education: Mean years of schooling (variable 809139); (4) Welfare:
  Social protection spending % GDP (variable 1210307). Estimation: Fixed-effects panel regression with triple interaction
  (inequality × education × welfare), controlling for GDP per capita, natural resource rents, ethnic fractionalization, and
  regional dummies. Test robustness with: (a) alternative inequality measures (P90/P10 ratio if available); (b) liberal democracy
  index as outcome; (c) lagged dependent variable models; (d) propensity-score matching to address selection into high-education/high-welfare
  combinations.
success_criteria: >-
  Hypothesis confirmed if: (1) Triple interaction term is statistically significant (p < 0.05) and positive (indicating buffering);
  (2) Simple effect of inequality on democracy is negative and significant when education AND welfare are low, but non-significant
  when both are high; (3) Results hold with alternative specifications and robustness checks. Hypothesis disconfirmed if:
  (1) Triple interaction is non-significant; (2) Only single interactions (inequality×education OR inequality×welfare) are
  significant but not the triple; (3) Effect disappears with basic controls.
related_works:
- >-
  Carothers & Hartnett (2024) 'Misunderstanding Democratic Backsliding' (Journal of Democracy): Argues backsliding is driven
  by predatory leaders, not economic delivery failures. Our hypothesis DIFFERS by focusing on institutional conditions (education
  + welfare) that enable resistance to such leaders, not denying their importance.
- >-
  Acemoglu & Robinson (2006) 'De Facto Political Power and Institutional Persistence' (American Economic Review): Develops
  de facto vs de jure power framework. Our hypothesis DIFFERS by empirically testing how education (de facto power) and welfare
  institutions (de jure constraints) interact to protect democracy under high inequality.
- >-
  PNAS 2024 'Income inequality and the erosion of democracy in the twenty-first century': Finds robust inequality-backsliding
  link. Our hypothesis DIFFERS by identifying conditional factors (education, welfare) that moderate this relationship, moving
  beyond simple main effects.
- >-
  Orenstein (2008) 'Poverty, Inequality, and Democracy: Postcommunist Welfare States' (Journal of Democracy): Examines welfare
  spending in post-communist countries. Our hypothesis DIFFERS by (a) including education as co-mediator, (b) testing triple
  interaction explicitly, (c) covering all post-1990 democratizers globally, not just post-communist cases.
inspiration: >-
  The hypothesis synthesizes three insights from Acemoglu's framework: (1) De facto political power (education increases citizens'
  capacity to organize and resist elite predation); (2) De jure political power (welfare state institutions constrain executive
  authority and provide formal channels for interest representation); (3) Strategic interaction between elites and masses
  under uncertainty about future political power. The triple interaction design was inspired by recent work in political economy
  on 'interlocking institutional protections' (e.g., how multiple inclusive institutions reinforce each other). The focus
  on post-1990 democratizers responds to Carothers & Hartnett's (2024) call for nuanced, context-specific analysis of backsliding
  rather than sweeping 'inequality causes backsliding' claims.
terms:
- term: De facto political power
  definition: >-
    Actual influence over political outcomes that citizens wield through collective action, protests, and informal political
    pressure, as opposed to formal legal rights (de jure power). Education increases de facto power by enhancing citizens'
    ability to coordinate and demand accountability.
- term: De jure political power
  definition: >-
    Political influence derived from formal legal and institutional arrangements, such as voting rights, legislative constraints
    on executive power, and constitutional protections. Welfare state institutions provide de jure power by creating formal
    channels for interest representation and resource redistribution.
- term: Democratic backsliding
  definition: >-
    The process by which elected leaders gradually undermine democratic institutions (free elections, civil liberties, checks
    and balances) without formally abandoning democratic institutions, typically through executive aggrandizement and norm
    erosion.
- term: Post-1990 democratizers
  definition: >-
    Countries that transitioned from authoritarian rule to electoral democracy during the 'Third Wave' peak (1990-1999), including
    post-communist states, Latin American cases completing transitions, and sub-Saharan African democratizers in the 1990s.
- term: Triple interaction
  definition: >-
    A statistical specification where the effect of one variable (inequality) on an outcome (democratic quality) depends simultaneously
    on two moderating variables (education and welfare spending), allowing testing of whether BOTH conditions must be present
    to provide protection.
- term: V-Dem Electoral Democracy Index
  definition: >-
    A continuous index (0-1) produced by Varieties of Democracy project, measuring the extent to which political leaders are
    elected under comprehensive suffrage in free and fair elections with freedom of expression and association.
summary: >-
  In post-1990 democratizers, high inequality threatens democratic quality only when citizens lack both education (de facto
  power) and welfare state protection (de jure constraints); when both are present, the inequality-democracy link is buffered.
_relation_rationale: >-
  Refining claims to acknowledge null result and data errors; same conceptual frame but more cautious scope
_confidence_delta: decreased
_key_changes:
- >-
  Added explicit acknowledgment that preliminary analysis yielded non-significant triple interaction (p=0.18)
- >-
  Identified critical Gini coefficient data error (incorrect scaling, mean=2.84 instead of ~0.28-0.65) that invalidates prior
  results
- >-
  Highlighted severe missing data problem (76% exclusion rate reduces N to 391) creating selection bias
- >-
  Shifted from confirmatory to more exploratory/cautious framing: 'we investigate whether' rather than strong prediction
- >-
  Prioritized data quality correction as prerequisite: fix Gini scaling, use SWIID or multiple imputation
- >-
  Narrowed claims: now hypothesize positive main effects of education and welfare spending (better supported by correlations:
  r=0.66 and r=0.14)
- >-
  Downgraded triple interaction from confirmed prediction to difficult-to-detect effect that may be null
- >-
  Added that null result for triple interaction would be valuable contribution (institutions may operate independently, not
  synergistically)
- >-
  Specified methodological corrections: multiple imputation primary analysis, not robustness check; verify all variable scaling
relation_type: evolution
</hypothesis>

<all_artifacts>
FULL EVIDENCE BASE: All 4 research artifacts across all iterations.

--- Item 1 ---
id: art_0hVluVdTtxOI
type: dataset
title: >-
  OWID Panel Data for Triple Shield Hypothesis - 50 Post-1990 Democratizers (1990-2022)
summary: >-
  Successfully collected and merged 8 OWID datasets plus World Bank API data into a comprehensive panel dataset. The dataset
  includes 50 post-1990 democratizers with 1,641 country-year observations from 1990-2022. Variables include: V-Dem Electoral
  Democracy Index (outcome), Gini coefficient, mean years of schooling, social protection spending (% GDP), GDP per capita,
  natural resource rents, population, and derived interaction terms (gini×education, gini×social, triple interaction). Data
  sources verified: OWID (V-Dem, Gini, education, social spending, GDP, population, resource rents) and World Bank API (supplementary
  Gini, education, GDP, population, social spending). Missing data documented: gini 54%, education 34%, social spending 52%.
  Correlations with V-Dem: social_spending=0.66, education=0.14, gini=0.12. Dataset formatted into exp_sel_data_out.json schema
  with 1,641 examples (each country-year observation as separate example). Validation passed. Files: full_data_out.json (1.3MB),
  mini_data_out.json, preview_data_out.json, data_dictionary.json, pyproject.toml with pinned dependencies.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_wB2RIRpHGhWl
type: research
title: 'Triple Shield Hypothesis: Inequality, Education, Welfare, Democracy'
summary: >-
  This artifact provides a comprehensive literature review evaluating the 'Triple Shield' hypothesis, which posits that income
  inequality threatens democratic resilience, but education (de facto political capacity) and welfare state institutions (de
  jure constraints) interact to protect democracy. The review synthesizes findings across four thematic areas: (1) the inequality-democratic
  backsliding link, (2) education as de facto political power, (3) welfare state institutions as de jure constraints, and
  (4) methodological approaches to triple interactions in panel data. Key findings include: Rau & Stokes (2024) provide robust
  evidence that income inequality predicts democratic erosion [1], while Carothers & Hartnett (2024) complicate this by emphasizing
  predatory leaders over delivery failures [2]. Acemoglu & Robinson's (2006) de facto/de jure framework provides theoretical
  foundation [3]. The review identifies 15+ key empirical papers, validates OWID and V-Dem data sources, and provides methodological
  guidance for specifying and interpreting triple interactions in panel data. The output includes a 5000-word research report
  (research_report.md) and structured JSON output (research_out.json) with citations, sources, and follow-up questions for
  further investigation.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 3 ---
id: art_jpaofTxfGJl-
type: dataset
title: Post-1990 Democratizers Panel Dataset (1990-2022)
summary: >-
  This dataset contains 1,552 country-year observations from 48 post-1990 democratizers covering 1990-2022. Variables include:
  (1) Gini coefficient (0-1 scale, mean=0.39, correctly scaled from World Bank PIP via OWID), (2) V-Dem Electoral Democracy
  Index (0-1 scale, mean=0.61), (3) Mean years of schooling (0-17 years, mean=8.3), (4) Social protection spending (% GDP,
  mean=13.2%). Data sources: OWID (World Bank PIP, V-Dem v13, Barro-Lee education, OECD social spending). Multiple Imputation
  by Chained Equations (MICE) applied via sklearn IterativeImputer with bounds constraints to ensure valid ranges. Dataset
  formatted for experiment pipeline as regression task: predict V-Dem democracy index from Gini + education + social spending
  + region dummies. JSON schema validated against exp_sel_data_out.json format. Files: full_data_out.json (1.4MB, 1,552 examples),
  mini_data_out.json (3.4KB, 3 examples), preview_data_out.json (2.4KB, 3 truncated examples). Data dictionary and metadata
  included. File size well under 300MB limit (actual: 2MB).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 4 ---
id: art_sZylIgzAmw7c
type: experiment
title: Triple Interaction Analysis with MICE Imputation on OWID Panel Data
summary: >-
  This experiment implements a confirmatory test of the triple interaction hypothesis (inequality × education × welfare spending)
  on democratic resilience using panel data from 50 post-1990 democratizers. The analysis corrects Gini scaling errors (mixed
  0-1 and 0-100 scales) identified in the data, implements MICE multiple imputation with 50 imputations to handle 54% missing
  Gini values, 34% missing education, and 52% missing social spending, and runs fixed-effects panel regressions with clustered
  standard errors. The primary hypothesis test examines whether the triple interaction coefficient is positive and statistically
  significant (p < 0.05). Marginal effects are computed per Brambor et al. (2006) at education and welfare = -1SD, 0, +1SD.
  Results show the triple interaction coefficient = 0.0065 (p = 0.1399, 95% CI [-0.0021, 0.0151]), which is not statistically
  significant. The analysis includes Rubin's Rules pooling across imputations, robustness checks comparing complete case vs.
  imputed results, and verification of Gini scaling corrections. The dataset includes 1,641 country-year observations from
  1990-2022. Data sources: Our World in Data (V-Dem, Gini, education, social spending, GDP, population, resource rents) and
  World Bank API. All code uses Python with linearmodels for panel regression, miceforest for MICE imputation, and loguru
  for logging. The method.py script is fully self-contained with data loading, Gini correction, MICE imputation, interaction
  term creation, panel regression, Rubin's Rules pooling, and results export to method_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 2 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

title: Post-1990 Democratizers Panel Dataset (1990-2022)
id: art_jpaofTxfGJl-
type: dataset
summary: >-
  This dataset contains 1,552 country-year observations from 48 post-1990 democratizers covering 1990-2022. Variables include:
  (1) Gini coefficient (0-1 scale, mean=0.39, correctly scaled from World Bank PIP via OWID), (2) V-Dem Electoral Democracy
  Index (0-1 scale, mean=0.61), (3) Mean years of schooling (0-17 years, mean=8.3), (4) Social protection spending (% GDP,
  mean=13.2%). Data sources: OWID (World Bank PIP, V-Dem v13, Barro-Lee education, OECD social spending). Multiple Imputation
  by Chained Equations (MICE) applied via sklearn IterativeImputer with bounds constraints to ensure valid ranges. Dataset
  formatted for experiment pipeline as regression task: predict V-Dem democracy index from Gini + education + social spending
  + region dummies. JSON schema validated against exp_sel_data_out.json format. Files: full_data_out.json (1.4MB, 1,552 examples),
  mini_data_out.json (3.4KB, 3 examples), preview_data_out.json (2.4KB, 3 truncated examples). Data dictionary and metadata
  included. File size well under 300MB limit (actual: 2MB).

title: Triple Interaction Analysis with MICE Imputation on OWID Panel Data
id: art_sZylIgzAmw7c
type: experiment
summary: >-
  This experiment implements a confirmatory test of the triple interaction hypothesis (inequality × education × welfare spending)
  on democratic resilience using panel data from 50 post-1990 democratizers. The analysis corrects Gini scaling errors (mixed
  0-1 and 0-100 scales) identified in the data, implements MICE multiple imputation with 50 imputations to handle 54% missing
  Gini values, 34% missing education, and 52% missing social spending, and runs fixed-effects panel regressions with clustered
  standard errors. The primary hypothesis test examines whether the triple interaction coefficient is positive and statistically
  significant (p < 0.05). Marginal effects are computed per Brambor et al. (2006) at education and welfare = -1SD, 0, +1SD.
  Results show the triple interaction coefficient = 0.0065 (p = 0.1399, 95% CI [-0.0021, 0.0151]), which is not statistically
  significant. The analysis includes Rubin's Rules pooling across imputations, robustness checks comparing complete case vs.
  imputed results, and verification of Gini scaling corrections. The dataset includes 1,641 country-year observations from
  1990-2022. Data sources: Our World in Data (V-Dem, Gini, education, social spending, GDP, population, resource rents) and
  World Bank API. All code uses Python with linearmodels for panel regression, miceforest for MICE imputation, and loguru
  for logging. The method.py script is fully self-contained with data loading, Gini correction, MICE imputation, interaction
  term creation, panel regression, Rubin's Rules pooling, and results export to method_out.json.
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison):
  {"id": "fig3", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: latency (seconds, 0-5). Values: PostgreSQL=4.6s (red), Bao=2.8s (blue), RLQOpt=2.0s (green). Error bars +/-0.3-0.8. Sans-serif font, white background.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero):
  {"id": "fig1", "title": "System Architecture", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Short descriptive figure title",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "Detailed image generation prompt \u2014 axes, labels, ALL numeric values, colors, aspect ratio, layout. The image generator cannot read files; this is its ONLY input.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title - concise, descriptive, captures the main contribution",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-22 13:12:33 UTC

```
Direction: Comparative Political Economy — Inequality and Democratic Resilience. Something genuinely novel and groundbreaking that traces how inequality, education, and democratic-quality co-evolve across post-1990 democratizers, identifies what sustains resilience versus backsliding, and tests whether welfare-state institutions mediate the link. MUST use Our World in Data (OWID) panels.

Ambition: level 1 of 5 — confirmatory/parametric science: a careful confirmatory test within established institutional-economics theory; precision, identification, and robustness over conceptual novelty.

Reviewer: I am Daron Acemoglu (MIT). Calibrate from my existing work. Cross-domain perspectives (historical sociology, political behavior, economic anthropology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for the American Political Science Review, the Journal of Democracy, or World Politics. Audience: comparative political economists and political scientists. Tone: empirically rigorous, grounded in institutional economics, reproducible on public OWID data.
```

### [3] SKILL-INPUT — aii-paper-writing · 2026-06-22 13:12:53 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: Academic paper writing guidance for AI research. Covers paper structure, figure placeholders, bibliography building with Semantic Scholar, and citation rules. Does NOT cover LaTeX compilation or figure file generation — see aii-paper-to-latex for that.
---

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in one batch
3. Write the returned .bib text into `./references.bib`

Rules:
- Do NOT fabricate BibTeX entries — always fetch from Semantic Scholar
- If a paper isn't found (very recent preprint), write the entry manually as fallback
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-06-22 13:12:53 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SKILL-INPUT — aii-web-tools · 2026-06-22 13:14:11 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````
