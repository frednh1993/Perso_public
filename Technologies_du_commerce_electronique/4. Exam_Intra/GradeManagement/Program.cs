var builder = WebApplication.CreateBuilder(args);
// To use MVC.
builder.Services.AddMvc(option => option.EnableEndpointRouting = false);
var app = builder.Build();
// To use client libraries.
app.UseFileServer();


app.UseMvc(routes => routes.MapRoute("Default", "{controller=Home}/{action=Index}"));
app.Run();





