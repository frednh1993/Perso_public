namespace stripe_api_fruit_manager_app.Models
{
    public class AddPayment
    {
        public string? CustomerId { get; set; }

        public string? PaymentId { get; set; }

        public string? Description { get; set; }

        public string? Currency { get; set; }

        public long Amount { get; set; }

        public string? ReceiptEmail { get; set; }
    }
}
