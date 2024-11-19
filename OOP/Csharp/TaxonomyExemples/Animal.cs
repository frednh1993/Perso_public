using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Csharp
{

    abstract class Animal : IAnimal
    {
        // PROPERTIES & ACCESSORS
        protected string className;
        public string ClassName 
        { 
            get { return className; } 

            set {
                if (string.IsNullOrEmpty(value)) 
                {
                    Console.WriteLine("ClassName cannot be empty.");
                    throw new ArgumentException("ClassName cannot be empty.");
                }
                className = value; 
            }
        }



        // METHODS
        public void IsOfWhatClass()
        {
            if (!string.IsNullOrEmpty(className))
                Console.WriteLine($"{ClassName} class !");
            else
                Console.WriteLine("Class have not been assigned !");

            Console.WriteLine("IsOfWhatClass method triggered by Animal Class \n");
        }

        public void IsOfWhatKingdom()
        {
            Console.WriteLine("Animalia Kingdom ! ");
            Console.WriteLine("IsOfWhatKingdom method triggered by Animal Class \n");
        }

        public virtual void TriggerTheInstinct()
        {
            Console.WriteLine("TriggerTheInstinct method triggered by Animal Class \n");
        }

        abstract public void SetClassName(string className);
    }

}
