using Microsoft.AspNetCore.Mvc;

namespace Recherche_livres.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            List<Models.PageInfo> pagesInfo = new List<Models.PageInfo>()
            {
                new Models.PageInfo(){ Title = "First title", PageNumber= 1 },
                new Models.PageInfo(){ Title = "Second title", PageNumber= 2 }
            };
            return View(pagesInfo);
        }
    }
}
