using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Csharp
{

    public interface IAnimal
    {
        // Public properties
        string ClassName { get; set; }



        // Abstract public
        void SetClassName (string className);



        // Public
        void IsOfWhatKingdom();
        void IsOfWhatClass();
    }
       
}
