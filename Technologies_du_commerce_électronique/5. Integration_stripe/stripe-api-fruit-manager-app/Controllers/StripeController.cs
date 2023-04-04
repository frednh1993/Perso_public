using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Stripe;
using System.Net;
using stripe_api_fruit_manager_app.Models;




namespace stripe_api_fruit_manager_app.Controllers
{
    //[Produces("application/json")]
    // [controller] is a placeholder that will be replaced with the name of the controller class.
    [Route("api/[controller]")]
    [ApiController]
    public class StripeController : ControllerBase
    {
        // Stripe Api class to manage payments.
        private readonly ChargeService _chargeService;
        // Stripe Api class to manage customers.
        private readonly CustomerService _customerService;
        // Stripe Api class to manage token (card, customer, ...).
        private readonly TokenService _tokenService;

        public StripeController(ChargeService chargeService, CustomerService customerService, TokenService tokenService)
        {
            _chargeService = chargeService;
            _customerService = customerService;
            _tokenService = tokenService;
        }


       
        
        //public async Task<StripePayment> AddPaymentAsync(AddPayment newPayment, CancellationToken ct)
        //{
        //    // Set the new payment.
        //    ChargeCreateOptions paymentOptions = new ChargeCreateOptions
        //    {
        //        Customer = newPayment.CustomerId,
        //        Description = newPayment.Description,
        //        Currency = newPayment.Currency,
        //        Amount = newPayment.Amount,
        //        ReceiptEmail = newPayment.ReceiptEmail,
        //    };

        //    // Create the payment on Stripe.
        //    var createdPayment = await _chargeService.CreateAsync(paymentOptions, null, ct);

        //    // Return the payment to requesting method
        //    return new StripePayment(createdPayment.CustomerId, createdPayment.Id,createdPayment.Description,
        //                             createdPayment.Currency, createdPayment.Amount, createdPayment.ReceiptEmail);
        //}




        // Add a new Customer to Stripe.
        [HttpPost("customer/add")]
        public async Task<ActionResult<StripeCustomer>> AddCustomerAsync([FromBody] AddCustomer newCustomer, CancellationToken ct)
        {
            // Set Stripe Token attach to Customer(card).
            TokenCreateOptions tokenOptions = new TokenCreateOptions
            {
                Card = new TokenCardOptions
                {
                    Name = newCustomer.Name,
                    Number = newCustomer.CardNumber,
                    ExpYear = newCustomer.ExpirationYear,
                    ExpMonth = newCustomer.ExpirationMonth,
                    Cvc = newCustomer.Cvc
                }
            };

            // Create new Stripe Token attach to Customer(card).
            Token stripeToken = await _tokenService.CreateAsync(tokenOptions, null, ct);

            // Set a Customer.
            CustomerCreateOptions customerOptions = new CustomerCreateOptions
            {
                Name = newCustomer.Name,
                Email = newCustomer.Email,
                Source = stripeToken.Id
            };

            // Create new Customer in Stripe
            Customer createdCustomer = await _customerService.CreateAsync(customerOptions, null, ct);

            return StatusCode(StatusCodes.Status200OK, new StripeCustomer(createdCustomer.Id, createdCustomer.Name, createdCustomer.Email, createdCustomer.DefaultSourceId));
        }

    }
}
