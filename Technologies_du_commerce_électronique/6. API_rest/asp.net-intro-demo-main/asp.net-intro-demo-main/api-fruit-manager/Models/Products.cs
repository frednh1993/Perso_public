namespace api_fruit_manager.Models
{
    public class Products
    {
        // API database attributes.
        public int ProductId { get; set; }

        public string Title { get; set; }

        public string? Description { get; set; }

        public string? Country { get; set; }

        public float Price { get; set; }


        // Stripe attributes.
        public int? StripeProductId { get; set;}

        public int? StripePriceId { get; set; }


        // Table relation (1 user have * products / 1 product belong to 1 user).
        public int UserId { get; set; }
        public Users User { get; set; }

        public ICollection<Sales>? Sales { get; set; }
    }
}
