using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Csharp.TaxonomyExemples
{
    internal class Pelican : Bird
    {
        public override void TriggerTheInstinct()
        {
            TriggerTheVertebrateInstinct();
        }
    }
}
