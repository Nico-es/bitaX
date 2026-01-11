package com.abitax.utils

object Constants {
    // API Configuration
    const val BASE_URL = "https://api.abitax.ge/"
    const val MAPS_API_KEY = "AIzaSyCNskrqibDP4rG-3PN9jWIo1dslkQkXO6w"
    
    // Shared Preferences
    const val PREF_NAME = "abitax_pref"
    const val KEY_IS_LOGGED_IN = "is_logged_in"
    const val KEY_USER_ID = "user_id"
    const val KEY_USER_NAME = "user_name"
    const val KEY_USER_EMAIL = "user_email"
    const val KEY_USER_TYPE = "user_type"
    
    // API Endpoints
    const val LOGIN_URL = "api/auth/login"
    const val REGISTER_URL = "api/auth/register"
    const val SERVICES_URL = "api/services"
    const val PROPERTIES_URL = "api/properties"
    const val PROFESSIONALS_URL = "api/professionals"
    
    // Request Codes
    const val LOCATION_PERMISSION_REQUEST_CODE = 1001
    const val IMAGE_PICK_REQUEST_CODE = 1002
    
    // Colors
    const val COLOR_GREEN = "#007A33"
    const val COLOR_WHITE = "#FFFFFF"
    const val COLOR_RED = "#CE1126"
    const val COLOR_BLUE = "#0055A4"
    const val COLOR_GOLD = "#FFD700"
}