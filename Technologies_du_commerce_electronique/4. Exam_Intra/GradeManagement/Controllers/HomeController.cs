using GradeManagement.Models;
using GradeManagement.Models.ForViews;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace GradeManagement.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }


        [HttpGet] 
        public IActionResult AddCourse()
        {
            Course course= new Course();

            return View(course);
        }
        [HttpPost]
        public IActionResult AddCourse(Course _course)
        {
            GradeManagementContext context = new GradeManagementContext();
            context.Courses.Add(_course);
            context.SaveChanges();
            return RedirectToAction("Index");
        }


        [HttpGet]
        public IActionResult AddStudent()
        {
            Student student = new Student();
            return View(student);
        }
        [HttpPost]
        public IActionResult AddStudent(Student _student)
        {
            GradeManagementContext context = new GradeManagementContext();
            context.Students.Add(_student);
            context.SaveChanges();
            return RedirectToAction("Index");
        }


        [HttpGet]
        public IActionResult AddCourseToStudent()
        {
            GradeManagementContext context = new GradeManagementContext();
            List<Student> studentsList = context.Students.ToList();
            List<Course> coursesList = context.Courses.ToList();

            StudentCourse studentCourse = new StudentCourse();
            studentCourse.StudentsList = studentsList;
            studentCourse.CoursesList = coursesList;

            return View(studentCourse);
        }
        [HttpPost]
        public IActionResult AddCourseToStudent(int CourseId, int StudentId, int Grade)
        {
            GradeManagementContext context = new GradeManagementContext();
            Student student = context.Students.Include(s => s.Transcripts).Where(s => s.Id == StudentId).First();
            Course course = context.Courses.Where(c => c.Id == CourseId).First();
            
            Transcript transcript = new Transcript();
            transcript.Grade = Grade;
            transcript.StudentId = StudentId;
            transcript.CourseId = CourseId;
            course.Transcripts.Add(transcript);
            student.Transcripts.Add(transcript);
            student.CalculOverallAverage();               
            context.SaveChanges();

            return RedirectToAction("Index");
        }
    }
}
