# abitaX - Android Application 🇬🇶

## Description
abitaX is the first map-based superapp for Equatorial Guinea, connecting people, places, and services throughout the country.

## Features
- 🗺️ Interactive map with service locations
- 👷 Professional directory (construction, maintenance, etc.)
- 🏠 Property listings (rental and sale)
- 💬 Secure chat system
- 📱 User and professional profiles
- 🔐 Secure authentication
- 📍 Real-time location services

## Setup Instructions

### Prerequisites
- Android Studio Flamingo or later
- Java Development Kit (JDK) 17 or later
- Android SDK 34
- Google Maps API Key

### Installation
1. Clone the repository
2. Open in Android Studio
3. Add your Google Maps API key in `AndroidManifest.xml`
4. Add `google-services.json` to app folder
5. Sync Gradle
6. Run on device/emulator

## API Configuration
Replace the following in your configuration:
- Google Maps API Key: Add your key in AndroidManifest.xml
- Firebase: Add your google-services.json
- Backend URL: Update in Constants.kt

## Build Variants
- Debug: Development with logging enabled
- Release: Production optimized build

## Dependencies
- Google Maps SDK
- Firebase (Auth, Firestore, Analytics)
- Retrofit for API calls
- Glide for image loading
- Material Design Components

## Architecture
- MVVM (Model-View-ViewModel)
- Repository pattern
- LiveData for observables
- Navigation Component

## License
© 2024 abitaX. All rights reserved.