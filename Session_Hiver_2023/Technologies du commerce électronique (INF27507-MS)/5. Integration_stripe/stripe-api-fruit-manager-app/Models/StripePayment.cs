namespace stripe_api_fruit_manager_app.Models
{
    public class StripePayment
    {
        string? CustomerId { get; set; }

        string? PaymentId { get; set; }

        string? Description { get; set; }

        string? Currency { get; set; }

        long Amount { get; set; }

        string? ReceiptEmail { get; set; }


        public StripePayment(string _CustomerId, string _PaymentId, string _Description, string _Currency, long _Amount, string _ReceiptEmail)
        {
            this.CustomerId = _CustomerId;
            this.PaymentId = _PaymentId;
            this.Description = _Description;
            this.Currency = _Currency;
            this.Amount = _Amount;
            this.ReceiptEmail = _ReceiptEmail;
        }
    }
}
