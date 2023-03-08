using GradeManagement.Models;
using System.ComponentModel.DataAnnotations;


namespace GradeManagement.Models
{
    public class Course
    {
        public Course()
        {
            Transcripts = new List<Transcript>();
        }

        [Key]
        public int Id { get; set; }

        public string Title { get; set; }
        public double Coefficient { get; set; }

        public ICollection<Transcript> Transcripts { get;set; }
    }
}
