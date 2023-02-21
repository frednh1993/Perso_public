using Microsoft.AspNetCore.Mvc;
using Books.Models;
using Microsoft.AspNetCore.Mvc.TagHelpers;

namespace Books.Controllers
{
    public class SearchBookController : Controller
    {
        // Persistance de donnees temporaire
        List<Book> books = new List<Book>()
        {
            new Book(){Title="Han d'Islande", Author="Victor Hugo", Editor="Plume de Carotte"},
            new Book(){Title="Le dernier Jour d'un Condamné", Author="Victor Hugo", Editor="Arvensa"},
            new Book(){Title="Le Silmarillon", Author="J.R.R. Tolkien", Editor="Bourgois"},
            new Book(){Title="Le Seigneur des anneaux : Les Deux Tours", Author="J.R.R. Tolkien", Editor="Bourgois"},
            new Book(){Title="Le Seigneur des anneaux : Le Retour du roi", Author="J.R.R. Tolkien", Editor="Bourgois"},
            new Book(){Title="Le Portrait de Dorian Gray", Author="Oscar Wilde", Editor="Le livre qui parle"}
        };
        

        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public IActionResult Search()
        {
            Book book = new Book();
            return View(book);
        }

        [HttpPost]
        public IActionResult Result(Book _book)
        {
            List<Book> results = books;

            if (_book.Title != null || _book.Author != null || _book.Editor != null)
            {
                if (_book.Title != null)
                {
                    results = results.Where(r => r.Title == _book.Title).ToList();
                }
                if (_book.Author != null)
                {
                    results = results.Where(r => r.Author == _book.Author).ToList();
                }
                if (_book.Editor != null)
                {
                    results = results.Where(r => r.Editor == _book.Editor).ToList();
                }
            }
            else 
            {
                results.Clear();
            }
            
            return View(results);
        }

        [HttpGet]
        public IActionResult Result(List<Book> liste)
        {
            return View(liste);
        }

    }
}
