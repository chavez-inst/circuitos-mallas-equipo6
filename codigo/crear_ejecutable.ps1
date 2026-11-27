# crea el ejecutable de la interfaz en entregables/Mallas_Equipo6.exe
# se necesita PyInstaller: pip install pyinstaller
# se corre desde cualquier carpeta con: powershell -ExecutionPolicy Bypass -File codigo/crear_ejecutable.ps1
$raiz = Split-Path -Parent $PSScriptRoot
# los archivos de trabajo de PyInstaller van a una carpeta temporal y no a la del proyecto
$temporal = Join-Path $env:TEMP "mallas_equipo6_build"
# bibliotecas que matplotlib arrastra pero el programa no usa; quitarlas hace el ejecutable mas chico
$quitar = "scipy", "pandas", "openpyxl", "xlsxwriter", "sympy", "lxml", "aiohttp", "fsspec", "requests", "urllib3", "yaml", "IPython", "setuptools"
$exclusiones = $quitar | ForEach-Object { "--exclude-module", $_ }

python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name Mallas_Equipo6 `
    --distpath (Join-Path $raiz "entregables") `
    --workpath $temporal `
    --specpath $temporal `
    @exclusiones `
    --add-data "$raiz/reporte/img/circuito1.png;reporte/img" `
    --add-data "$raiz/reporte/img/circuito2.png;reporte/img" `
    --add-data "$raiz/reporte/logos/Logo_UNAM.png;reporte/logos" `
    --add-data "$raiz/reporte/logos/Logo_FI.png;reporte/logos" `
    (Join-Path $raiz "codigo/interfaz.py")
