using Microsoft.EntityFrameworkCore;
using Books.Models;
using System.Reflection.Metadata;



namespace Books
{
    public class BooksContext : DbContext
    {
        public DbSet<Models.User> Users { get; set; }
        public DbSet<Models.Book> Books { get; set; }


        protected override void OnConfiguring(DbContextOptionsBuilder dbContextOptionsBuilder)
        {
            dbContextOptionsBuilder.UseSqlServer(@"Server=(localdb)\MSSQLLocalDB;Initial Catalog = master; Integrated Security = True; Connect Timeout = 30; Encrypt=False;TrustServerCertificate=False;ApplicationIntent=ReadWrite;MultiSubnetFailover=False;Database=bookDb;Trusted_Connection=True;");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Models.User>().HasData(
                new Models.User() { Id = 1, Name="Frederik Boutin" }
                );

            modelBuilder.Entity<Models.Book>().HasData(
                new Models.Book() {Id=1, Title = "Han d'Islande", Author = "Victor Hugo", Editor = "Plume de Carotte", UserId=1},
                new Models.Book() {Id = 2, Title = "Le dernier Jour d'un Condamné", Author = "Victor Hugo", Editor = "Arvensa", UserId = 1 },
                new Models.Book() {Id = 3, Title = "Le Silmarillon", Author = "J.R.R. Tolkien", Editor = "Bourgois", UserId = 1 },
                new Models.Book() {Id = 4, Title = "Le Seigneur des anneaux : Les Deux Tours", Author = "J.R.R. Tolkien", Editor = "Bourgois", UserId = 1 },
                new Models.Book() {Id = 5, Title = "Le Seigneur des anneaux : Le Retour du roi", Author = "J.R.R. Tolkien", Editor = "Bourgois", UserId = 1 },
                new Models.Book() {Id = 6, Title = "Le Portrait de Dorian Gray", Author = "Oscar Wilde", Editor = "Le livre qui parle", UserId = 1 }
                );
        }
    }
}
