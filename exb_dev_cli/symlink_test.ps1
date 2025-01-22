# Widget Configurations
# Core Widgets
New-Item -ItemType SymbolicLink -Path "C:\Development\arcgis-experience-builder-1.16\ArcGISExperienceBuilder\client\pc_core_widgets" -Target "C:\Development\widgettemplate"

# Application 
# Widgets
New-Item -ItemType SymbolicLink -Path "C:\Development\arcgis-experience-builder-1.16\ArcGISExperienceBuilder\client\apptemplate_widgets" -Target "C:\Development\apptemplate\Widgets"
# App Configuration
# New-Item -ItemType SymbolicLink -Path "C:\Development\arcgis-experience-builder-1.16\ArcGISExperienceBuilder\server\public\apps\1" -Target "C:\Development\apptemplate\AppConfig"