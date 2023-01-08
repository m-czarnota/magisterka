<?php

namespace App\Interface\Factory\Form;

use App\Interface\Factory\BaseFactoryInterface;
use Symfony\Component\Form\FormInterface;

interface FormFactoryInterface extends BaseFactoryInterface
{
    public function create(): FormInterface;
}