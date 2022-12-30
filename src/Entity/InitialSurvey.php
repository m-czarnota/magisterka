<?php

namespace App\Entity;

use App\Enum\InitialSurvey\AgeEnum;
use App\Enum\InitialSurvey\GameTypeEnum;
use App\Enum\InitialSurvey\GenderEnum;
use App\Enum\InitialSurvey\PlayingStyleEnum;
use App\Enum\InitialSurvey\WorkTypeEnum;
use App\Repository\InitialSurveyRepository;
use Doctrine\ORM\Mapping as ORM;
use App\Trait\Entity\HistoryEntityTrait;

#[ORM\Entity(repositoryClass: InitialSurveyRepository::class)]
class InitialSurvey
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\OneToOne(inversedBy: 'initialSurvey')]
    #[ORM\JoinColumn(nullable: false)]
    private ?User $user = null;

    #[ORM\Column(type: 'string', length: 255, enumType: AgeEnum::class)]
    private ?AgeEnum $age = null;

    #[ORM\Column(type: 'string', length: 255, enumType: GenderEnum::class)]
    private ?GenderEnum $gender = null;

    #[ORM\Column(type: 'string', length: 255, enumType: WorkTypeEnum::class)]
    private ?WorkTypeEnum $workType = null;

    #[ORM\Column(type: 'string', length: 255, enumType: PlayingStyleEnum::class)]
    private ?PlayingStyleEnum $preferredPlayingStyle = null;

    #[ORM\Column(type: 'string', length: 255, enumType: GameTypeEnum::class)]
    private ?GameTypeEnum $favouriteGameType = null;

    #[ORM\Column]
    private ?float $computer_usage_per_day = null;

    #[ORM\Column]
    private ?float $gaming_per_day = null;

    use HistoryEntityTrait;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(User $user): self
    {
        $this->user = $user;

        return $this;
    }

    public function getAge(): ?AgeEnum
    {
        return $this->age;
    }

    public function setAge(AgeEnum $age): self
    {
        $this->age = $age;

        return $this;
    }

    public function getGender(): ?GenderEnum
    {
        return $this->gender;
    }

    public function setGender(GenderEnum $gender): self
    {
        $this->gender = $gender;

        return $this;
    }

    public function getWorkType(): ?WorkTypeEnum
    {
        return $this->workType;
    }

    public function setWorkType(WorkTypeEnum $workType): self
    {
        $this->workType = $workType;

        return $this;
    }

    public function getPreferredPlayingStyle(): ?PlayingStyleEnum
    {
        return $this->preferredPlayingStyle;
    }

    public function setPreferredPlayingStyle(PlayingStyleEnum $preferredPlayingStyle): self
    {
        $this->preferredPlayingStyle = $preferredPlayingStyle;

        return $this;
    }

    public function getFavouriteGameType(): ?GameTypeEnum
    {
        return $this->favouriteGameType;
    }

    public function setFavouriteGameType(GameTypeEnum $favouriteGameType): self
    {
        $this->favouriteGameType = $favouriteGameType;

        return $this;
    }

    public function getComputerUsagePerDay(): ?float
    {
        return $this->computer_usage_per_day;
    }

    public function setComputerUsagePerDay(float $computer_usage_per_day): self
    {
        $this->computer_usage_per_day = $computer_usage_per_day;

        return $this;
    }

    public function getGamingPerDay(): ?float
    {
        return $this->gaming_per_day;
    }

    public function setGamingPerDay(float $gaming_per_day): self
    {
        $this->gaming_per_day = $gaming_per_day;

        return $this;
    }
}
