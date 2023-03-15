namespace GradeManagement.Models.ForViews
{
    public class StudentCourse
    {
        // Inputs :
        public List<Student> StudentsList { get; set; }
        public List<Course> CoursesList { get; set; }

        // Outputs :
        public int Grade { get; set; }
        public int StudentId { get; set; }
        public int CourseId { get; set; }
    }
}
