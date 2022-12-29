<?php

namespace App\Interface;

interface RepositoryModifierInterface
{
    public function save(Object $entity, bool $flash = false): self;
    public function remove(Object $entity, bool $flash = false): self;
    public function saveMultiple(array $entities, bool $flash = false): self;
    public function removeMultiple(array $entities, bool $flash = false): self;
}