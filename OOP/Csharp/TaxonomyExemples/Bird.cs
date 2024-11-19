using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Csharp
{
    internal class Bird : Vertebrate
    {
        // CONSTRUCTOR
        public Bird() { }



        // PROPERTIES & ACCESSORS
        // className and ClassName Class Animal  /-.-/  name and Name from Class Vertebrate



        // METHODS
        // IsOfWhatClass, IsOfWhatKingdom from Class Animal  /-.-/  SetName from Class Vertebrate
        public void SetNameModified(string _name) 
        {
            base.SetName(_name);
            Console.WriteLine("SetName method (SetNameModified) triggered by Vertebrate Class with modification in Bird Class \n");
        }

        public void DisplaySecondSecretFromBird()
        {
            Console.WriteLine(secondSecret);
            Console.WriteLine("DisplaySecondSecretFromBird method triggered by Bird Class \n");
        }

        public override void TriggerTheInstinct()
        {
            Console.WriteLine("TriggerTheInstinct method triggered by Bird \n");
        }
    }
}
