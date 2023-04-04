namespace stripe_api_fruit_manager_app.Models
{
    public class AddCustomer
    {
        public string? Name { get; set; }

        public string? Email { get; set; }

        public string? CardOwner { get; set; }

        public string? CardNumber { get; set; }

        public string? ExpirationYear { get; set; }

        public string? ExpirationMonth { get; set; }

        public string? Cvc { get; set; }
    }
}
