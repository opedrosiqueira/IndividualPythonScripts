Remove-Item C:\VSCode* -Recurse
Remove-Item "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\VS Code.lnk"
Remove-Item "C:\Users\Public\Desktop\VS Code.lnk"

Expand-Archive "\\10.8.32.3\arquivos\Arquivos curso superior\tads-algoritmos\VSCode-win32-x64-1.76.1.zip" -DestinationPath C:\

[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\VSCode-win32-x64-1.76.1\jdk-17.0.6", "User")

exit
