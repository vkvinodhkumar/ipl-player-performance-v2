
from django.db import models


class BowlingNextMatchFeatures(models.Model):
    """
    Read-only ORM mapping for bowling_next_match_features.

    Contains current-match statistics, historical features,
    and next-appearance prediction targets.
    """

    pk = models.CompositePrimaryKey(
        "match_id",
        "player"
    )

    match = models.ForeignKey(
        "matches.Matches",
        on_delete=models.DO_NOTHING,
        db_column="match_id",
        related_name="bowling_next_match_features"
    )

    player = models.CharField(max_length=100)

    # Current-match features
    is_super_over = models.IntegerField()
    runs_conceded = models.IntegerField()
    legal_balls = models.IntegerField()
    wides_conceded = models.IntegerField()
    noballs_conceded = models.IntegerField()
    innings_bowled = models.IntegerField()
    wickets = models.IntegerField()
    overs_bowled = models.FloatField()

    economy_rate = models.FloatField(blank=True, null=True)
    bowling_average = models.FloatField(blank=True, null=True)
    bowling_strike_rate = models.FloatField(blank=True, null=True)

    season = models.CharField(max_length=30)
    date = models.DateField()
    match_type = models.CharField(max_length=30)

    # Next-match prediction targets
    target_next_match_wickets = models.IntegerField(
        blank=True, null=True
    )
    target_next_match_runs_conceded = models.IntegerField(
        blank=True, null=True
    )
    target_next_match_legal_balls = models.IntegerField(
        blank=True, null=True
    )
    target_next_match_economy_rate = models.FloatField(
        blank=True, null=True
    )

    # Previous-match information
    previous_match_date = models.DateField(
        blank=True, null=True
    )
    days_since_previous_match = models.IntegerField(
        blank=True, null=True
    )

    # Historical wickets features
    previous_wickets = models.IntegerField(
        blank=True, null=True
    )
    wickets_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    wickets_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    wickets_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    wickets_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical runs-conceded features
    previous_runs_conceded = models.IntegerField(
        blank=True, null=True
    )
    runs_conceded_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    runs_conceded_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    runs_conceded_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    runs_conceded_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical legal-balls features
    previous_legal_balls = models.IntegerField(
        blank=True, null=True
    )
    legal_balls_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    legal_balls_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    legal_balls_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    legal_balls_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical economy-rate features
    previous_economy_rate = models.FloatField(
        blank=True, null=True
    )
    economy_rate_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    economy_rate_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    economy_rate_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    economy_rate_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    matches_played_before = models.IntegerField()

    class Meta:
        managed = False
        db_table = "bowling_next_match_features"
        verbose_name = "Bowling Next Match Feature"
        verbose_name_plural = "Bowling Next Match Features"
        ordering = ["-date", "player"]

    def __str__(self):
        return (
            f"{self.player} - "
            f"{self.date} - "
            f"{self.wickets} wickets"
        )
