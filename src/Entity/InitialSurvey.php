<?php

declare(strict_types=1);

namespace App\Entity;

use App\Enum\InitialSurvey\AgeEnum;
use App\Enum\InitialSurvey\GameTypeEnum;
use App\Enum\InitialSurvey\GenderEnum;
use App\Enum\InitialSurvey\PlayingStyleEnum;
use App\Enum\InitialSurvey\WorkTypeEnum;
use App\Repository\InitialSurveyRepository;
use DateTime;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;
use App\Validator as AppAssert;

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
    #[AppAssert\Enum(path: AgeEnum::class)]
    private ?AgeEnum $age = null;

    #[ORM\Column(type: 'string', length: 255, enumType: GenderEnum::class)]
    #[AppAssert\Enum(path: GenderEnum::class)]
    private ?GenderEnum $gender = null;

    #[ORM\Column(type: 'string', length: 255, enumType: WorkTypeEnum::class)]
    #[AppAssert\Enum(path: WorkTypeEnum::class)]
    private ?WorkTypeEnum $workType = null;

    #[ORM\Column(type: 'string', length: 255, enumType: PlayingStyleEnum::class)]
    #[AppAssert\Enum(path: PlayingStyleEnum::class)]
    private ?PlayingStyleEnum $preferredPlayingStyle = null;

    #[ORM\Column(type: 'string', length: 255, enumType: GameTypeEnum::class)]
    #[AppAssert\Enum(path: GameTypeEnum::class)]
    private ?GameTypeEnum $favouriteGameType = null;

    #[ORM\Column(type: 'float')]
    #[Assert\NotBlank]
    #[Assert\Type(type: 'float')]
    #[Assert\GreaterThanOrEqual(value: 0)]
    #[Assert\LessThanOrEqual(value: 24)]
    private ?float $computerUsagePerDay = null;

    #[ORM\Column(type: 'float')]
    #[Assert\NotBlank]
    #[Assert\Type(type: 'float')]
    #[Assert\GreaterThanOrEqual(value: 0)]
    #[Assert\LessThanOrEqual(value: 24)]
    private ?float $gamingPerDay = null;

    #[ORM\Column(type: 'datetime')]
    private DateTime $createdAt;

    public function __construct()
    {
        $this->createdAt = new DateTime();
    }

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
        return $this->computerUsagePerDay;
    }

    public function setComputerUsagePerDay(float $computerUsagePerDay): self
    {
        $this->computerUsagePerDay = $computerUsagePerDay;

        return $this;
    }

    public function getGamingPerDay(): ?float
    {
        return $this->gamingPerDay;
    }

    public function setGamingPerDay(float $gamingPerDay): self
    {
        $this->gamingPerDay = $gamingPerDay;

        return $this;
    }

    public function getCreatedAt(): DateTime
    {
        return $this->createdAt;
    }

    public function setCreatedAt(DateTime $createdAt): self
    {
        $this->createdAt = $createdAt;

        return $this;
    }
}
