using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Books.Migrations
{
    public partial class Creation_base_donnees : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Books",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Title = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Author = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Editor = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Image = table.Column<string>(type: "nvarchar(max)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Books", x => x.Id);
                });

            migrationBuilder.InsertData(
                table: "Books",
                columns: new[] { "Id", "Author", "Editor", "Image", "Title" },
                values: new object[,]
                {
                    { 1, "Victor Hugo", "Plume de Carotte", null, "Han d'Islande" },
                    { 2, "Victor Hugo", "Arvensa", null, "Le dernier Jour d'un Condamné" },
                    { 3, "J.R.R. Tolkien", "Bourgois", null, "Le Silmarillon" },
                    { 4, "J.R.R. Tolkien", "Bourgois", null, "Le Seigneur des anneaux : Les Deux Tours" },
                    { 5, "J.R.R. Tolkien", "Bourgois", null, "Le Seigneur des anneaux : Le Retour du roi" },
                    { 6, "Oscar Wilde", "Le livre qui parle", null, "Le Portrait de Dorian Gray" }
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Books");
        }
    }
}
