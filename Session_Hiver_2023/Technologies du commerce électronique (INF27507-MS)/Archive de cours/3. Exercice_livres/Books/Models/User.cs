namespace Books.Models
{
    public class User
    {
        public User() 
        {
            Books = new List<Book>();
        }
        public int Id { get; set; }

        public string Name { get; set; }

        public ICollection<Book> Books { get; set;}
    }
}
