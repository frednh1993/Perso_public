using System;


namespace ApiStripe.Models.Stripe
{
    public record UpdateStripeCustomer
    (
        string CustomerId,

        string Email,

        string Name,

        AddStripeCard CreditCard
    );
}


