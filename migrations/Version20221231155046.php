<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20221231155046 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE game DROP created_by, DROP modified_by, DROP modified_at, DROP is_deleted, CHANGE data data LONGTEXT NOT NULL COMMENT \'(DC2Type:json)\'');
        $this->addSql('ALTER TABLE initial_survey DROP created_by, DROP modified_by, DROP modified_at, DROP is_deleted');
        $this->addSql('ALTER TABLE user DROP created_by, DROP modified_by, CHANGE roles roles LONGTEXT NOT NULL COMMENT \'(DC2Type:json)\', CHANGE modified_at modify_at DATETIME DEFAULT NULL');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE initial_survey ADD created_by INT NOT NULL, ADD modified_by INT DEFAULT NULL, ADD modified_at DATETIME DEFAULT NULL, ADD is_deleted TINYINT(1) NOT NULL');
        $this->addSql('ALTER TABLE user ADD created_by INT NOT NULL, ADD modified_by INT DEFAULT NULL, CHANGE roles roles LONGTEXT NOT NULL COLLATE `utf8mb4_bin`, CHANGE modify_at modified_at DATETIME DEFAULT NULL');
        $this->addSql('ALTER TABLE game ADD created_by INT NOT NULL, ADD modified_by INT DEFAULT NULL, ADD modified_at DATETIME DEFAULT NULL, ADD is_deleted TINYINT(1) NOT NULL, CHANGE data data LONGTEXT NOT NULL COLLATE `utf8mb4_bin`');
    }
}
