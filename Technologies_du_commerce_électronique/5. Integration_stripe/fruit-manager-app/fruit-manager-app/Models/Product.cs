using System.ComponentModel.DataAnnotations;


namespace DemoAspNet.Models
{
    public class Product
    {  
        public int? StripeId { get; set; }


        [Required(ErrorMessage = "Champs requis !")]
        public string? Title { get; set; }


        [Required(ErrorMessage = "Champs requis !")]
        public float? Price { get; set; }


        [Required(ErrorMessage = "Champs requis !")]
        public string? Description { get; set; }


        [Required(ErrorMessage = "Champs requis !")]
        public string? Country { get; set; }
    }
}
