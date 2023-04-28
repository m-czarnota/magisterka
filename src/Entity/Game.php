<?php

namespace App\Entity;

use App\Repository\GameRepository;
use DateTime;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: GameRepository::class)]
class Game
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(inversedBy: 'games')]
    #[ORM\JoinColumn(nullable: false)]
    private ?User $user = null;

    #[ORM\Column(type: 'float')]
    private ?string $time = null;

    #[ORM\Column(nullable: true)]
    private ?string $data = null;

    #[ORM\Column(type: 'float')]
    private ?float $score = null;

    #[ORM\Column(type: 'datetime')]
    private DateTime $createdAt;

    #[ORM\OneToMany(mappedBy: 'game', targetEntity: Square::class)]
    private Collection $squares;

    #[ORM\Column(type: 'float', nullable: true)]
    private ?float $timeToNewScoreRecord = null;

    #[ORM\Column(type: 'float', nullable: true)]
    private ?float $timeToNewTimeRecord = null;

    public function __construct()
    {
        $this->createdAt = new DateTime();
        $this->squares = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(?User $user): self
    {
        $this->user = $user;

        return $this;
    }

    public function getTime(): ?string
    {
        return $this->time;
    }

    public function setTime(string $time): self
    {
        $this->time = $time;

        return $this;
    }

    public function getData(): ?string
    {
        return $this->data;
    }

    public function setData(?string $data): self
    {
        $this->data = $data;

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

    public function getCreatedAt(): DateTime
    {
        return $this->createdAt;
    }

    public function setCreatedAt(DateTime $createdAt): self
    {
        $this->createdAt = $createdAt;

        return $this;
    }

    /**
     * @return Collection<int, Square>
     */
    public function getSquares(): Collection
    {
        return $this->squares;
    }

    public function addSquare(Square $square): self
    {
        if (!$this->squares->contains($square)) {
            $this->squares->add($square);
            $square->setGame($this);
        }

        return $this;
    }

    public function removeSquare(Square $square): self
    {
        if ($this->squares->removeElement($square)) {
            // set the owning side to null (unless already changed)
            if ($square->getGame() === $this) {
                $square->setGame(null);
            }
        }

        return $this;
    }

    public function getTimeToNewScoreRecord(): ?float
    {
        return $this->timeToNewScoreRecord;
    }

    public function setTimeToNewScoreRecord(?float $timeToNewScoreRecord): self
    {
        $this->timeToNewScoreRecord = $timeToNewScoreRecord;

        return $this;
    }

    public function getTimeToNewTimeRecord(): ?float
    {
        return $this->timeToNewTimeRecord;
    }

    public function setTimeToNewTimeRecord(?float $timeToNewTimeRecord): self
    {
        $this->timeToNewTimeRecord = $timeToNewTimeRecord;

        return $this;
    }
}
