"""
Build Script for WDock
Creates installer and portable versions
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path


class WDockBuilder:
    """Builder for WDock distribution packages"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.version = "1.0.0"
        
        # Clean build directories
        self.clean_build_dirs()
    
    def clean_build_dirs(self):
        """Clean build and dist directories"""
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def install_pyinstaller(self):
        """Install PyInstaller if not available"""
        try:
            import PyInstaller
            print("PyInstaller is already installed")
        except ImportError:
            print("Installing PyInstaller...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    def create_spec_file(self):
        """Create PyInstaller spec file"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['{self.project_root}'],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'win32api',
        'win32gui',
        'win32com.shell',
        'pythoncom',
        'psutil',
        'PIL',
        'pygetwindow',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WDock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/wdock.ico' if Path('assets/wdock.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WDock',
)
'''
        
        spec_file = self.project_root / "WDock.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        return spec_file
    
    def create_icon(self):
        """Create application icon"""
        assets_dir = self.project_root / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        icon_path = assets_dir / "wdock.ico"
        
        if not icon_path.exists():
            print("Creating default application icon...")
            # Create a simple icon using PIL
            try:
                from PIL import Image, ImageDraw
                
                # Create 64x64 icon
                img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Draw dock base
                draw.rectangle([8, 45, 56, 58], fill=(70, 130, 200, 255), outline=(50, 100, 170, 255))
                
                # Draw app icons
                colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
                for i, color in enumerate(colors):
                    x = 12 + i * 10
                    y = 20
                    draw.rectangle([x, y, x+6, y+6], fill=color, outline=(0, 0, 0, 100))
                    # Connection line
                    draw.line([x+3, y+6, x+3, 45], fill=(150, 150, 150, 255))
                
                # Save as ICO
                img.save(icon_path, format='ICO')
                print(f"Icon created: {icon_path}")
            except Exception as e:
                print(f"Warning: Could not create icon: {e}")
        
        return icon_path if icon_path.exists() else None
    
    def build_executable(self):
        """Build executable using PyInstaller"""
        print("Building executable...")
        
        # Install PyInstaller
        self.install_pyinstaller()
        
        # Create icon
        self.create_icon()
        
        # Create spec file
        spec_file = self.create_spec_file()
        
        # Run PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", str(spec_file)]
        result = subprocess.run(cmd, cwd=self.project_root)
        
        if result.returncode == 0:
            print("Executable built successfully!")
            return self.dist_dir / "WDock"
        else:
            print("Error building executable!")
            return None
    
    def create_portable_version(self, exe_dir):
        """Create portable ZIP version"""
        if not exe_dir or not exe_dir.exists():
            print("Executable directory not found, skipping portable version")
            return None
        
        print("Creating portable version...")
        
        portable_name = f"WDock-{self.version}-Portable.zip"
        portable_path = self.dist_dir / portable_name
        
        with zipfile.ZipFile(portable_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add executable files
            for file_path in exe_dir.rglob('*'):
                if file_path.is_file():
                    arc_name = file_path.relative_to(exe_dir)
                    zf.write(file_path, arc_name)
            
            # Add documentation
            readme_content = f'''# WDock {self.version} - Portable Version

## About
WDock is a modern, customizable dock panel for Windows.

## Installation
1. Extract all files to a folder of your choice
2. Run WDock.exe
3. Right-click on the dock to access settings

## Features
- Adaptive icons with hover effects
- Drag & drop to add shortcuts
- Smart grouping by dragging icons together
- Auto-hide functionality
- Dark/light themes
- Multi-monitor support
- System tray integration

## Requirements
- Windows 10/11
- No additional installation required

## Support
For support and updates, check the project documentation.

Version: {self.version}
Built: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
'''
            
            zf.writestr("README.txt", readme_content)
        
        print(f"Portable version created: {portable_path}")
        return portable_path
    
    def create_installer_script(self):
        """Create Inno Setup installer script"""
        installer_script = f'''[Setup]
AppName=WDock
AppVersion={self.version}
AppPublisher=WDock Project
AppPublisherURL=https://github.com/wdock/wdock
AppSupportURL=https://github.com/wdock/wdock/issues
AppUpdatesURL=https://github.com/wdock/wdock/releases
DefaultDirName={{autopf}}\\WDock
DisableProgramGroupPage=yes
OutputDir={self.dist_dir}
OutputBaseFilename=WDock-{self.version}-Setup
SetupIconFile={self.project_root / "assets" / "wdock.ico" if Path("assets/wdock.ico").exists() else ""}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "startup"; Description: "Start WDock with Windows"; GroupDescription: "Startup Options"

[Files]
Source: "{self.dist_dir / "WDock" / "*"}"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{autoprograms}}\\WDock"; Filename: "{{app}}\\WDock.exe"
Name: "{{autodesktop}}\\WDock"; Filename: "{{app}}\\WDock.exe"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\\Microsoft\\Windows\\CurrentVersion\\Run"; ValueType: string; ValueName: "WDock"; ValueData: "{{app}}\\WDock.exe"; Flags: uninsdeletevalue; Tasks: startup

[Run]
Filename: "{{app}}\\WDock.exe"; Description: "{{cm:LaunchProgram,WDock}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{{userappdata}}\\WDock"
'''
        
        script_path = self.project_root / "installer.iss"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(installer_script)
        
        return script_path
    
    def build_installer(self):
        """Build Windows installer using Inno Setup"""
        print("Creating installer script...")
        
        script_path = self.create_installer_script()
        
        # Check if Inno Setup is available
        inno_paths = [
            r"C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe",
            r"C:\\Program Files\\Inno Setup 6\\ISCC.exe",
            r"C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe",
            r"C:\\Program Files\\Inno Setup 5\\ISCC.exe",
        ]
        
        inno_exe = None
        for path in inno_paths:
            if Path(path).exists():
                inno_exe = path
                break
        
        if inno_exe:
            print("Building installer with Inno Setup...")
            result = subprocess.run([inno_exe, str(script_path)])
            if result.returncode == 0:
                print("Installer built successfully!")
                return self.dist_dir / f"WDock-{self.version}-Setup.exe"
            else:
                print("Error building installer!")
        else:
            print("Inno Setup not found. Installer script created but not compiled.")
            print("Install Inno Setup from: https://jrsoftware.org/isdl.php")
            print(f"Then run: ISCC.exe {script_path}")
        
        return None
    
    def build_all(self):
        """Build all distribution packages"""
        print(f"Building WDock {self.version}...")
        print("=" * 50)
        
        # Build executable
        exe_dir = self.build_executable()
        
        if exe_dir:
            # Create portable version
            portable_path = self.create_portable_version(exe_dir)
            
            # Create installer
            installer_path = self.build_installer()
            
            print("\\n" + "=" * 50)
            print("Build completed!")
            
            if exe_dir:
                print(f"Executable: {exe_dir}")
            if portable_path:
                print(f"Portable: {portable_path}")
            if installer_path:
                print(f"Installer: {installer_path}")
            
            return True
        else:
            print("Build failed!")
            return False


def main():
    """Main build function"""
    builder = WDockBuilder()
    success = builder.build_all()
    
    if success:
        print("\\n✅ Build completed successfully!")
    else:
        print("\\n❌ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()