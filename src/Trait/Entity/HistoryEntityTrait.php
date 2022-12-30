<?php

namespace App\Trait\Entity;

use App\Entity\User;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Security\Core\User\UserInterface;
use Symfony\Component\Validator\Constraints as Assert;

trait HistoryEntityTrait
{
    #[ORM\Column(type: 'integer')]
    #[Assert\NotBlank]
    #[Assert\Type('integer')]
    protected ?int $createdBy = null;

    #[ORM\Column(type: 'datetime')]
    #[Assert\NotBlank]
    #[Assert\DateTime]
    protected ?DateTime $createdAt = null;

    #[ORM\Column(type: 'integer', nullable: true)]
    #[Assert\NotBlank(allowNull: true)]
    #[Assert\Type('integer')]
    protected ?int $modifiedBy = null;

    #[ORM\Column(type: 'datetime', nullable: true)]
    #[Assert\NotBlank(allowNull: true)]
    #[Assert\Type('datetime')]
    protected ?DateTime $modifiedAt = null;

    #[ORM\Column(type: 'boolean')]
    #[Assert\NotBlank]
    #[Assert\Type('bool')]
    protected ?bool $isDeleted = null;

    public function getCreatedBy(): ?int
    {
        return $this->createdBy;
    }

    public function setCreatedBy(int $createdBy): self
    {
        $this->createdBy = $createdBy;

        return $this;
    }

    public function getCreatedAt(): ?DateTime
    {
        return $this->createdAt;
    }

    public function setCreatedAt(?DateTime $createdAt): self
    {
        $this->createdAt = $createdAt;

        return $this;
    }

    public function getModifiedBy(): ?int
    {
        return $this->modifiedBy;
    }

    public function setModifiedBy(?int $modifiedBy): self
    {
        $this->modifiedBy = $modifiedBy;

        return $this;
    }

    public function getModifiedAt(): ?DateTime
    {
        return $this->modifiedAt;
    }

    public function setModifiedAt(?DateTime $modifiedAt): self
    {
        $this->modifiedAt = $modifiedAt;

        return $this;
    }

    public function getIsDeleted(): ?bool
    {
        return $this->isDeleted;
    }

    public function setIsDeleted(bool $isDeleted): self
    {
        $this->isDeleted = $isDeleted;

        return $this;
    }

    public function touch(): self
    {
        $date = new DateTime();
        $this->setModifiedAt($date);

        return $this;
    }

    public function init(User|UserInterface $user): self
    {
        $date = new DateTime();
        $this->setCreatedBy($user->getId());
        $this->setCreatedAt($date);
        $this->setIsDeleted(false);

        return $this;
    }
}