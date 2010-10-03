using System;
using AVRConnector;
using System.Threading;

namespace main {

  public class MainClass {

	public static void Main(String[] args) {
	  try {
		byte l = 0;
		AVRConnection c = new AVRConnection();
		Console.WriteLine("Hello from AVR-connection example");

		while( true ) {
		  c.set_led(l);
		  if ( l == 1 ) {l = 0;}
		  else l = 1;
		}
	  }
	  finally{
		Console.WriteLine("EXIT AVR-connection example");
	  }
	}
  }
}
