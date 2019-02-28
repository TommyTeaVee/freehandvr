using System;
using System.Diagnostics;

public class StartAndEnd
{
	// remember to start windows hidden
	public static string xyStart; //once close to finish, compile all scripts into one exe
	public static string zStart;
	public static string handStart;
	public static string xyStartName;
	public static string zStartName;
	public static string handStartName;
	public static string calibrateStart1;
	public static string calibrateStart2;
	public static string destroyProcesses; //keep as batch script?
	
	public static void start()
	{
		System.Diagnostics.Process.Start("CMD.exe", calibrateStart1);
		System.Diagnostics.Process.Start("CMD.exe", calibrateStart2);
		System.Diagnostics.Process.Start("CMD.exe", xyStart);
		System.Diagnostics.Process.Start("CMD.exe", zStart);
		System.Diagnostics.Process.Start("CMD.exe", handStart);
	}
	
	public static destroy()
	{
		//System.Diagnostics.Process.Start("CMD.exe", destroyProcesses); below idea might work better, needs to be tested
		foreach (var process in Process.GetProcessesByName(xyStartName))
		{
			process.Kill();
		}
		foreach (var process in Process.GetProcessesByName(zStartName))
		{
			process.Kill();
		}
		foreach (var process in Process.GetProcessesByName(handStartName))
		{
			process.Kill();
		}
	}
}
