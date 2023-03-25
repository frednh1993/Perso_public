using Microsoft.AspNetCore.Mvc;

namespace DemoAspNet.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            ViewBag.Title = "Page des prix";
            return View();
        }

        public IActionResult Contact()
        {
            ViewBag.Title = "Page de contact";
            return View();
        }
    }
}
