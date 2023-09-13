var builder = WebApplication.CreateBuilder(args);
builder.Services.AddMvc(option => option.EnableEndpointRouting = false);


var app = builder.Build();
// Permet d'utiliser les librairies 
app.UseFileServer();
app.UseMvc(routes => routes.MapRoute("Default", "{controller=SearchBook}/{action=Search}"));
app.Run();
