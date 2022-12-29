<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20221229170703 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE game (id INT AUTO_INCREMENT NOT NULL, user_id INT NOT NULL, time TIME NOT NULL, data JSON NOT NULL, score DOUBLE PRECISION NOT NULL, created_by INT NOT NULL, created_at DATETIME NOT NULL, modified_by INT DEFAULT NULL, modified_at DATETIME DEFAULT NULL, is_deleted TINYINT(1) NOT NULL, INDEX IDX_232B318CA76ED395 (user_id), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE initial_survey (id INT AUTO_INCREMENT NOT NULL, user_id INT NOT NULL, age VARCHAR(255) NOT NULL, gender VARCHAR(255) NOT NULL, work_type VARCHAR(255) NOT NULL, preferred_playing_style VARCHAR(255) NOT NULL, favourite_game_type VARCHAR(255) NOT NULL, computer_usage_per_day DOUBLE PRECISION NOT NULL, gaming_per_day DOUBLE PRECISION NOT NULL, created_by INT NOT NULL, created_at DATETIME NOT NULL, modified_by INT DEFAULT NULL, modified_at DATETIME DEFAULT NULL, is_deleted TINYINT(1) NOT NULL, UNIQUE INDEX UNIQ_D48B0400A76ED395 (user_id), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE user (id INT AUTO_INCREMENT NOT NULL, email VARCHAR(180) DEFAULT NULL, roles JSON NOT NULL, password VARCHAR(255) DEFAULT NULL, created_by INT NOT NULL, created_at DATETIME NOT NULL, modified_by INT DEFAULT NULL, modified_at DATETIME DEFAULT NULL, is_deleted TINYINT(1) NOT NULL, UNIQUE INDEX UNIQ_8D93D649E7927C74 (email), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('CREATE TABLE messenger_messages (id BIGINT AUTO_INCREMENT NOT NULL, body LONGTEXT NOT NULL, headers LONGTEXT NOT NULL, queue_name VARCHAR(190) NOT NULL, created_at DATETIME NOT NULL, available_at DATETIME NOT NULL, delivered_at DATETIME DEFAULT NULL, INDEX IDX_75EA56E0FB7336F0 (queue_name), INDEX IDX_75EA56E0E3BD61CE (available_at), INDEX IDX_75EA56E016BA31DB (delivered_at), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('ALTER TABLE game ADD CONSTRAINT FK_232B318CA76ED395 FOREIGN KEY (user_id) REFERENCES user (id)');
        $this->addSql('ALTER TABLE initial_survey ADD CONSTRAINT FK_D48B0400A76ED395 FOREIGN KEY (user_id) REFERENCES user (id)');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE game DROP FOREIGN KEY FK_232B318CA76ED395');
        $this->addSql('ALTER TABLE initial_survey DROP FOREIGN KEY FK_D48B0400A76ED395');
        $this->addSql('DROP TABLE game');
        $this->addSql('DROP TABLE initial_survey');
        $this->addSql('DROP TABLE user');
        $this->addSql('DROP TABLE messenger_messages');
    }
}
