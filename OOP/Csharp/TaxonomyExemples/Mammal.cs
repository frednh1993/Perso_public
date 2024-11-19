using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Csharp
{
    internal class Mammal : Animal
    {
        // CONSTRUCTOR
        public Mammal() { }



        // PROPERTIES & ACCESSORS
        // className and ClassName from Class Animal



        // METHODS
        // IsOfWhatClass, IsOfWhatKingdom and TriggerTheInstinct from Class Animal
        public override void SetClassName(string _className)
        {
            ClassName = _className;
            Console.WriteLine("SetClassName method triggered by Mammal Class \n");
        }
    }
}
