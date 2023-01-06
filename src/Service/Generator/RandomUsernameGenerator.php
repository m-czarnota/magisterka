<?php

namespace App\Service\Generator;

use App\Interface\Generator\RandomNameGeneratorInterface;
use App\Interface\Transformer\StringTransformerInterface;
use App\Repository\UserRepository;
use Doctrine\ORM\NonUniqueResultException;
use SplFileObject;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;

class RandomNameGenerator implements RandomNameGeneratorInterface
{
    private StringTransformerInterface $wordSimplifier;
    private UserRepository $userRepository;

    readonly private string $wordsDirPath;
    readonly public string $nounsPath;
    readonly public string $adjectivesPath;

    public function __construct(StringTransformerInterface $wordSimplifier, UserRepository $userRepository, ParameterBagInterface $parameterBag)
    {
        $this->wordSimplifier = $wordSimplifier;
        $this->userRepository = $userRepository;

        $this->wordsDirPath = $parameterBag->get('kernel.project_dir') . '/words';
        $this->nounsPath = $this->wordsDirPath . '/nouns.txt';
        $this->adjectivesPath = $this->wordsDirPath . '/adjectives.txt';
    }

    /**
     * @throws NonUniqueResultException
     */
    public function generateRandomName(): string
    {
        do {
            $noun = $this->readRandomWord(new SplFileObject($this->nounsPath));
            $adjective = $this->readRandomWord(new SplFileObject($this->adjectivesPath));

            $capitalisedWords = array_map(fn(string $word) => ucfirst(mb_strtolower($word)), [$noun, $adjective]);
            $username = implode('', $capitalisedWords);

            $user = $this->userRepository->findOneByUsername($username);
        } while ($user !== null);

        return $username;
    }

    private function readRandomWord(SplFileObject $fileObject): string
    {
        $fileObject->seek(PHP_INT_MAX);
        $linesCount = $fileObject->key();

        $fileObject->seek(rand(0, $linesCount));

        return $this->wordSimplifier->transform($fileObject->fgets());
    }
}