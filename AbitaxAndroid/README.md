# abitaX Android App

Android application for abitaX - The SuperApp of Equatorial Guinea

## Setup Instructions

### Prerequisites
- Android Studio (latest version recommended)
- JDK 8 or higher
- Android SDK with API level 34

### Opening the Project

1. Extract the ZIP file to your desired location
2. Open Android Studio
3. Click "Open" and select the `AbitaxAndroid` folder
4. Wait for Gradle to sync (this may take a few minutes)

### Configuration

#### Google Maps API Key
1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Open `app/src/main/AndroidManifest.xml`
3. Replace `YOUR_GOOGLE_MAPS_API_KEY_HERE` with your actual API key

#### Supabase Configuration
1. Open `app/src/main/java/com/abitax/utils/SupabaseClient.kt` (you'll need to create this)
2. Add your Supabase URL and Anon Key:
```kotlin
object SupabaseClient {
    private const val SUPABASE_URL = "your-supabase-url"
    private const val SUPABASE_KEY = "your-supabase-anon-key"

    val client = createSupabaseClient(SUPABASE_URL, SUPABASE_KEY) {
        install(Postgrest)
        install(GoTrue)
    }
}
```

### Running the App

1. Connect an Android device or start an emulator
2. Click the "Run" button in Android Studio
3. Select your device from the list

### Project Structure

```
app/
├── src/main/
│   ├── java/com/abitax/
│   │   ├── MainActivity.kt          # Splash screen
│   │   ├── activities/
│   │   │   ├── HomeActivity.kt      # Main home screen
│   │   │   ├── LoginActivity.kt     # Login screen
│   │   │   └── MapActivity.kt       # Map view
│   │   └── utils/
│   │       └── SharedPrefManager.kt # User session management
│   ├── res/
│   │   ├── layout/                  # XML layouts
│   │   ├── values/                  # Strings, colors, themes
│   │   └── mipmap/                  # App icons
│   └── AndroidManifest.xml
└── build.gradle
```

### Features

- User authentication (Login/Register)
- Google Maps integration
- Service listings
- Property search
- Professional directory
- User profile management

### Dependencies

- AndroidX libraries
- Material Design Components
- Google Maps SDK
- Google Location Services
- Retrofit (for API calls)
- Supabase Kotlin SDK
- Glide (for image loading)

### Next Steps

1. Implement Supabase authentication
2. Connect to your backend API
3. Add custom app icons in `res/mipmap-*` folders
4. Implement remaining activities and fragments
5. Add proper error handling and loading states

### Support

For issues or questions, refer to the main project documentation or contact the development team.
