using GradeManagement.Models;
using System.ComponentModel.DataAnnotations;


namespace GradeManagement.Models
{
    public class Transcript
    {
        [Key]
        public int Id { get; set; }


        public int StudentId { get; set; }
        public Student Student { get; set; }


        public int Grade { get; set; }


        public int CourseId { get; set; }
        public Course Course { get; set; }
    }
}
