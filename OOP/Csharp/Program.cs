using Csharp.TaxonomyExemples;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Csharp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // From TaxonomyExemples folder : 

            Mammal elephant = new Mammal();
            elephant.IsOfWhatKingdom();
            elephant.IsOfWhatClass();
            
            elephant.SetClassName("Mammal");
            elephant.IsOfWhatClass();
            Console.WriteLine("\n");



            Vertebrate vertebrate = new Vertebrate();
            vertebrate.SetClassName("Vertebrate");
            vertebrate.SetName("Dumbo");
            vertebrate.IsOfWhatKingdom();
            vertebrate.IsOfWhatClass();
            Console.WriteLine(vertebrate.Name);
            Console.WriteLine(vertebrate.Secret);
            vertebrate.DisplaySecondSecret();
            vertebrate.DisplayThirdSecret();
            vertebrate.TriggerTheInstinct();
            Console.WriteLine("\n");



            Bird bird = new Bird();
            bird.SetClassName("Aves");
            bird.SetName("Pitpit");
            bird.IsOfWhatKingdom();
            bird.IsOfWhatClass();
            Console.WriteLine(bird.Name);
            Console.WriteLine(bird.Secret);
            bird.DisplaySecondSecret();
            bird.DisplayThirdSecret();

            bird.SetNameModified("Cocotte");
            Console.WriteLine(bird.Name);
            bird.DisplaySecondSecretFromBird();
            bird.TriggerTheInstinct();
            Console.WriteLine("\n");



            Pelican pelican = new Pelican();
            pelican.SetClassName("Aves");
            pelican.SetName("Nigel");
            pelican.TriggerTheInstinct();



            Console.WriteLine("Press any keyboard key to close");
            Console.ReadLine();
        }
    }
}
