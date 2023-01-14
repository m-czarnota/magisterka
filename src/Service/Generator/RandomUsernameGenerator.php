<?php

namespace App\Service\Generator;

use App\Interface\Generator\RandomUsernameGeneratorInterface;
use App\Interface\Transformer\StringTransformerInterface;
use App\Repository\UserRepository;
use Doctrine\ORM\NonUniqueResultException;
use Exception;
use SplFileObject;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\String\ByteString;

class RandomUsernameGenerator implements RandomUsernameGeneratorInterface
{
    protected const MIN_GENERATOR_NUMBER = 10;
    protected const MAX_GENERATOR_NUMBER = 9999;

    protected StringTransformerInterface $wordSimplifier;
    protected UserRepository $userRepository;

    readonly protected string $wordsDirPath;
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
     * @throws Exception
     */
    public function generateRandomName(): string
    {
        do {
            $noun = $this->readRandomWord(new SplFileObject($this->nounsPath));
            $adjective = $this->readRandomWord(new SplFileObject($this->adjectivesPath));

            $capitalisedWords = array_map(fn(string $word) => ucfirst(mb_strtolower($word)), [$noun, $adjective]);
            $username = implode('', $capitalisedWords) . random_int(self::MIN_GENERATOR_NUMBER, self::MAX_GENERATOR_NUMBER);

            $user = $this->userRepository->findOneByUsername($username);
        } while ($user !== null);

        return $username;
    }

    protected function readRandomWord(SplFileObject $fileObject): string
    {
        $fileObject->seek(PHP_INT_MAX);
        $linesCount = $fileObject->key();

        $fileObject->seek(rand(0, $linesCount));

        return $this->wordSimplifier->transform($fileObject->fgets());
    }
}