using System;
using System.Diagnostics;
using System.IO;

class Launcher
{
    static void Main()
    {
        var dir = Path.GetDirectoryName(typeof(Launcher).Assembly.Location);
        var exePath = Path.Combine(dir, "_internal", "WSA Installer.exe");

        var proc = new Process();
        proc.StartInfo.FileName = exePath;
        proc.StartInfo.WorkingDirectory = Path.Combine(dir, "_internal");
        proc.Start();
        proc.WaitForExit();
        Environment.Exit(proc.ExitCode);
    }
}
