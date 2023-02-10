<?php

declare(strict_types=1);

namespace App\Form\Type;

use App\Entity\InitialSurvey;
use App\Enum\InitialSurvey\AgeEnum;
use App\Enum\InitialSurvey\GameTypeEnum;
use App\Enum\InitialSurvey\GenderEnum;
use App\Enum\InitialSurvey\PlayingStyleEnum;
use App\Enum\InitialSurvey\WorkTypeEnum;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\EnumType;
use Symfony\Component\Form\Extension\Core\Type\NumberType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Contracts\Translation\TranslatorInterface;

class NewInitialSurveyType extends AbstractType
{
    public function __construct(
        protected TranslatorInterface $translator,
    ) {}

    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('age', EnumType::class, [
                'class' => AgeEnum::class,
                'choice_label' => fn(AgeEnum $age) => $age->value,
            ])
            ->add('gender', EnumType::class, [
                'class' => GenderEnum::class,
                'choice_label' => fn(GenderEnum $gender) => $gender->getTransKey(),
            ])
            ->add('workType', EnumType::class, [
                'class' => WorkTypeEnum::class,
                'choice_label' => fn(WorkTypeEnum $workType) => $workType->getTransKey(),
            ])
            ->add('preferredPlayingStyle', EnumType::class, [
                'class' => PlayingStyleEnum::class,
                'choice_label' => fn(PlayingStyleEnum $playingStyle) => $playingStyle->getTransKey(),
            ])
            ->add('favouriteGameType', EnumType::class, [
                'class' => GameTypeEnum::class,
                'choice_label' => function (GameTypeEnum $gameType) {
                    $gameTypeTrans = $this->translator->trans($gameType->getTransKey());
                    $gameExamples = implode(', ', $gameType->getExamplesGames());

                    return "$gameTypeTrans ($gameExamples)";
                },
            ])
            ->add('computerUsagePerDay', NumberType::class, [
                'html5' => true,
                'attr' => [
                    'min' => 0,
                    'max' => 24,
                ],
            ])
            ->add('gamingPerDay', NumberType::class, [
                'html5' => true,
                'attr' => [
                    'min' => 0,
                    'max' => 24,
                ],
            ])
            ->add('submit', SubmitType::class);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => InitialSurvey::class,
        ]);
    }
}