<?php

namespace App\Security\Authenticator;

use App\Repository\UserRepository;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Exception\CustomUserMessageAuthenticationException;
use Symfony\Component\Security\Http\Authenticator\AbstractLoginFormAuthenticator;
use Symfony\Component\Security\Http\Authenticator\Passport\Badge\RememberMeBadge;
use Symfony\Component\Security\Http\Authenticator\Passport\Badge\UserBadge;
use Symfony\Component\Security\Http\Authenticator\Passport\Credentials\PasswordCredentials;
use Symfony\Component\Security\Http\Authenticator\Passport\Passport;
use Symfony\Component\Security\Http\Authenticator\Passport\SelfValidatingPassport;
use Symfony\Component\Security\Http\SecurityRequestAttributes;
use Symfony\Component\Security\Http\Util\TargetPathTrait;

class PasswordlessAuthenticator extends AbstractLoginFormAuthenticator
{
    use TargetPathTrait;

    public const LOGIN_ROUTE = 'app_login';

    public function __construct(
        protected UserRepository $userRepository,
        protected UrlGeneratorInterface $urlGenerator,
    ) {}

    public function authenticate(Request $request): Passport
    {
        $username = $request->request->get('username', '');
        $request->getSession()->set(SecurityRequestAttributes::LAST_USERNAME, $username);

        $userBadge = new UserBadge($username, function (string $userIdentifier) {
            $user = $this->userRepository->findOneByUsername($userIdentifier);

            if ($user) {
                return $user;
            }

            throw new CustomUserMessageAuthenticationException('Invalid credentials');
        });

//        return new SelfValidatingPassport($userBadge, [new RememberMeBadge()]);

        if ($userBadge->getUser()->getPassword() === null) {
            return new SelfValidatingPassport($userBadge, [new RememberMeBadge()]);
        }

        $password = $request->request->get('password', '');
        $credentials = new PasswordCredentials($password);

        return new Passport($userBadge, $credentials, [new RememberMeBadge()]);
    }

    protected function getLoginUrl(Request $request): string
    {
        return $this->urlGenerator->generate(self::LOGIN_ROUTE);
    }

    public function onAuthenticationSuccess(Request $request, TokenInterface $token, string $firewallName): ?Response
    {
        return new RedirectResponse($this->urlGenerator->generate('app_user_dashboard'));
    }

    public function supports(Request $request): bool
    {
        return self::LOGIN_ROUTE === $request->attributes->get('_route') && $request->isMethod('POST');
    }
}