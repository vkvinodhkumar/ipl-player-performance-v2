
from django.db import models


class Matches(models.Model):
    """
    Read-only ORM mapping for the existing MySQL matches table.
    """

    match_id = models.CharField(
        primary_key=True,
        max_length=20
    )

    source_file = models.CharField(max_length=100)
    season = models.CharField(max_length=10)
    date = models.DateField()
    match_type = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    team_type = models.CharField(max_length=30)
    overs_limit = models.SmallIntegerField()

    venue = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    city_original = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    city_was_imputed = models.IntegerField()

    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    teams_json = models.JSONField()

    toss_winner = models.CharField(max_length=100)
    toss_decision = models.CharField(max_length=20)

    winner = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    result = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    method = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    eliminator = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    bowl_out = models.IntegerField(
        blank=True,
        null=True
    )

    player_of_match = models.CharField(max_length=100)
    event_name = models.CharField(max_length=150)
    event_match_number = models.IntegerField(
        blank=True,
        null=True
    )
    event_stage = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = "matches"
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.match_id} - {self.team1} vs {self.team2}"



class Innings(models.Model):
    """
    Read-only ORM mapping for the existing MySQL innings table.
    """

    pk = models.CompositePrimaryKey(
        "match_id",
        "innings_number"
    )

    match = models.ForeignKey(
        Matches,
        on_delete=models.DO_NOTHING,
        db_column="match_id",
        related_name="innings"
    )

    innings_number = models.SmallIntegerField()
    batting_team = models.CharField(max_length=100)
    is_super_over = models.IntegerField()

    target_runs = models.IntegerField(
        blank=True,
        null=True
    )

    target_overs = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    overs_recorded = models.SmallIntegerField()
    delivery_count = models.IntegerField()
    legal_deliveries = models.IntegerField()
    total_runs = models.IntegerField()
    extras_runs = models.IntegerField()
    batter_runs = models.IntegerField()
    wicket_records = models.SmallIntegerField()
    actual_dismissals = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = "innings"
        verbose_name = "Innings"
        verbose_name_plural = "Innings"

    def __str__(self):
        return (
            f"{self.match_id} - "
            f"Innings {self.innings_number}"
        )



class Deliveries(models.Model):
    """
    Read-only ORM mapping for the existing MySQL deliveries table.

    The database has a composite foreign key:
    (match_id, innings_number) -> innings(match_id, innings_number).

    Django does not natively support composite ForeignKey fields.
    Therefore, these columns are represented as scalar fields.
    """

    pk = models.CompositePrimaryKey(
        "match_id",
        "innings_number",
        "over_number",
        "delivery_index_in_over"
    )

    # Composite FK components: intentionally scalar fields.
    match_id = models.CharField(max_length=20)
    innings_number = models.SmallIntegerField()

    over_number = models.SmallIntegerField()
    delivery_index_in_over = models.SmallIntegerField()

    batting_team = models.CharField(max_length=100)
    batter = models.CharField(max_length=100)
    bowler = models.CharField(max_length=100)
    non_striker = models.CharField(max_length=100)

    batter_runs = models.IntegerField()
    extras_runs = models.IntegerField()
    total_runs = models.IntegerField()

    wides = models.SmallIntegerField()
    noballs = models.SmallIntegerField()
    byes = models.SmallIntegerField()
    legbyes = models.SmallIntegerField()
    penalty = models.SmallIntegerField()

    is_legal_delivery = models.IntegerField()
    wicket_count = models.SmallIntegerField()
    wicket_kinds = models.CharField(max_length=255)

    wickets_json = models.JSONField()
    extras_json = models.JSONField()

    class Meta:
        managed = False
        db_table = "deliveries"
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
        ordering = [
            "match_id",
            "innings_number",
            "over_number",
            "delivery_index_in_over",
        ]

    def __str__(self):
        return (
            f"{self.match_id} | "
            f"Innings {self.innings_number} | "
            f"Over {self.over_number} | "
            f"Ball {self.delivery_index_in_over}"
        )
