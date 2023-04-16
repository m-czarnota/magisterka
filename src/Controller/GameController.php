<?php

namespace App\Controller;

use App\Entity\User;
use App\Security\Exception\ValidationException;
use App\Service\Controller\Game\GameService;
use Doctrine\ORM\EntityManagerInterface;
use Exception;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/game')]
class GameController extends AbstractController
{
    public function __construct(
        private readonly GameService $service,
        private readonly EntityManagerInterface $entityManager,
    ) {
    }

    #[Route('/', name: 'app_game_index')]
    public function game(): Response
    {
        return $this->render('page/game/game.html.twig');
    }

    /**
     * @throws Exception
     */
    #[Route('/save-game-data', name: 'app_game_save_game_data', options: ['expose' => true], methods: Request::METHOD_POST)]
    public function saveGameData(Request $request): JsonResponse
    {
        /** @var User $user */
        $user = $this->getUser();
        $data = json_decode($request->getContent(), true);

        try {
            $game = $this->service->saveGameData(
                $data['gameData'] ?? [],
                $data['squares'] ?? [],
                $user
            );
        } catch (ValidationException $exception) {
            return $this->json(['status' => 'error', 'message' => $exception->getMessage()], Response::HTTP_CONFLICT);
        }

        $this->entityManager->flush();

        return $this->json(['status' => 'ok', 'game' => $game->getId()]);
    }
}