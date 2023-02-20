//--- Utiliser le design pattern MVC ---
using Microsoft.AspNetCore.Mvc;

namespace Recherche_livres.Controllers
{
    public class HomeController : Controller
    {
        //--- Route Index ---
        public IActionResult Index()
        {
            //List<Models.PageInfo> pagesInfo = new List<Models.PageInfo>()
            //{
            //    new Models.PageInfo(){ Title = "First title", PageNumber= 1 },
            //    new Models.PageInfo(){ Title = "Second title", PageNumber= 2 }
            //};

            Models.PageInfo searchPage = new Models.PageInfo() { Title = "Recherche test Fred" };
            return View(searchPage);
        }
    }
}
