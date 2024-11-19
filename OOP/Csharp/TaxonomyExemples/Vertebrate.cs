using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Csharp
{
    internal class Vertebrate : Animal
    {
        // CONSTRUCTOR
        public Vertebrate() { }



        // PROPERTIES & ACCESSORS
        // className and ClassName from Class Animal
        protected string name;
        public string Name
        {
            get { return name; }

            set
            {
                if (string.IsNullOrEmpty(value))
                {
                    Console.WriteLine("ClassName cannot be empty.");
                    throw new ArgumentException("ClassName cannot be empty.");
                }
                name = value;
            }
        }

        private string thirdSecret = "Vertebrate third secret";

        protected string secondSecret = "Vertebrate second secret";

        private string secret = "Vertebrate secret"; 
        public string Secret
        {
            get { return secret; }
        }



        // METHODS
        // IsOfWhatClass, IsOfWhatKingdom and TriggerTheInstinct from Class Animal
        public void DisplayThirdSecret()
        {
            Console.WriteLine(thirdSecret);
            Console.WriteLine("DisplayThirdSecret method triggered by Vertebrate Class \n");
        }

        public void DisplaySecondSecret()
        {
            Console.WriteLine(secondSecret);
            Console.WriteLine("DisplaySecondSecret method triggered by Vertebrate Class \n");
        }

        public override void TriggerTheInstinct()
        {
            Console.WriteLine("TriggerTheInstinct method triggered by Vertebrate Class \n");
        }

        public void TriggerTheVertebrateInstinct()
        {
            Console.WriteLine("TriggerTheVertebrateInstinct method triggered by Vertebrate Class \n");
        }

        public override void SetClassName(string _className)
        {
            string addition = "(super class)";

            string tempString = string.Format("{0} {1}", _className, addition);
            ClassName = tempString;
            Console.WriteLine("SetClassName method triggered by Vertebrate Class \n");
        }

        public virtual void SetName(string _name)
        {
            Name = _name;
            Console.WriteLine("SetName method triggered by Vertebrate Class \n");
        }
    }
}
