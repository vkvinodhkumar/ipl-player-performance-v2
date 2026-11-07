
from django.db import models


class BattingNextMatchFeatures(models.Model):
    """
    Read-only ORM mapping for batting_next_match_features.

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
        related_name="batting_next_match_features"
    )

    player = models.CharField(max_length=100)

    # Current-match features
    is_super_over = models.IntegerField()
    batting_team = models.CharField(max_length=100)
    runs_scored = models.IntegerField()
    balls_faced = models.IntegerField()
    fours = models.IntegerField()
    sixes = models.IntegerField()
    dismissals = models.IntegerField()
    retired_hurt_count = models.IntegerField()

    strike_rate = models.FloatField(blank=True, null=True)
    batting_average = models.FloatField(blank=True, null=True)

    innings_batted = models.IntegerField()
    not_out_innings = models.IntegerField()

    season = models.CharField(max_length=30)
    date = models.DateField()
    match_type = models.CharField(max_length=30)

    # Next-match prediction targets
    target_next_match_runs_scored = models.IntegerField(
        blank=True, null=True
    )
    target_next_match_balls_faced = models.IntegerField(
        blank=True, null=True
    )
    target_next_match_fours = models.IntegerField(
        blank=True, null=True
    )
    target_next_match_sixes = models.IntegerField(
        blank=True, null=True
    )
    target_next_match_strike_rate = models.FloatField(
        blank=True, null=True
    )
    target_next_match_dismissals = models.IntegerField(
        blank=True, null=True
    )

    # Previous-match information
    previous_match_date = models.DateField(
        blank=True, null=True
    )
    days_since_previous_match = models.IntegerField(
        blank=True, null=True
    )

    # Historical runs features
    previous_runs_scored = models.IntegerField(
        blank=True, null=True
    )
    runs_scored_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    runs_scored_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    runs_scored_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    runs_scored_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical balls-faced features
    previous_balls_faced = models.IntegerField(
        blank=True, null=True
    )
    balls_faced_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    balls_faced_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    balls_faced_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    balls_faced_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical fours features
    previous_fours = models.IntegerField(
        blank=True, null=True
    )
    fours_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    fours_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    fours_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    fours_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical sixes features
    previous_sixes = models.IntegerField(
        blank=True, null=True
    )
    sixes_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    sixes_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    sixes_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    sixes_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical strike-rate features
    previous_strike_rate = models.FloatField(
        blank=True, null=True
    )
    strike_rate_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    strike_rate_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    strike_rate_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    strike_rate_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    # Historical dismissals features
    previous_dismissals = models.IntegerField(
        blank=True, null=True
    )
    dismissals_rolling_mean_3 = models.FloatField(
        blank=True, null=True
    )
    dismissals_rolling_mean_5 = models.FloatField(
        blank=True, null=True
    )
    dismissals_rolling_mean_10 = models.FloatField(
        blank=True, null=True
    )
    dismissals_expanding_mean = models.FloatField(
        blank=True, null=True
    )

    matches_played_before = models.IntegerField()

    class Meta:
        managed = False
        db_table = "batting_next_match_features"
        verbose_name = "Batting Next Match Feature"
        verbose_name_plural = "Batting Next Match Features"
        ordering = ["-date", "player"]

    def __str__(self):
        return (
            f"{self.player} - "
            f"{self.date} - "
            f"{self.runs_scored} runs"
        )
