using Microsoft.EntityFrameworkCore;
using GradeManagement.Models;


namespace GradeManagement
{
    public class GradeManagementContext : DbContext
    {
        public DbSet<Models.Student> Students { get; set; }
        public DbSet<Models.Course> Courses { get; set; }
        public DbSet<Models.Transcript> Transcripts { get; set; }


        protected override void OnConfiguring(DbContextOptionsBuilder dbContextOptionsBuilder)
        {
            dbContextOptionsBuilder.UseSqlServer(@"Server=(localdb)\MSSQLLocalDB;Initial Catalog = master; Integrated Security = True; Connect Timeout = 30; Encrypt=False;TrustServerCertificate=False;ApplicationIntent=ReadWrite;MultiSubnetFailover=False;Database=gradeManagementDb;Trusted_Connection=True;");
        }


        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {

        }
    }
}
