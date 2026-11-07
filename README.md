# IPL Player Performance Analytics V2

An end-to-end IPL analytics application built with Django, MySQL, Machine Learning, and Deep Learning. The platform provides player performance analysis, batting and bowling analytics, match exploration, model evaluation, and next-match performance predictions.

## 1. Project Overview

IPL Player Performance Analytics V2 combines historical cricket data, statistical analysis, and predictive modelling in a web-based analytics platform.

The application is designed to help users:

- Explore IPL player and match performance.
- Analyse batting and bowling statistics.
- Compare two players across performance metrics.
- Explore season-wise and venue-wise trends.
- Evaluate trained Machine Learning and Deep Learning models.
- Generate next-match player performance predictions.

**Prediction definition:** Predict a player's next regular-innings appearance after the current match has completed.

## 2. Key Features

| Module | Capabilities |
|---|---|
| Dashboard | Overall dataset KPIs and season-level match statistics |
| Player Explorer | Player search, profiles, batting and bowling statistics |
| Player Comparison | Compare two players using performance metrics and charts |
| Batting Analytics | Runs, boundaries, batting averages, strike rates and leaderboards |
| Bowling Analytics | Wickets, economy, bowling average, strike rate and leaderboards |
| Match Explorer | Match search, filters and innings scorecards |
| EDA & Insights | Season, venue, team and player performance analysis |
| Batting Predictions | ML and DL batting performance predictions |
| Bowling Predictions | ML and DL bowling performance predictions |
| Model Comparison | Compare selected models using saved evaluation results |

## 3. Technology Stack

**Backend**
- Python 3.12
- Django 5.2
- PyMySQL

**Database**
- MySQL 8
- SQL-based analytical tables

**Data Science and Machine Learning**
- NumPy
- Pandas
- SciPy
- Scikit-learn
- XGBoost
- CatBoost
- Joblib

**Deep Learning**
- TensorFlow / Keras

**Visualisation**
- Matplotlib
- Seaborn
- Chart.js

**Development**
- Anaconda / Conda
- Jupyter Notebook
- VS Code
- Git and GitHub

## 4. System Architecture

```text
Historical IPL Data
        |
        v
Data Processing and ETL
        |
        v
Processed Analytical Tables
        |
        v
MySQL Database
        |
        v
Django Application
        |
        +----------------------+
        |                      |
        v                      v
  Analytics Modules      Prediction Modules
        |                      |
        v                      v
  Django Views           ML / DL Inference
        |                      |
        v                      v
  HTML Templates         Saved Model Artifacts
        |                      |
        +-----------+----------+
                    |
                    v
             Web Interface
```

## 5. Machine Learning and Deep Learning

The project maintains saved model artifacts for inference and model evaluation.

### Deep Learning

The model registry contains 10 registered Deep Learning models:

| Category | Prediction targets |
|---|---|
| Batting | Runs scored, balls faced, fours, sixes, strike rate, dismissals |
| Bowling | Wickets