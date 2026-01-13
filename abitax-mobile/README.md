# Abitax Mobile App

React Native app built with Expo for the Abitax platform.

## Prerequisites

- Node.js installed
- Expo Go app installed on your phone ([iOS](https://apps.apple.com/app/expo-go/id982107779) | [Android](https://play.google.com/store/apps/details?id=host.exp.exponent))

## Setup Instructions

1. Install dependencies:
```bash
cd abitax-mobile
npm install
```

2. Start the development server:
```bash
npm start
```

3. Scan the QR code:
   - **iOS**: Open the Camera app and scan the QR code
   - **Android**: Open the Expo Go app and scan the QR code

## Features

- User authentication (login/register)
- Property browsing
- Service listings
- Professional directory
- User profile management

## Tech Stack

- React Native
- Expo
- TypeScript
- Supabase (authentication & database)
- React Navigation

## Project Structure

```
abitax-mobile/
├── src/
│   ├── contexts/       # React contexts (Auth)
│   ├── lib/           # Utilities (Supabase client)
│   ├── navigation/    # Navigation setup
│   └── screens/       # App screens
├── App.tsx            # Main app component
├── app.json          # Expo configuration
└── package.json      # Dependencies
```

## Available Scripts

- `npm start` - Start the Expo development server
- `npm run android` - Open on Android device/emulator
- `npm run ios` - Open on iOS simulator (Mac only)

## Connecting to Your Backend

The app is already configured to connect to your Supabase backend. The connection details are stored in the `.env` file.
