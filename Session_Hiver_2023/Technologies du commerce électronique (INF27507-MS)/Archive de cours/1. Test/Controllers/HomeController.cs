using Microsoft.AspNetCore.Mvc;

namespace Test.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
