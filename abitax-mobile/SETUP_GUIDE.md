# Abitax Mobile - Setup Guide for Expo Go

Follow these steps to run the Abitax mobile app on your phone using Expo Go.

## Step 1: Install Expo Go on Your Phone

Download and install the Expo Go app:

- **iPhone**: [Download from App Store](https://apps.apple.com/app/expo-go/id982107779)
- **Android**: [Download from Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

## Step 2: Install Dependencies

Open your terminal and navigate to the mobile app directory:

```bash
cd abitax-mobile
npm install
```

This will install all required packages.

## Step 3: Start the Development Server

Run the following command:

```bash
npm start
```

This will start the Expo development server and display a QR code in your terminal.

## Step 4: Connect Your Phone

**Important**: Make sure your phone and computer are on the same WiFi network.

### On iPhone:
1. Open the Camera app
2. Point it at the QR code in your terminal
3. Tap the notification that appears
4. The app will open in Expo Go

### On Android:
1. Open the Expo Go app
2. Tap "Scan QR Code"
3. Point your camera at the QR code in your terminal
4. The app will load automatically

## Step 5: Using the App

Once the app loads:

1. **Create an Account**: Tap "Sign up" and register as either a Client or Professional
2. **Browse Features**: Use the bottom navigation to explore Properties, Services, and Professionals
3. **View Profile**: Check your profile in the Profile tab

## Troubleshooting

### QR Code Not Working?
- Ensure your phone and computer are on the same WiFi network
- Try running `npm start` with the `--tunnel` flag: `npm start --tunnel`

### App Not Loading?
- Check that all dependencies installed correctly
- Try clearing the cache: `npm start --clear`
- Restart the Expo Go app on your phone

### Connection Issues?
- Make sure your firewall isn't blocking the connection
- Try connecting via USB and running `npm run android` (Android) or `npm run ios` (iOS)

### Database Connection Issues?
- Verify the Supabase credentials in `.env` file are correct
- Check that your Supabase project is active and accessible

## Features Available

- User Authentication (Login/Register)
- Property Listings
- Service Directory
- Professional Profiles
- User Profile Management

## Development Tips

- Shake your phone to open the developer menu
- Enable "Fast Refresh" for instant updates when you change code
- Check the terminal for error messages if something goes wrong

## Next Steps

After successfully running the app, you can:
- Customize the UI colors and styling
- Add more features to the screens
- Implement property creation and editing
- Add image uploads
- Integrate maps for property locations

Enjoy developing with Abitax Mobile!
