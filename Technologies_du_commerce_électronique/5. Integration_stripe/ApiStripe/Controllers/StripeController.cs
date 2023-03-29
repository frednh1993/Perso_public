using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using ApiStripe.Contracts;
using ApiStripe.Models.Stripe;


namespace ApiStripe.Controllers
{
    [Route("api/[controller]")]
    public class StripeController : Controller
    {
        private readonly IStripeAppService _stripeService;


        // Constructor.
        public StripeController(IStripeAppService stripeService)
        {
            _stripeService = stripeService;
        }


        // Add Customer.
        [HttpPost("customer/add")]
        public async Task<ActionResult<StripeCustomer>> AddStripeCustomer(
            [FromBody] AddStripeCustomer customer,
            CancellationToken ct)
        {
            StripeCustomer createdCustomer = await _stripeService.AddStripeCustomerAsync(
                customer,
                ct);

            return StatusCode(StatusCodes.Status200OK, createdCustomer);
        }


        // Update Customer.
        [HttpPatch("customer/update")]
        public async Task<ActionResult<StripeUpdatedCustomer>> UpdateStripeCustomer(
            [FromBody] UpdateStripeCustomer customer,
            CancellationToken ct)
        {
            StripeUpdatedCustomer updatedCustomer = await _stripeService.UpdateStripeCustomerAsync(customer, ct);
                
            return StatusCode(StatusCodes.Status200OK, updatedCustomer);
        }


        // Add Product.
        [HttpPost("payment/add")]
        public async Task<ActionResult<StripePayment>> AddStripePayment(
            [FromBody] AddStripePayment payment,
            CancellationToken ct)
        {
            StripePayment createdPayment = await _stripeService.AddStripePaymentAsync(
                payment,
                ct);

            return StatusCode(StatusCodes.Status200OK, createdPayment);
        }
    }
}
