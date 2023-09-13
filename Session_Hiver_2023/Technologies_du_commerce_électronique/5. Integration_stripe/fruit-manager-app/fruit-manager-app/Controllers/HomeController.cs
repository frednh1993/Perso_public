using Microsoft.AspNetCore.Mvc;




namespace DemoAspNet.Controllers
{
    public class HomeController : Controller
    {       
        // Page Produits pour les achats.
        public IActionResult Index()
        {
            ViewBag.Title = "Page des produits";

            List<Models.Product> products = new List<Models.Product>() {
                new Models.Product{ Title="Avocat", Country="Mexique", Description="L'avocat est le fruit de l'avocatier, un arbre de la famille des Lauraceae, originaire du Mexique. Il en existe trois grandes variétés. La variété la plus populaire est l'avocat Hass." },
                new Models.Product{ Title="Banane", Country="Brésil", Description="La banane est le fruit ou la baie dérivant de l’inflorescence du bananier. Les bananes sont des fruits très généralement stériles issus de variétés domestiquées." },
                new Models.Product{ Title="Kiwi", Country="Chine", Description="Les kiwis sont des fruits de plusieurs espèces de lianes du genre Actinidia, famille des Actinidiaceae. Ils sont originaires de Chine, notamment de la province de Shaanxi." }
            };

            return View(products);
        }


        // Page Ajouts pour creer des produits.
        [HttpGet]
        public IActionResult AddProduct()
        {
            ViewBag.Title = "Ajouter un produit";
            return View();
        }
        [HttpPost]
        public IActionResult AddProduct(Models.Product product)
        {
            ViewBag.Title = "Ajouter un produit";

            if (ModelState.IsValid)
                return RedirectToAction("Result", product);

            return View();
        }


        // Page Result pour confirmer la creation d'un produit.
        [HttpGet]
        public IActionResult Result(Models.Product _product)
        {
            ViewBag.Title = "Page du produit ajouté";
            return View(_product);
        }
    }
}
