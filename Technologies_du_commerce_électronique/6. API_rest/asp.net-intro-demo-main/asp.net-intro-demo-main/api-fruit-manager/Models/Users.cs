namespace api_fruit_manager.Models
{
    public class Users
    {
        // API database attributes.
        public int UserId { get; set; }

        public string UserName { get; set; }

        public string Password { get; set; }


        // Table relation (1 user have * products & * sales / 1 sale belong to 1 user /
        // 1 product belong to 1 user).
        public ICollection<Products>? Products { get; set; }

        public ICollection<Sales>? Sales { get; set; }
    }
}
