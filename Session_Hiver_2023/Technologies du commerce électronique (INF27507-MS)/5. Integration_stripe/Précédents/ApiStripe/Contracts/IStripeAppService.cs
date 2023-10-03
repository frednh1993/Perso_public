using System;
using ApiStripe.Models.Stripe;


namespace ApiStripe.Contracts
{
    public interface IStripeAppService
    {
        Task<StripeCustomer> AddStripeCustomerAsync(AddStripeCustomer customer, CancellationToken ct);
        Task<StripePayment> AddStripePaymentAsync(AddStripePayment payment, CancellationToken ct);

        Task<StripeUpdatedCustomer> UpdateStripeCustomerAsync(UpdateStripeCustomer customer, CancellationToken ct);
    }
}
