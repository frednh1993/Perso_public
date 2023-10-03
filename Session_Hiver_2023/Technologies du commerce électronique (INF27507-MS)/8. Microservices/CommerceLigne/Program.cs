using Microsoft.Extensions.Options;
using MMLib.SwaggerForOcelot.DependencyInjection;
using Ocelot.DependencyInjection;
using Ocelot.Middleware;



// builder (class WebApplication) := The web application use to configure HTTP pipeline and routes.
var builder = WebApplication.CreateBuilder(args);

// app := the web application builded
var app = builder.Build();

// routes := Le fichier de configuration des routes.
var routes = "Routes";
builder.Configuration.AddOcelotWithSwaggerSupport(options =>
{
    options.Folder = routes;
});

// Use the services AddOcelot () and AddSwaggerForOcelot ()
builder.Services.AddOcelot(builder.Configuration);
builder.Services.AddSwaggerForOcelot(builder.Configuration);

app.UseSwaggerForOcelotUI(options =>
{
    options.PathToSwaggerGenerator = "/swagger/docs";
});

app.UseOcelot().Wait();

