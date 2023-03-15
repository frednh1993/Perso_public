using GradeManagement.Models;
using System.ComponentModel.DataAnnotations;

namespace GradeManagement.Models
{
    public class Student
    {
        public Student () 
        {
            OverallAverage = 0;
            Transcripts = new List<Transcript> ();
        }


        [Key]
        public int Id { get; set; }


        public string FirstName { get; set; }
        public string LastName { get; set;}
        public double OverallAverage { get; set; }
        public ICollection<Transcript> Transcripts { get;set; }


        public void CalculOverallAverage()
        {
            double SumGradeCoefficient = 0;
            double SumCoefficient = 0;

            foreach (Transcript transcript in this.Transcripts)
            {
                SumGradeCoefficient = SumGradeCoefficient + (transcript.Grade * transcript.Course.Coefficient);
                SumCoefficient = SumCoefficient + transcript.Course.Coefficient;
            }
            this.OverallAverage = (SumGradeCoefficient / SumCoefficient);
        }
    }
}

