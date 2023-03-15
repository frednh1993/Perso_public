using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Books.Migrations
{
    public partial class Creation : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Users",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Users", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Books",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Title = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Author = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Editor = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Image = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    UserId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Books", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Books_Users_UserId",
                        column: x => x.UserId,
                        principalTable: "Users",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.InsertData(
                table: "Users",
                columns: new[] { "Id", "Name" },
                values: new object[] { 1, "Frederik Boutin" });

            migrationBuilder.InsertData(
                table: "Books",
                columns: new[] { "Id", "Author", "Editor", "Image", "Title", "UserId" },
                values: new object[,]
                {
                    { 1, "Victor Hugo", "Plume de Carotte", null, "Han d'Islande", 1 },
                    { 2, "Victor Hugo", "Arvensa", null, "Le dernier Jour d'un Condamné", 1 },
                    { 3, "J.R.R. Tolkien", "Bourgois", null, "Le Silmarillon", 1 },
                    { 4, "J.R.R. Tolkien", "Bourgois", null, "Le Seigneur des anneaux : Les Deux Tours", 1 },
                    { 5, "J.R.R. Tolkien", "Bourgois", null, "Le Seigneur des anneaux : Le Retour du roi", 1 },
                    { 6, "Oscar Wilde", "Le livre qui parle", null, "Le Portrait de Dorian Gray", 1 }
                });

            migrationBuilder.CreateIndex(
                name: "IX_Books_UserId",
                table: "Books",
                column: "UserId");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Books");

            migrationBuilder.DropTable(
                name: "Users");
        }
    }
}
