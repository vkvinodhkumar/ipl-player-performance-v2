# IPL Player Performance Analytics V2
## Final Target-Specific Model Selection

**Generated:** 2026-11-02T16:47:21.020601+00:00

### Selection policy

- Primary metric: MAE
- Supporting metrics: RMSE, R² and bias
- Evaluation: chronological held-out test data
- Test period: 2024-05-02 to 2026-05-29
- Baseline: independently calculated training-mean predictor

### Selected models

| target | selected_model | selected_MAE | selected_RMSE | selected_R2 | MAE_improvement_pct |
| --- | --- | --- | --- | --- | --- |
| target_next_match_runs_scored | batting_original | 16.6438 | 22.4600 | 0.1116 | 8.0160 |
| target_next_match_balls_faced | DL_MLP | 9.3641 | 12.0186 | 0.1276 | 10.1680 |
| target_next_match_fours | DL_MLP | 1.6712 | 2.2951 | 0.1113 | 8.5450 |
| target_next_match_sixes | DL_MLP | 1.1580 | 1.7900 | -0.0226 | 4.3739 |
| target_next_match_strike_rate | DL_MLP | 58.5298 | 76.0547 | -0.0233 | 4.7250 |
| target_next_match_dismissals | DL_MLP | 0.2727 | 0.4018 | 0.0397 | 19.9286 |
| target_next_match_wickets | bowling_wickets | 0.7637 | 0.9936 | 0.0236 | 2.3521 |
| target_next_match_runs_conceded | DL_MLP | 9.2279 | 11.5773 | 0.1035 | 13.2118 |
| target_next_match_legal_balls | DL_MLP | 3.8724 | 5.3706 | 0.1938 | 23.3679 |
| target_next_match_economy_rate | DL_MLP | 2.8214 | 4.0583 | -0.1173 | 3.8275 |

### Selection notes

- Runs scored: batting_original selected for balanced RMSE and R²;
  batting_sqrt has marginally lower MAE.
- Wickets: bowling_wickets selected over DL and baseline.
- Eight targets selected DL MLP models.
- Two targets selected ML models.
- Strike rate and economy rate have negative test R².

### Bowling baseline discrepancy

Saved DummyRegressor metrics differ from the independently recalculated
training-mean baseline. The comparison was rebuilt using aligned
held-out test indices. The precise historical cause of the difference
has not been established.
