namespace ApiStripe.Models.Stripe
{
    public record StripeUpdatedCustomer
    (
            string Name,

            string Email,

            string CustomerId,

            string CartOwner,

            string CardNumber,

            string ExpirationYear,

            string ExpirationMonth,

            string Cvc
    );
}
