using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace outliers
{
    class Program
    {
        public static void Main(string[] args)
        {
            using (StreamReader sr = new StreamReader("dataForKosi.txt"))
            {
                Position[] t = ParseData(sr);
                
                ;
            }
        }

        public static Position[] ParseData(StreamReader sr)
        {
            Regex rx = new Regex(@".*?(\d+), (\d+).*?", RegexOptions.Compiled);

            List<Position> pos = new List<Position>();

            string line;

            while ((line = sr.ReadLine()) != null)
            {
                if (line.Contains("Red"))
                {
                    Match mt = rx.Match(line);

                    Position xy = new Position();

                    xy.X = double.Parse(mt.Groups[1].Value);
                    xy.Y = double.Parse(mt.Groups[2].Value);

                    pos.Add(xy);
                }
            }

            return pos.ToArray();
        }
    }
}
