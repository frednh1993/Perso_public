using System;


namespace ApiStripe.Models.Stripe
{
    public record AddStripeCustomer
    (
        string Email,

        string Name,

        AddStripeCard CreditCard
    );
    
}
