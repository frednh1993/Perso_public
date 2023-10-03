using Stripe;
using System.Xml.Linq;




namespace stripe_api_fruit_manager_app.Models
{
    public record StripeCustomer
    (
        string CustomerId,

        string Name,

        string Email,

        string CreditCardId   
    );
}
