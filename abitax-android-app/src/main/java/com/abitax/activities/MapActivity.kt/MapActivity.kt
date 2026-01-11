package com.abitax.activities

import android.Manifest
import android.content.pm.PackageManager
import android.location.Location
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.abitax.R
import com.abitax.databinding.ActivityMapBinding
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.BitmapDescriptorFactory
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions

class MapActivity : AppCompatActivity(), OnMapReadyCallback {
    
    private lateinit var binding: ActivityMapBinding
    private lateinit var googleMap: GoogleMap
    private lateinit var fusedLocationClient: FusedLocationProviderClient
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMapBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        // Set up toolbar
        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = "Mapa de Servicios"
        
        // Initialize map
        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)
        
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        
        // Set up click listeners
        binding.fabMyLocation.setOnClickListener {
            getCurrentLocation()
        }
        
        binding.fabFilter.setOnClickListener {
            // Show filter dialog
            showFilterDialog()
        }
    }
    
    override fun onMapReady(map: GoogleMap) {
        googleMap = map
        
        // Configure map
        googleMap.uiSettings.isZoomControlsEnabled = true
        googleMap.uiSettings.isCompassEnabled = true
        googleMap.uiSettings.isMyLocationButtonEnabled = false
        
        // Check location permission
        if (checkLocationPermission()) {
            googleMap.isMyLocationEnabled = true
            getCurrentLocation()
        } else {
            requestLocationPermission()
        }
        
        // Add sample markers (in production, these would come from API)
        addSampleMarkers()
    }
    
    private fun checkLocationPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
    }
    
    private fun requestLocationPermission() {
        ActivityCompat.requestPermissions(
            this,
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
            LOCATION_PERMISSION_REQUEST_CODE
        )
    }
    
    private fun getCurrentLocation() {
        if (checkLocationPermission()) {
            fusedLocationClient.lastLocation.addOnSuccessListener { location: Location? ->
                location?.let {
                    val currentLatLng = LatLng(it.latitude, it.longitude)
                    googleMap.animateCamera(
                        CameraUpdateFactory.newLatLngZoom(currentLatLng, 12f)
                    )
                }
            }
        } else {
            Toast.makeText(this, "Permiso de ubicación requerido", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun addSampleMarkers() {
        // Guinea Equatorial locations
        val malabo = LatLng(3.7521, 8.7737)
        val bata = LatLng(1.8659, 9.7687)
        val ebeibiyin = LatLng(2.1511, 11.3353)
        
        // Add markers
        googleMap.addMarker(
            MarkerOptions()
                .position(malabo)
                .title("Malabo")
                .snippet("45 profesionales disponibles")
                .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN))
        )
        
        googleMap.addMarker(
            MarkerOptions()
                .position(bata)
                .title("Bata")
                .snippet("32 propiedades disponibles")
                .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_BLUE))
        )
        
        googleMap.addMarker(
            MarkerOptions()
                .position(ebeibiyin)
                .title("Ebebiyín")
                .snippet("18 servicios activos")
                .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED))
        )
    }
    
    private fun showFilterDialog() {
        // Implement filter dialog
        Toast.makeText(this, "Filtros de búsqueda", Toast.LENGTH_SHORT).show()
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == LOCATION_PERMISSION_REQUEST_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                if (::googleMap.isInitialized) {
                    googleMap.isMyLocationEnabled = true
                    getCurrentLocation()
                }
            }
        }
    }
    
    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
    
    companion object {
        private const val LOCATION_PERMISSION_REQUEST_CODE = 1001
    }
}