<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
// use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

// First return
// class MoviesController extends AbstractController
// {
//     #[Route('/movies/{name}', name: 'app_movies', defaults: ['name' => null], methods:['GET', 'HEAD'])]
//     public function index($name): JsonResponse
//     {
//         return $this->json([
//             'message' => $name,
//             'path' => 'src/Controller/MoviesController.php',
//         ]);
//     }
// }

// Second return
// class MoviesController extends AbstractController
// {
//     #[Route('/movies', name: 'app_movies')]
//     public function index(): Response
//     {
//         // return $this->render('index.html.twig', [
//         //     'title' => 'Avengers: Endgame'
//         // ]);

//         return $this->render('index.html.twig', [
//             'title' => 'Test123'
//         ]);
//     }
// }

// Third return
class MoviesController extends AbstractController
{
    #[Route('/movies', name: 'app_movies')]
    public function index(): Response
    {
        $movies = ["Avengers: Endgame", "Inception", "Loki", "Black Widow"];
        
        return $this->render('index2.html.twig', array(
            'movies' => $movies
        ));

    }
}
