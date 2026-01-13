# Assets Folder

This folder should contain:

- `icon.png` - App icon (1024x1024px)
- `splash.png` - Splash screen (1284x2778px for iPhone 13 Pro Max)
- `adaptive-icon.png` - Android adaptive icon (1024x1024px)
- `favicon.png` - Web favicon (48x48px)

## Generating Assets

You can use the following tools to generate app icons:

1. **Expo Asset Generator**: Use Expo's built-in tools
2. **Online Tools**:
   - https://www.appicon.co/
   - https://icon.kitchen/

## Temporary Solution

For development, you can use placeholder images. The app will still work without custom icons, Expo will use default placeholders.

To add your own icons later:
1. Create or download icon images
2. Place them in this `assets` folder
3. Update the paths in `app.json` if needed
