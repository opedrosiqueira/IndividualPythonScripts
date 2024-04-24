Remove-Item C:\VSCode* -Recurse
Expand-Archive "\\10.8.32.3\arquivos\Arquivos curso superior\tads-algoritmos\VSCode-win32-x64-1.83.1.zip" -DestinationPath C:\

Remove-Item C:\Users\aluno\Desktop\prova -Recurse
Expand-Archive "\\10.8.32.3\arquivos\Arquivos curso superior\tads-algoritmos\prova.zip" -DestinationPath C:\Users\aluno\Desktop\

Copy-Item "\\10.8.32.3\Arquivos\Arquivos curso superior\tads-algoritmos\exam-supervisor.py" -Destination "C:\VSCode-win32-x64-1.83.1\data\user-data\User\globalStorage\"

pip install pywinauto tk --user

Start-Process -FilePath "pythonw" -ArgumentList "C:\VSCode-win32-x64-1.83.1\data\user-data\User\globalStorage\exam-supervisor.py"

net use \\10.8.32.3\Arquivos /del
