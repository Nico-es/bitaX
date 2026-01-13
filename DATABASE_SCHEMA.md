# abitaX Database Schema Documentation

## Overview
This document describes the complete database schema for the abitaX Android application. The database is hosted on Supabase (PostgreSQL) and includes Row Level Security (RLS) for data protection.

## Connection Details
```
Environment Variables:
- VITE_SUPABASE_URL: https://rtypzsrdktjbrrymqvnu.supabase.co
- VITE_SUPABASE_ANON_KEY: [Available in .env file]
```

## Table of Contents
1. [User Management](#user-management)
2. [Professional Services](#professional-services)
3. [Properties](#properties)
4. [Bookings](#bookings)
5. [Social Features](#social-features)
6. [System Tables](#system-tables)

---

## User Management

### 1. profiles
User profile information and authentication data.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key, references auth.users |
| full_name | text | User's full name |
| phone | text | Phone number (optional) |
| avatar_url | text | Profile picture URL |
| user_type | text | 'user' or 'professional' |
| bio | text | User biography |
| fcm_token | text | Firebase Cloud Messaging token for push notifications |
| notification_enabled | boolean | User notification preferences |
| language | text | Preferred language ('es', 'en', 'fr') |
| created_at | timestamptz | Account creation timestamp |
| updated_at | timestamptz | Last update timestamp |

**Android Model (User.kt):**
```kotlin
data class User(
    val id: String,
    val fullName: String,
    val phone: String? = null,
    val avatarUrl: String? = null,
    val userType: UserType,
    val bio: String? = null,
    val fcmToken: String? = null,
    val notificationEnabled: Boolean = true,
    val language: String = "es",
    val createdAt: String,
    val updatedAt: String
)

enum class UserType {
    USER, PROFESSIONAL
}
```

**API Endpoints:**
```kotlin
// Get current user profile
suspend fun getCurrentProfile(): User {
    val response = supabase.from("profiles")
        .select()
        .eq("id", supabase.auth.currentUserOrNull()?.id ?: "")
        .single()
    return response.decodeAs<User>()
}

// Update profile
suspend fun updateProfile(userId: String, updates: Map<String, Any>) {
    supabase.from("profiles")
        .update(updates)
        .eq("id", userId)
        .execute()
}
```

---

## Professional Services

### 2. professionals
Professional user information and credentials.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| user_id | uuid | References profiles.id (unique) |
| profession | text | Professional title/specialty |
| company_name | text | Company name (optional) |
| years_experience | integer | Years of experience |
| certifications | text[] | Array of certifications |
| rating | numeric | Average rating (0-5) |
| total_reviews | integer | Total number of reviews |
| verified | boolean | Verification status |
| available | boolean | Availability status |
| location | text | Professional's location |
| latitude | numeric | GPS latitude |
| longitude | numeric | GPS longitude |
| response_time_hours | integer | Average response time in hours |
| completion_rate | numeric | Job completion percentage (0-100) |
| created_at | timestamptz | Profile creation timestamp |

**Android Model (Professional.kt):**
```kotlin
data class Professional(
    val id: String,
    val userId: String,
    val profession: String,
    val companyName: String? = null,
    val yearsExperience: Int = 0,
    val certifications: List<String> = emptyList(),
    val rating: Double = 0.0,
    val totalReviews: Int = 0,
    val verified: Boolean = false,
    val available: Boolean = true,
    val location: String? = null,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val responseTimeHours: Int = 24,
    val completionRate: Double = 100.0,
    val createdAt: String,
    val profile: User? = null // Joined data
)
```

### 3. service_categories
Categories for organizing services.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| name | text | Category name in Spanish |
| name_en | text | Category name in English |
| icon | text | Icon identifier |
| description | text | Category description |
| active | boolean | Whether category is active |
| created_at | timestamptz | Creation timestamp |

**Default Categories:**
- Plomería (Plumbing)
- Electricidad (Electrical)
- Carpintería (Carpentry)
- Limpieza (Cleaning)
- Construcción (Construction)
- Jardinería (Gardening)
- Pintura (Painting)
- Mudanzas (Moving)
- Reparaciones (Repairs)
- Tecnología (Technology)

### 4. services
Services offered by professionals.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| professional_id | uuid | References professionals.id |
| category_id | uuid | References service_categories.id |
| title | text | Service title |
| description | text | Service description |
| category | text | Legacy category field |
| price_from | numeric | Starting price |
| price_to | numeric | Maximum price |
| currency | text | Currency code (default: XAF) |
| images | text[] | Array of image URLs |
| location | text | Service coverage area |
| latitude | numeric | GPS latitude |
| longitude | numeric | GPS longitude |
| featured | boolean | Featured service flag |
| active | boolean | Service availability |
| created_at | timestamptz | Creation timestamp |
| updated_at | timestamptz | Last update timestamp |

**Android Model (Service.kt):**
```kotlin
data class Service(
    val id: String,
    val professionalId: String,
    val categoryId: String? = null,
    val title: String,
    val description: String,
    val category: String,
    val priceFrom: Double? = null,
    val priceTo: Double? = null,
    val currency: String = "XAF",
    val images: List<String> = emptyList(),
    val location: String? = null,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val featured: Boolean = false,
    val active: Boolean = true,
    val createdAt: String,
    val updatedAt: String,
    val professional: Professional? = null // Joined data
)
```

**API Example:**
```kotlin
// Get services by category
suspend fun getServicesByCategory(categoryId: String): List<Service> {
    return supabase.from("services")
        .select("""
            *,
            professional:professionals(
                *,
                profile:profiles(*)
            )
        """)
        .eq("category_id", categoryId)
        .eq("active", true)
        .order("created_at", ascending = false)
        .decodeList<Service>()
}

// Search services near location
suspend fun searchNearbyServices(
    lat: Double,
    lng: Double,
    radiusKm: Double = 10.0
): List<Service> {
    // Use PostGIS or implement distance calculation
    // For simple distance: sqrt((lat1-lat2)^2 + (lng1-lng2)^2) * 111 km
}
```

---

## Properties

### 5. properties
Real estate listings.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| owner_id | uuid | References profiles.id |
| title | text | Property title |
| description | text | Property description |
| property_type | text | 'house', 'apartment', 'land', 'commercial' |
| listing_type | text | 'rent' or 'sale' |
| price | numeric | Property price |
| currency | text | Currency code (default: XAF) |
| bedrooms | integer | Number of bedrooms |
| bathrooms | integer | Number of bathrooms |
| area_sqm | numeric | Area in square meters |
| address | text | Property address |
| city | text | City name |
| latitude | numeric | GPS latitude |
| longitude | numeric | GPS longitude |
| images | text[] | Array of image URLs |
| amenities | text[] | Array of amenities |
| featured | boolean | Featured listing flag |
| views_count | integer | Number of views |
| available | boolean | Availability status |
| created_at | timestamptz | Creation timestamp |
| updated_at | timestamptz | Last update timestamp |

**Android Model (Property.kt):**
```kotlin
data class Property(
    val id: String,
    val ownerId: String,
    val title: String,
    val description: String,
    val propertyType: PropertyType,
    val listingType: ListingType,
    val price: Double,
    val currency: String = "XAF",
    val bedrooms: Int? = null,
    val bathrooms: Int? = null,
    val areaSqm: Double? = null,
    val address: String,
    val city: String,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val images: List<String> = emptyList(),
    val amenities: List<String> = emptyList(),
    val featured: Boolean = false,
    val viewsCount: Int = 0,
    val available: Boolean = true,
    val createdAt: String,
    val updatedAt: String,
    val owner: User? = null // Joined data
)

enum class PropertyType {
    HOUSE, APARTMENT, LAND, COMMERCIAL
}

enum class ListingType {
    RENT, SALE
}
```

### 6. property_viewings
Property viewing appointments.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| property_id | uuid | References properties.id |
| viewer_id | uuid | References profiles.id |
| viewing_date | timestamptz | Scheduled viewing date/time |
| status | text | 'requested', 'confirmed', 'completed', 'cancelled' |
| notes | text | Additional notes |
| created_at | timestamptz | Request creation timestamp |

---

## Bookings

### 7. bookings
Service booking appointments.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| client_id | uuid | References profiles.id |
| professional_id | uuid | References professionals.id |
| service_id | uuid | References services.id (optional) |
| booking_date | date | Booking date |
| booking_time | time | Booking time |
| status | text | 'pending', 'confirmed', 'completed', 'cancelled' |
| location | text | Service location address |
| latitude | numeric | GPS latitude |
| longitude | numeric | GPS longitude |
| notes | text | Additional notes |
| total_amount | numeric | Total booking amount |
| currency | text | Currency code (default: XAF) |
| created_at | timestamptz | Booking creation timestamp |
| updated_at | timestamptz | Last update timestamp |

**Android Model (Booking.kt):**
```kotlin
data class Booking(
    val id: String,
    val clientId: String,
    val professionalId: String,
    val serviceId: String? = null,
    val bookingDate: String, // LocalDate
    val bookingTime: String, // LocalTime
    val status: BookingStatus,
    val location: String,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val notes: String? = null,
    val totalAmount: Double? = null,
    val currency: String = "XAF",
    val createdAt: String,
    val updatedAt: String,
    val client: User? = null, // Joined data
    val professional: Professional? = null, // Joined data
    val service: Service? = null // Joined data
)

enum class BookingStatus {
    PENDING, CONFIRMED, COMPLETED, CANCELLED
}
```

**API Example:**
```kotlin
// Create a booking
suspend fun createBooking(booking: Booking): Booking {
    return supabase.from("bookings")
        .insert(booking)
        .select()
        .single()
        .decodeAs<Booking>()
}

// Get user's bookings
suspend fun getMyBookings(): List<Booking> {
    return supabase.from("bookings")
        .select("""
            *,
            professional:professionals(*),
            service:services(*)
        """)
        .eq("client_id", supabase.auth.currentUserOrNull()?.id ?: "")
        .order("booking_date", ascending = false)
        .decodeList<Booking>()
}

// Update booking status
suspend fun updateBookingStatus(bookingId: String, status: BookingStatus) {
    supabase.from("bookings")
        .update(mapOf("status" to status.name.lowercase()))
        .eq("id", bookingId)
        .execute()
}
```

---

## Social Features

### 8. reviews
User reviews and ratings.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| reviewer_id | uuid | References profiles.id |
| professional_id | uuid | References professionals.id |
| service_id | uuid | References services.id (optional) |
| rating | integer | Rating (1-5) |
| comment | text | Review comment |
| created_at | timestamptz | Review creation timestamp |

### 9. favorites
User favorite items.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| user_id | uuid | References profiles.id |
| item_type | text | 'property' or 'service' |
| item_id | uuid | ID of favorited item |
| created_at | timestamptz | Favorite creation timestamp |

### 10. chats
Chat conversations between users.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| user1_id | uuid | References profiles.id |
| user2_id | uuid | References profiles.id |
| last_message | text | Last message preview |
| last_message_at | timestamptz | Last message timestamp |
| created_at | timestamptz | Chat creation timestamp |

### 11. messages
Individual messages in chats.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| chat_id | uuid | References chats.id |
| sender_id | uuid | References profiles.id |
| content | text | Message content |
| read | boolean | Read status |
| created_at | timestamptz | Message timestamp |

---

## System Tables

### 12. notifications
User notifications.

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| user_id | uuid | References profiles.id |
| title | text | Notification title |
| body | text | Notification body |
| type | text | 'booking', 'message', 'review', 'system', 'property' |
| reference_id | uuid | Related item ID |
| read | boolean | Read status |
| created_at | timestamptz | Notification timestamp |

**API Example:**
```kotlin
// Get unread notifications
suspend fun getUnreadNotifications(): List<Notification> {
    return supabase.from("notifications")
        .select()
        .eq("user_id", supabase.auth.currentUserOrNull()?.id ?: "")
        .eq("read", false)
        .order("created_at", ascending = false)
        .decodeList<Notification>()
}

// Mark notification as read
suspend fun markNotificationAsRead(notificationId: String) {
    supabase.from("notifications")
        .update(mapOf("read" to true))
        .eq("id", notificationId)
        .execute()
}
```

---

## Security & Row Level Security (RLS)

All tables have RLS enabled with the following general rules:

1. **profiles**: Users can view all profiles, update only their own
2. **professionals**: Anyone can view available professionals, professionals can update their own
3. **services**: Anyone can view active services, professionals can manage their own
4. **properties**: Anyone can view available properties, owners can manage their own
5. **bookings**: Clients and professionals can view/manage their respective bookings
6. **reviews**: Anyone can view, reviewers can create, no updates/deletes
7. **favorites**: Users can view/manage only their own favorites
8. **chats/messages**: Users can only access chats they're part of
9. **notifications**: Users can only access their own notifications
10. **property_viewings**: Viewers and property owners can access relevant viewings

---

## API Client Setup (ApiClient.kt)

```kotlin
object SupabaseClient {
    val client = createSupabaseClient(
        supabaseUrl = BuildConfig.SUPABASE_URL,
        supabaseKey = BuildConfig.SUPABASE_ANON_KEY
    ) {
        install(Auth)
        install(Postgrest)
        install(Storage)
        install(Realtime)
    }
}

// Usage
val supabase = SupabaseClient.client
```

---

## Realtime Subscriptions

Example for listening to new messages:

```kotlin
val messageChannel = supabase.from("messages").subscribe(
    "chat_$chatId"
) { action ->
    when (action) {
        is PostgresAction.Insert -> {
            val newMessage = action.decodeRecord<Message>()
            // Handle new message
        }
    }
}
```

---

## Indexes and Performance

All foreign keys have indexes for optimal query performance. Geolocation queries use spatial indexes on latitude/longitude columns.

**Query Optimization Tips:**
1. Always use `.select()` with specific columns instead of `*` when possible
2. Use `.single()` or `.maybeSingle()` for single row queries
3. Add `.limit()` for list queries
4. Use indexes for filtering (city, status, category_id, etc.)
5. Leverage joined queries instead of multiple requests

---

## Environment Setup

**build.gradle (Module level):**
```gradle
android {
    buildTypes {
        debug {
            buildConfigField "String", "SUPABASE_URL", "\"https://rtypzsrdktjbrrymqvnu.supabase.co\""
            buildConfigField "String", "SUPABASE_ANON_KEY", "\"YOUR_ANON_KEY\""
        }
    }
}

dependencies {
    implementation "io.github.jan-tennert.supabase:postgrest-kt:2.0.0"
    implementation "io.github.jan-tennert.supabase:auth-kt:2.0.0"
    implementation "io.github.jan-tennert.supabase:storage-kt:2.0.0"
    implementation "io.github.jan-tennert.supabase:realtime-kt:2.0.0"
}
```

---

## Additional Resources

- [Supabase Kotlin Documentation](https://supabase.com/docs/reference/kotlin)
- [Supabase Dashboard](https://app.supabase.com/project/rtypzsrdktjbrrymqvnu)
- [PostgREST API Reference](https://postgrest.org/en/stable/api.html)

---

## Support

For database issues or schema changes, contact the backend team or check the project's README.md file.
