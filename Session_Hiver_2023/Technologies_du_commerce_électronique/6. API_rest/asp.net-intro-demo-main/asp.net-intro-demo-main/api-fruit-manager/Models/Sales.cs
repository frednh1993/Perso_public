namespace api_fruit_manager.Models
{
    public class Sales
    {
        // API database attributes.
        public int SaleId { get; set; }


        // Stripe attributes.
        public int? StripeSaleId { get; set; }


        // Table relation (1 sale have 1 product, 1 user / 1 product can be in * sales /
        // 1 user can be in * sales).
        public int UserId { get; set; }
        public Users User { get; set; }

        public int ProductId { get; set; }
        public Products Product { get; set; }
    }
}
