
from django.db import models


class BattingPlayerMatchRegular(models.Model):
    """
    Read-only ORM mapping for batting_player_match_regular.
    """

    pk = models.CompositePrimaryKey(
        "match_id",
        "player"
    )

    match = models.ForeignKey(
        "matches.Matches",
        on_delete=models.DO_NOTHING,
        db_column="match_id",
        related_name="batting_performances"
    )

    player = models.CharField(max_length=100)
    is_super_over = models.IntegerField()
    batting_team = models.CharField(max_length=100)

    runs_scored = models.IntegerField()
    balls_faced = models.IntegerField()
    fours = models.IntegerField()
    sixes = models.IntegerField()
    dismissals = models.IntegerField()
    retired_hurt_count = models.IntegerField()

    strike_rate = models.FloatField(
        blank=True,
        null=True
    )

    batting_average = models.FloatField(
        blank=True,
        null=True
    )

    innings_batted = models.IntegerField()
    not_out_innings = models.IntegerField()

    season = models.CharField(max_length=30)
    date = models.DateField()
    match_type = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "batting_player_match_regular"
        verbose_name = "Batting Player Match"
        verbose_name_plural = "Batting Player Matches"
        ordering = ["-date", "player"]

    def __str__(self):
        return f"{self.player} - {self.runs_scored} runs"



class BowlingPlayerMatchRegular(models.Model):
    """
    Read-only ORM mapping for bowling_player_match_regular.
    """

    pk = models.CompositePrimaryKey(
        "match_id",
        "player"
    )

    match = models.ForeignKey(
        "matches.Matches",
        on_delete=models.DO_NOTHING,
        db_column="match_id",
        related_name="bowling_performances"
    )

    player = models.CharField(max_length=100)
    is_super_over = models.IntegerField()

    runs_conceded = models.IntegerField()
    legal_balls = models.IntegerField()
    wides_conceded = models.IntegerField()
    noballs_conceded = models.IntegerField()

    innings_bowled = models.IntegerField()
    wickets = models.IntegerField()
    overs_bowled = models.FloatField()

    economy_rate = models.FloatField(
        blank=True,
        null=True
    )

    bowling_average = models.FloatField(
        blank=True,
        null=True
    )

    bowling_strike_rate = models.FloatField(
        blank=True,
        null=True
    )

    season = models.CharField(max_length=30)
    date = models.DateField()
    match_type = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "bowling_player_match_regular"
        verbose_name = "Bowling Player Match"
        verbose_name_plural = "Bowling Player Matches"
        ordering = ["-date", "player"]

    def __str__(self):
        return (
            f"{self.player} - "
            f"{self.wickets} wickets"
        )
