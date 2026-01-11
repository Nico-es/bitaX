package com.abitax

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.appcompat.app.AppCompatActivity
import com.abitax.utils.SharedPrefManager

class MainActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Check if user is logged in
        Handler(Looper.getMainLooper()).postDelayed({
            val sharedPrefManager = SharedPrefManager.getInstance(this)
            
            if (sharedPrefManager.isLoggedIn) {
                // User is logged in, go to Home
                startActivity(Intent(this, HomeActivity::class.java))
            } else {
                // User is not logged in, go to Login
                startActivity(Intent(this, LoginActivity::class.java))
            }
            
            finish()
        }, 2000) // 2 seconds splash screen
    }
}