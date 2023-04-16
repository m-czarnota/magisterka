<?php

namespace App\Entity;

use App\Enum\Game\SquareStatusEnum;
use App\Repository\SquareRepository;
use Doctrine\ORM\Mapping as ORM;
use Ramsey\Uuid\Uuid;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity(repositoryClass: SquareRepository::class)]
class Square
{
    #[ORM\Id]
    #[ORM\Column(type: 'string')]
    private string $id;

    #[ORM\Column]
    #[Assert\GreaterThan(0, message: 'Size {{ value }} must be greater than {{ compared_value }}')]
    private ?int $size = null;

    #[ORM\Column]
    #[Assert\GreaterThan(0, message: 'Time to fall {{ value }} must be greater than {{ compared_value }}')]
    private ?float $timeToFall = null;

    #[ORM\Column(nullable: true)]
    #[Assert\NotBlank(allowNull: true)]
    #[Assert\GreaterThan(0, message: 'Time to click {{ value }} must be greater than {{ compared_value }}')]
    private ?float $timeToClick = null;

    #[ORM\Column]
    #[Assert\GreaterThanOrEqual(0, message: 'Time to click {{ value }} cannot be negative')]
    private ?float $score = null;

    #[ORM\Column(length: 255, enumType: SquareStatusEnum::class)]
    private SquareStatusEnum $status = SquareStatusEnum::NOT_FULLY_SPAWN;

    #[ORM\Column]
    #[Assert\GreaterThanOrEqual(0, message: 'Miss shots {{ value }} cannot be negative')]
    private int $missShots = 0;

    #[ORM\Column]
    #[Assert\NotBlank]
    private ?float $position = null;

    #[ORM\Column(length: 255)]
    #[Assert\NotBlank]
    private ?string $color = null;

    #[ORM\ManyToOne(inversedBy: 'squares')]
    #[ORM\JoinColumn(nullable: false)]
    #[Assert\NotBlank]
    private ?Game $Game = null;

    #[ORM\Column]
    #[Assert\GreaterThanOrEqual(0, message: 'Order ID in Game cannot be negative')]
    private ?int $orderIdInGame = null;

    public function __construct()
    {
        $this->id = Uuid::uuid7();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getSize(): ?int
    {
        return $this->size;
    }

    public function setSize(int $size): self
    {
        $this->size = $size;

        return $this;
    }

    public function getTimeToFall(): ?float
    {
        return $this->timeToFall;
    }

    public function setTimeToFall(float $timeToFall): self
    {
        $this->timeToFall = $timeToFall;

        return $this;
    }

    public function getTimeToClick(): ?float
    {
        return $this->timeToClick;
    }

    public function setTimeToClick(?float $timeToClick): self
    {
        $this->timeToClick = $timeToClick;

        return $this;
    }

    public function getScore(): ?float
    {
        return $this->score;
    }

    public function setScore(float $score): self
    {
        $this->score = $score;

        return $this;
    }

    public function getStatus(): SquareStatusEnum
    {
        return $this->status;
    }

    public function setStatus(SquareStatusEnum $status): self
    {
        $this->status = $status;

        return $this;
    }

    public function getMissShots(): ?int
    {
        return $this->missShots;
    }

    public function setMissShots(int $missShots): self
    {
        $this->missShots = $missShots;

        return $this;
    }

    public function getPosition(): ?float
    {
        return $this->position;
    }

    public function setPosition(float $position): self
    {
        $this->position = $position;

        return $this;
    }

    public function getColor(): ?string
    {
        return $this->color;
    }

    public function setColor(string $color): self
    {
        $this->color = $color;

        return $this;
    }

    public function getGame(): ?Game
    {
        return $this->Game;
    }

    public function setGame(?Game $Game): self
    {
        $this->Game = $Game;

        return $this;
    }

    public function getOrderIdInGame(): ?int
    {
        return $this->orderIdInGame;
    }

    public function setOrderIdInGame(int $orderIdInGame): self
    {
        $this->orderIdInGame = $orderIdInGame;

        return $this;
    }
}
