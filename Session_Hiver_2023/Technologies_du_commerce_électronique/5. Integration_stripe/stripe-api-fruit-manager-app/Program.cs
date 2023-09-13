using stripe_api_fruit_manager_app;




// WebApplication := Use to configure HTTP pipeline (series of middleware
// components that handle incoming HTTP requests and outgoing HTTP responses
// in a web application) and the routes.
var builder = WebApplication.CreateBuilder(args);

// Add services (refers to a set of related functionality that can be accessed
// programmatically by other applications or services) to the project.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Add Stripe Infrastructure to enable the import of Stripe services.
builder.Services.AddStripeInfrastructure(builder.Configuration);

var app = builder.Build();

// Use Swagger if the api is in development mode.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}


// Add methods for using in the api.
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();


