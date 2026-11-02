CREATE DATABASE IF NOT EXISTS `ipl_analytics` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `ipl_analytics`;

CREATE TABLE IF NOT EXISTS `matches` (
    `match_id` VARCHAR(20) NOT NULL,
    `source_file` VARCHAR(100) NOT NULL,
    `season` VARCHAR(10) NOT NULL,
    `date` DATE NOT NULL,
    `match_type` VARCHAR(20) NOT NULL,
    `gender` VARCHAR(20) NOT NULL,
    `team_type` VARCHAR(30) NOT NULL,
    `overs_limit` SMALLINT NOT NULL,
    `venue` VARCHAR(150) NOT NULL,
    `city` VARCHAR(100) NOT NULL,
    `city_original` VARCHAR(100) NULL,
    `city_was_imputed` BOOLEAN NOT NULL,
    `team1` VARCHAR(100) NOT NULL,
    `team2` VARCHAR(100) NOT NULL,
    `teams_json` JSON NOT NULL,
    `toss_winner` VARCHAR(100) NOT NULL,
    `toss_decision` VARCHAR(20) NOT NULL,
    `winner` VARCHAR(100) NULL,
    `result` VARCHAR(30) NULL,
    `method` VARCHAR(30) NULL,
    `eliminator` VARCHAR(100) NULL,
    `bowl_out` INT NULL,
    `player_of_match` VARCHAR(100) NOT NULL,
    `event_name` VARCHAR(150) NOT NULL,
    `event_match_number` INT NULL,
    `event_stage` VARCHAR(100) NULL,
    PRIMARY KEY (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `innings` (
    `match_id` VARCHAR(20) NOT NULL,
    `innings_number` SMALLINT NOT NULL,
    `batting_team` VARCHAR(100) NOT NULL,
    `is_super_over` BOOLEAN NOT NULL,
    `target_runs` INT NULL,
    `target_overs` DECIMAL(5,2) NULL,
    `overs_recorded` SMALLINT NOT NULL,
    `delivery_count` INT NOT NULL,
    `legal_deliveries` INT NOT NULL,
    `total_runs` INT NOT NULL,
    `extras_runs` INT NOT NULL,
    `batter_runs` INT NOT NULL,
    `wicket_records` SMALLINT NOT NULL,
    `actual_dismissals` SMALLINT NOT NULL,
    PRIMARY KEY (`match_id`, `innings_number`),
    CONSTRAINT `fk_innings_matches` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `deliveries` (
    `match_id` VARCHAR(20) NOT NULL,
    `innings_number` SMALLINT NOT NULL,
    `over_number` SMALLINT NOT NULL,
    `delivery_index_in_over` SMALLINT NOT NULL,
    `batting_team` VARCHAR(100) NOT NULL,
    `batter` VARCHAR(100) NOT NULL,
    `bowler` VARCHAR(100) NOT NULL,
    `non_striker` VARCHAR(100) NOT NULL,
    `batter_runs` INT NOT NULL,
    `extras_runs` INT NOT NULL,
    `total_runs` INT NOT NULL,
    `wides` SMALLINT NOT NULL,
    `noballs` SMALLINT NOT NULL,
    `byes` SMALLINT NOT NULL,
    `legbyes` SMALLINT NOT NULL,
    `penalty` SMALLINT NOT NULL,
    `is_legal_delivery` BOOLEAN NOT NULL,
    `wicket_count` SMALLINT NOT NULL,
    `wicket_kinds` VARCHAR(255) NOT NULL,
    `wickets_json` JSON NOT NULL,
    `extras_json` JSON NOT NULL,
    PRIMARY KEY (`match_id`, `innings_number`, `over_number`, `delivery_index_in_over`),
    CONSTRAINT `fk_deliveries_innings` FOREIGN KEY (`match_id`, `innings_number`) REFERENCES `innings` (`match_id`, `innings_number`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;