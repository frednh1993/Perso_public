using Stripe;
using stripe_api_fruit_manager_app.Controllers;




namespace stripe_api_fruit_manager_app
{
    public static class StripeInfrastructure
    {
        public static IServiceCollection AddStripeInfrastructure(this IServiceCollection services, IConfiguration configuration)
        {
            // Stripe Api registration to my account(seller).
            StripeConfiguration.ApiKey = configuration.GetValue<string>("Stripe:SecretKey");

            // Inject the needed Stripe services in the StripeController.
            return services
                .AddScoped<CustomerService>()
                .AddScoped<ChargeService>()
                .AddScoped<TokenService>()
                .AddScoped<StripeController>();
        }
    }
}
