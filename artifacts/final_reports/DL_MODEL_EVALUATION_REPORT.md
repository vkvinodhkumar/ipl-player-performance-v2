# DL / ML Model Evaluation Report

## Evaluation design

- Chronological test period: 2024-05-02 to 2026-05-29.
- All ten target alignment checks passed.
- Saved preprocessors and target scalers were used for DL inference.

## Selected model test metrics

| target | selected_model | input_rows | MAE | RMSE | R2 |
| --- | --- | --- | --- | --- | --- |
| target_next_match_runs_scored | batting_original | 2375 | 16.6438 | 22.4600 | 0.1116 |
| target_next_match_balls_faced | DL_MLP | 2375 | 9.3641 | 12.0186 | 0.1276 |
| target_next_match_fours | DL_MLP | 2375 | 1.6712 | 2.2951 | 0.1113 |
| target_next_match_sixes | DL_MLP | 2375 | 1.1580 | 1.7900 | -0.0226 |
| target_next_match_strike_rate | DL_MLP | 2373 | 58.5298 | 76.0547 | -0.0233 |
| target_next_match_dismissals | DL_MLP | 2375 | 0.2727 | 0.4018 | 0.0397 |
| target_next_match_wickets | bowling_wickets | 1805 | 0.7637 | 0.9936 | 0.0236 |
| target_next_match_runs_conceded | DL_MLP | 1805 | 9.2279 | 11.5773 | 0.1035 |
| target_next_match_legal_balls | DL_MLP | 1805 | 3.8724 | 5.3706 | 0.1938 |
| target_next_match_economy_rate | DL_MLP | 1805 | 2.8214 | 4.0583 | -0.1173 |

## Interpretation

MAE and RMSE measure prediction error in target units.
R² measures explained variance relative to a test-set mean predictor.

Negative R² indicates limited predictive performance.

## Output constraints

Count targets are clipped at zero and rounded to integers.
Rate targets are clipped at zero and rounded to two decimal places.

Raw predictions are retained separately from constrained predictions.
Constrained metrics describe output behavior, not original model
performance.
