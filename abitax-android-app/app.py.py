# Creando el archivo ZIP completo para abitaX Android Studio Project
import zipfile
import os
from pathlib import Path

# Estructura de directorios del proyecto Android
project_structure = {
    'abitaX_Android_Project/': '',
    
    'abitaX_Android_Project/app/': '',
    'abitaX_Android_Project/app/src/': '',
    'abitaX_Android_Project/app/src/main/': '',
    'abitaX_Android_Project/app/src/main/java/': '',
    'abitaX_Android_Project/app/src/main/java/com/': '',
    'abitaX_Android_Project/app/src/main/java/com/abitax/': '',
    'abitaX_Android_Project/app/src/main/res/': '',
    'abitaX_Android_Project/app/src/main/res/layout/': '',
    'abitaX_Android_Project/app/src/main/res/drawable/': '',
    'abitaX_Android_Project/app/src/main/res/values/': '',
    'abitaX_Android_Project/app/src/main/assets/': '',
    'abitaX_Android_Project/gradle/': '',
    'abitaX_Android_Project/gradle/wrapper/': '',
    
    'abitaX_Android_Project/app/src/main/res/drawable-v24/': '',
    'abitaX_Android_Project/app/src/main/res/mipmap-hdpi/': '',
    'abitaX_Android_Project/app/src/main/res/mipmap-mdpi/': '',
    'abitaX_Android_Project/app/src/main/res/mipmap-xhdpi/': '',
    'abitaX_Android_Project/app/src/main/res/mipmap-xxhdpi/': '',
    'abitaX_Android_Project/app/src/main/res/mipmap-xxxhdpi/': '',
}

# Archivos del proyecto
files_content = {
    # =============================================
    # 1. AndroidManifest.xml
    # =============================================
    'abitaX_Android_Project/app/src/main/AndroidManifest.xml': '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.abitax">

    <!-- Permisos necesarios -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="28" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AbitaX"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true"
        tools:targetApi="31">

        <!-- Actividad Principal -->
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.AbitaX.NoActionBar"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Actividad WebView para la aplicación web -->
        <activity
            android:name=".WebViewActivity"
            android:exported="false"
            android:theme="@style/Theme.AbitaX.NoActionBar"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:windowSoftInputMode="adjustResize" />

        <!-- Actividad Mapa (si decides usar nativo) -->
        <activity
            android:name=".MapActivity"
            android:exported="false"
            android:theme="@style/Theme.AbitaX.NoActionBar" />

        <!-- Meta datos para Google Maps -->
        <meta-data
            android:name="com.google.android.geo.API_KEY"
            android:value="@string/google_maps_key" />

        <!-- Configuración para WebView -->
        <meta-data
            android:name="android.webkit.WebView.EnableSafeBrowsing"
            android:value="true" />

    </application>

</manifest>''',

    # =============================================
    # 2. MainActivity.java
    # =============================================
    'abitaX_Android_Project/app/src/main/java/com/abitax/MainActivity.java': '''package com.abitax;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Configurar botones
        Button btnOpenApp = findViewById(R.id.btn_open_app);
        Button btnOpenMap = findViewById(R.id.btn_open_map);
        Button btnExit = findViewById(R.id.btn_exit);

        // Botón para abrir la aplicación web
        btnOpenApp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, WebViewActivity.class);
                startActivity(intent);
                overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            }
        });

        // Botón para abrir solo el mapa
        btnOpenMap.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, WebViewActivity.class);
                intent.putExtra("section", "mapa");
                startActivity(intent);
                overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            }
        });

        // Botón para salir
        btnExit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
                overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            }
        });
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
    }
}''',

    # =============================================
    # 3. WebViewActivity.java
    # =============================================
    'abitaX_Android_Project/app/src/main/java/com/abitax/WebViewActivity.java': '''package com.abitax;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import androidx.appcompat.app.AppCompatActivity;

public class WebViewActivity extends AppCompatActivity {

    private WebView webView;
    private ProgressBar progressBar;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_webview);

        webView = findViewById(R.id.webview);
        progressBar = findViewById(R.id.progress_bar);

        // Obtener sección específica si se pasó como extra
        Intent intent = getIntent();
        String section = intent.getStringExtra("section");

        // Configurar WebView
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setDatabaseEnabled(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        webSettings.setGeolocationEnabled(true);
        webSettings.setBuiltInZoomControls(true);
        webSettings.setDisplayZoomControls(false);
        webSettings.setSupportZoom(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        
        // Habilitar localStorage
        webSettings.setDomStorageEnabled(true);
        webSettings.setDatabaseEnabled(true);
        
        // Configurar para Android 5.0+
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        }

        // Configurar WebViewClient
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                progressBar.setVisibility(View.GONE);
                
                // Scroll a sección específica si se proporcionó
                if (section != null && !section.isEmpty()) {
                    String jsScroll = "document.getElementById('" + section + "').scrollIntoView({behavior: 'smooth'});";
                    view.loadUrl("javascript:(function(){" + jsScroll + "})()");
                }
                
                // Inyectar JavaScript para manejar errores de mapa
                injectJavaScript();
            }
        });

        // Configurar WebChromeClient para progreso
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    progressBar.setVisibility(View.GONE);
                }
            }
        });

        // Cargar desde assets
        webView.loadUrl("file:///android_asset/index.html");
    }

    private void injectJavaScript() {
        String jsCode = """
            // Detectar si estamos en Android WebView
            const isAndroid = /Android/i.test(navigator.userAgent);
            const isWebView = /wv|WebView/i.test(navigator.userAgent);
            
            if (isAndroid && isWebView) {
                // Optimizar para WebView
                document.body.style.webkitOverflowScrolling = 'touch';
                
                // Prevenir zoom doble-tap
                document.addEventListener('touchstart', function(event) {
                    if (event.touches.length > 1) {
                        event.preventDefault();
                    }
                }, { passive: false });
                
                // Mejorar interacción táctil
                document.querySelectorAll('button, a, .btn, .nav-link, .map-result-item, .category-card, .service-card, .property-card').forEach(el => {
                    el.style.cursor = 'pointer';
                    el.addEventListener('touchstart', function() {
                        this.style.opacity = '0.8';
                    });
                    el.addEventListener('touchend', function() {
                        this.style.opacity = '1';
                    });
                });
            }
            
            // Verificar si Google Maps está cargado
            setTimeout(function() {
                if (typeof google === 'undefined' || !google.maps) {
                    console.log('Google Maps no está disponible');
                    
                    // Mostrar mensaje al usuario
                    var messageDiv = document.createElement('div');
                    messageDiv.style.cssText = 'position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); background:white; padding:2rem; border-radius:16px; box-shadow:0 8px 30px rgba(0,0,0,0.15); text-align:center; z-index:10000; max-width:300px;';
                    messageDiv.innerHTML = '<h3 style="color:#007A33;">⚠️ Mapa no disponible</h3><p>La funcionalidad del mapa requiere conexión a internet.</p><button onclick="this.parentElement.remove()" style="background:#007A33; color:white; border:none; padding:0.75rem 1.5rem; border-radius:12px; margin-top:1rem; cursor:pointer;">Entendido</button>';
                    document.body.appendChild(messageDiv);
                }
            }, 3000);
            
            // Ajustar tamaños de fuente para móvil
            if (window.innerWidth <= 768) {
                document.querySelectorAll('h1').forEach(function(h1) {
                    h1.style.fontSize = '2rem';
                });
                document.querySelectorAll('h2').forEach(function(h2) {
                    h2.style.fontSize = '1.5rem';
                });
                document.querySelectorAll('.btn').forEach(function(btn) {
                    btn.style.padding = '0.875rem 1.5rem';
                    btn.style.fontSize = '0.875rem';
                });
            }
            """;
        
        webView.loadUrl("javascript:(function(){" + jsCode + "})()");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
        }
    }
}''',

    # =============================================
    # 4. MapActivity.java
    # =============================================
    'abitaX_Android_Project/app/src/main/java/com/abitax/MapActivity.java': '''package com.abitax;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import java.util.ArrayList;
import java.util.List;

public class MapActivity extends AppCompatActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private static final int LOCATION_PERMISSION_REQUEST_CODE = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map);

        // Verificar permisos de ubicación
        if (checkLocationPermission()) {
            // Obtener fragmento del mapa
            SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                    .findFragmentById(R.id.map);
            if (mapFragment != null) {
                mapFragment.getMapAsync(this);
            }
        } else {
            requestLocationPermission();
        }
    }

    @Override
    public void onMapReady(@NonNull GoogleMap googleMap) {
        mMap = googleMap;

        // Posición inicial: Guinea Ecuatorial
        LatLng guineaEcuatorial = new LatLng(1.6139, 10.4670);
        
        // Agregar marcadores de ejemplo
        List<Provider> providers = getSampleProviders();
        
        for (Provider provider : providers) {
            LatLng location = new LatLng(provider.latitude, provider.longitude);
            
            float color = BitmapDescriptorFactory.HUE_GREEN;
            if (provider.category.equals("mantenimiento")) {
                color = BitmapDescriptorFactory.HUE_BLUE;
            } else if (provider.category.equals("inmobiliaria")) {
                color = BitmapDescriptorFactory.HUE_RED;
            }
            
            mMap.addMarker(new MarkerOptions()
                    .position(location)
                    .title(provider.name)
                    .snippet(provider.description + "\\n" + provider.price)
                    .icon(BitmapDescriptorFactory.defaultMarker(color)));
        }

        // Mover cámara a Guinea Ecuatorial con zoom
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(guineaEcuatorial, 7f));
        
        // Habilitar controles
        mMap.getUiSettings().setZoomControlsEnabled(true);
        mMap.getUiSettings().setCompassEnabled(true);
        mMap.getUiSettings().setMyLocationButtonEnabled(true);
        mMap.getUiSettings().setScrollGesturesEnabled(true);
        mMap.getUiSettings().setZoomGesturesEnabled(true);
        mMap.getUiSettings().setTiltGesturesEnabled(true);
        mMap.getUiSettings().setRotateGesturesEnabled(true);
        
        // Habilitar ubicación si tenemos permiso
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            mMap.setMyLocationEnabled(true);
        }
        
        // Configurar clic en marcadores
        mMap.setOnMarkerClickListener(marker -> {
            Toast.makeText(MapActivity.this, marker.getTitle(), Toast.LENGTH_SHORT).show();
            return false;
        });
    }

    private boolean checkLocationPermission() {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED;
    }

    private void requestLocationPermission() {
        ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                LOCATION_PERMISSION_REQUEST_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == LOCATION_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permiso concedido, reiniciar actividad
                recreate();
            } else {
                Toast.makeText(this, "Permiso de ubicación denegado", Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
    }

    // Clase interna para proveedores
    private static class Provider {
        String name;
        String category;
        String description;
        String price;
        double latitude;
        double longitude;

        Provider(String name, String category, String description, String price, 
                double latitude, double longitude) {
            this.name = name;
            this.category = category;
            this.description = description;
            this.price = price;
            this.latitude = latitude;
            this.longitude = longitude;
        }
    }

    private List<Provider> getSampleProviders() {
        List<Provider> providers = new ArrayList<>();
        
        providers.add(new Provider("Constructor Experto Malabo", "construccion",
                "Especialista en construcción de viviendas", "30,000 XAF/día",
                3.7521, 8.7737));
        
        providers.add(new Provider("Electricista Certificado Bata", "mantenimiento",
                "Instalaciones eléctricas residenciales", "25,000 XAF/servicio",
                1.8650, 9.7679));
        
        providers.add(new Provider("Villa Moderna Malabo", "inmobiliaria",
                "Villa exclusiva con piscina", "450,000 XAF/día",
                3.7450, 8.7830));
        
        providers.add(new Provider("Fontanero Profesional Ebebiyín", "mantenimiento",
                "Reparaciones de fontanería", "20,000 XAF/servicio",
                2.1511, 11.3353));
        
        return providers;
    }
}''',

    # =============================================
    # 5. activity_main.xml
    # =============================================
    'abitaX_Android_Project/app/src/main/res/layout/activity_main.xml': '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="@drawable/bg_gradient"
    android:gravity="center"
    android:padding="24dp"
    android:focusable="true"
    android:focusableInTouchMode="true">

    <!-- Logo -->
    <ImageView
        android:id="@+id/logo"
        android:layout_width="120dp"
        android:layout_height="120dp"
        android:layout_marginBottom="32dp"
        android:src="@drawable/ic_logo"
        android:contentDescription="@string/app_logo"
        android:elevation="8dp" />

    <!-- Título -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        android:textSize="36sp"
        android:textColor="@color/white"
        android:textStyle="bold"
        android:layout_marginBottom="8dp"
        android:fontFamily="sans-serif-black"
        android:letterSpacing="0.02" />

    <!-- Subtítulo -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_slogan"
        android:textSize="16sp"
        android:textColor="@color/white"
        android:alpha="0.9"
        android:layout_marginBottom="48dp"
        android:textAlignment="center"
        android:paddingHorizontal="32dp"
        android:lineSpacingExtra="4dp" />

    <!-- Botón Abrir Aplicación -->
    <com.google.android.material.button.MaterialButton
        android:id="@+id/btn_open_app"
        android:layout_width="match_parent"
        android:layout_height="56dp"
        android:text="@string/open_app"
        android:textSize="18sp"
        android:textAllCaps="false"
        android:backgroundTint="@color/green_ge"
        android:layout_marginBottom="16dp"
        app:icon="@drawable/ic_home"
        app:iconPadding="12dp"
        app:iconTint="@color/white"
        app:cornerRadius="16dp"
        android:elevation="4dp"
        android:stateListAnimator="@null"
        style="@style/Widget.AbitaX.Button" />

    <!-- Botón Abrir Mapa -->
    <com.google.android.material.button.MaterialButton
        android:id="@+id/btn_open_map"
        android:layout_width="match_parent"
        android:layout_height="56dp"
        android:text="@string/open_map"
        android:textSize="18sp"
        android:textAllCaps="false"
        android:backgroundTint="@color/blue_ge"
        android:layout_marginBottom="16dp"
        app:icon="@drawable/ic_map"
        app:iconPadding="12dp"
        app:iconTint="@color/white"
        app:cornerRadius="16dp"
        android:elevation="4dp"
        android:stateListAnimator="@null"
        style="@style/Widget.AbitaX.Button" />

    <!-- Botón Salir -->
    <com.google.android.material.button.MaterialButton
        android:id="@+id/btn_exit"
        android:layout_width="match_parent"
        android:layout_height="56dp"
        android:text="@string/exit"
        android:textSize="18sp"
        android:textAllCaps="false"
        app:backgroundTint="@android:color/transparent"
        app:strokeColor="@color/white"
        app:strokeWidth="2dp"
        app:icon="@drawable/ic_exit"
        app:iconPadding="12dp"
        app:iconTint="@color/white"
        app:cornerRadius="16dp"
        android:elevation="2dp"
        android:stateListAnimator="@null"
        style="@style/Widget.AbitaX.Button.Outline" />

    <!-- Versión -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_version"
        android:textSize="12sp"
        android:textColor="@color/white"
        android:alpha="0.7"
        android:layout_marginTop="32dp" />

</LinearLayout>''',

    # =============================================
    # 6. activity_webview.xml
    # =============================================
    'abitaX_Android_Project/app/src/main/res/layout/activity_webview.xml': '''<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white">

    <!-- Progress Bar -->
    <ProgressBar
        android:id="@+id/progress_bar"
        style="?android:attr/progressBarStyleHorizontal"
        android:layout_width="match_parent"
        android:layout_height="4dp"
        android:layout_alignParentTop="true"
        android:progressTint="@color/green_ge"
        android:progressBackgroundTint="@color/green_light"
        android:max="100"
        android:progress="0"
        android:visibility="gone" />

    <!-- WebView -->
    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/progress_bar" />

</RelativeLayout>''',

    # =============================================
    # 7. activity_map.xml
    # =============================================
    'abitaX_Android_Project/app/src/main/res/layout/activity_map.xml': '''<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white">

    <!-- Fragmento del Mapa -->
    <fragment
        android:id="@+id/map"
        android:name="com.google.android.gms.maps.SupportMapFragment"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

    <!-- Botón de regreso -->
    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fab_back"
        android:layout_width="56dp"
        android:layout_height="56dp"
        android:layout_margin="16dp"
        android:src="@drawable/ic_back"
        android:contentDescription="@string/back"
        app:backgroundTint="@color/green_ge"
        app:rippleColor="@color/green_dark"
        android:elevation="8dp"
        app:maxImageSize="24dp" />

</RelativeLayout>''',

    # =============================================
    # 8. strings.xml
    # =============================================
    'abitaX_Android_Project/app/src/main/res/values/strings.xml': '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">abitaX 🇬🇶</string>
    <string name="app_slogan">La SuperApp de Guinea Ecuatorial</string>
    <string name="app_version">Versión 1.0.0</string>
    <string name="app_logo">Logo de abitaX</string>
    
    <!-- Botones -->
    <string name="open_app">Abrir Aplicación</string>
    <string name="open_map">Abrir Mapa</string>
    <string name="exit">Salir</string>
    <string name="back">Volver</string>
    
    <!-- Mensajes -->
    <string name="loading">Cargando…</string>
    <string name="error">Error</string>
    <string name="retry">Reintentar</string>
    <string name="no_internet">Sin conexión a internet</string>
    <string name="location_permission">Permiso de ubicación requerido</string>
    
    <!-- Google Maps -->
    <!-- REEMPLAZA CON TU CLAVE API DE GOOGLE MAPS -->
    <string name="google_maps_key">TU_CLAVE_API_DE_GOOGLE_MAPS</string>
    
    <!-- Categorías -->
    <string name="category_construction">Construcción</string>
    <string name="category_maintenance">Mantenimiento</string>
    <string name="category_real_estate">Inmobiliaria</string>
    <string name="category_electrician">Electricistas</string>
    <string name="category_plumber">Fontaneros</string>
    <string name="category_architect">Arquitectos</string>
    
    <!-- Ciudades -->
    <string name="city_malabo">Malabo</string>
    <string name="city_bata">Bata</string>
    <string name="city_ebebiyin">Ebebiyín</string>
</resources>''',

    # =============================================
    # 9. colors.xml
    # =============================================
    'abitaX_Android_Project/app/src/main/res/values/colors.xml': '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Colores de Guinea Ecuatorial -->
    <color name="green_ge">#007A33</color>
    <color name="white_ge">#FFFFFF</color>
    <color name="red_ge">#CE1126</color>
    <color name="blue_ge">#0055A4</color>
    <color name="gold_ge">#FFD700</color>
    
    <!-- Colores derivados -->
    <color name="green_light">#E8F5E9</color>
    <color name="green_dark">#006028</color>
    <color name="blue_light">#E3F2FD</color>
    <color name="red_light">#FFEBEE</color>
    <color name="gold_light">#FFF8E1</color>
    
    <!-- Colores de interfaz -->
    <color name="white">#FFFFFF</color>
    <color name="black">#000000</color>
    <color name="gray_light">#F7FAFC</color>
    <color name="gray_dark">#1A1A1A</color>
    <color name="gray_medium">#4A5568</color>
    <color name="gray_border">#E2E8F0</color>
    
    <!-- Transparentes -->
    <color name="transparent">#00000000</color>
    <color name="semi_transparent">#80000000</color>
    
    <!-- Estados -->
    <color name="pressed_green">#009B4D</color>
    <color name="pressed_blue">#0066CC</color>
</resources>''',

    # =============================================
    # 10. styles.xml
    # =============================================
    'abitaX_Android_Project/app/src/main/res/values/styles.xml': '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Base application theme -->
    <style name="Theme.AbitaX" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/green_ge</item>
        <item name="colorPrimaryVariant">@color/green_dark</item>
        <item name="colorSecondary">@color/blue_ge</item>
        <item name="colorSecondaryVariant">@color/blue_ge</color>
        <item name="colorOnPrimary">@color/white</item>
        <item name="colorOnSecondary">@color/white</item>
        <item name="android:statusBarColor">@color/green_dark</item>
        <item name="android:navigationBarColor">@color/green_dark</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:windowLightNavigationBar">false</item>
        <item name="android:windowBackground">@color/white</item>
        <item name="android:textColor">@color/gray_dark</item>
    </style>

    <style name="Theme.AbitaX.NoActionBar">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
        <item name="android:windowFullscreen">false</item>
        <item name="android:windowContentOverlay">@null</item>
        <item name="android:windowDrawsSystemBarBackgrounds">true</item>
    </style>

    <!-- Estilos de botones -->
    <style name="Widget.AbitaX.Button" parent="Widget.MaterialComponents.Button">
        <item name="cornerRadius">16dp</item>
        <item name="android:paddingStart">24dp</item>
        <item name="android:paddingEnd">24dp</item>
        <item name="android:minHeight">56dp</item>
        <item name="android:elevation">4dp</item>
        <item name="android:textColor">@color/white</item>
        <item name="android:textSize">16sp</item>
        <item name="android:fontFamily">sans-serif-medium</item>
        <item name="android:letterSpacing">0.01</item>
    </style>

    <style name="Widget.AbitaX.Button.Outline" parent="Widget.MaterialComponents.Button.OutlinedButton">
        <item name="cornerRadius">16dp</item>
        <item name="android:paddingStart">24dp</item>
        <item name="android:paddingEnd">24dp</item>
        <item name="android:minHeight">56dp</item>
        <item name="strokeColor">@color/white</item>
        <item name="strokeWidth">2dp</item>
        <item name="android:textColor">@color/white</item>
        <item name="android:textSize">16sp</item>
        <item name="android:fontFamily">sans-serif-medium</item>
        <item name="android:letterSpacing">0.01</item>
    </style>

    <!-- Estilo para WebView -->
    <style name="WebViewStyle">
        <item name="android:layout_width">match_parent</item>
        <item name="android:layout_height">match_parent</item>
        <item name="android:scrollbars">vertical</item>
        <item name="android:scrollbarStyle">insideOverlay</item>
    </style>

</resources>''',

    # =============================================
    # 11. index.html (Aplicación web completa)
    # =============================================
    'abitaX_Android_Project/app/src/main/assets/index.html': '''<!DOCTYPE html>
<html lang="es" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>abitaX 🇬🇶 | SuperApp de Guinea Ecuatorial</title>
    
    <!-- Meta tags SEO -->
    <meta name="description" content="La primera superapp basada en mapas de Guinea Ecuatorial. Encuentra profesionales, propiedades y servicios en todo el país.">
    <meta name="keywords" content="Guinea Ecuatorial, servicios, construcción, alquiler, profesionales, mapa, Malabo, Bata">
    <meta name="author" content="abitaX">
    <meta name="theme-color" content="#007A33">
    
    <!-- Google Maps API -->
    <!-- REEMPLAZA CON TU CLAVE API DE GOOGLE MAPS -->
    <script src="https://maps.googleapis.com/maps/api/js?key=TU_API_KEY_AQUI&callback=initMapSystem&libraries=places" async defer></script>
    
    <!-- Fonts & Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Montserrat:wght@700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* =============================================
           VARIABLES Y CONFIGURACIÓN GLOBAL
        ============================================== */
        :root {
            /* Colores patrios */
            --verde-ge: #007A33;
            --blanco-ge: #FFFFFF;
            --rojo-ge: #CE1126;
            --azul-ge: #0055A4;
            --dorado: #FFD700;
            
            /* Colores derivados */
            --verde-claro: #E8F5E9;
            --verde-oscuro: #006028;
            --rojo-claro: #FFEBEE;
            --azul-claro: #E3F2FD;
            --dorado-oscuro: #E6C300;
            
            /* Colores de interfaz */
            --texto-oscuro: #1A1A1A;
            --texto-medio: #4A5568;
            --texto-claro: #718096;
            --fondo-claro: #F7FAFC;
            --fondo-blanco: #FFFFFF;
            --borde: #E2E8F0;
            
            /* Sombras */
            --sombra-suave: 0 4px 20px rgba(0, 0, 0, 0.08);
            --sombra-media: 0 8px 30px rgba(0, 0, 0, 0.12);
            --sombra-fuerte: 0 15px 40px rgba(0, 0, 0, 0.15);
            
            /* Bordes redondeados */
            --radio-sm: 12px;
            --radio-md: 16px;
            --radio-lg: 24px;
            --radio-xl: 32px;
            
            /* Transiciones */
            --transicion-rapida: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --transicion-lenta: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            
            /* Gradientes */
            --gradiente-verde: linear-gradient(135deg, var(--verde-ge), #009B4D);
            --gradiente-azul: linear-gradient(135deg, var(--azul-ge), #0066CC);
            --gradiente-rojo: linear-gradient(135deg, var(--rojo-ge), #E63946);
            --gradiente-dorado: linear-gradient(135deg, var(--dorado), #FFC107);
            --gradiente-hero: linear-gradient(135deg, rgba(0, 122, 51, 0.95), rgba(0, 85, 164, 0.9));
            --gradiente-verde-azul: linear-gradient(135deg, var(--verde-ge), var(--azul-ge));
        }
        
        /* =============================================
           RESET Y ESTILOS BASE
        ============================================== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            color: var(--texto-oscuro);
            background: var(--fondo-blanco);
            line-height: 1.6;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            touch-action: pan-y;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-size: 3.5rem;
            font-weight: 900;
            background: var(--gradiente-verde-azul);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        h2 {
            font-size: 2.5rem;
            color: var(--verde-oscuro);
            position: relative;
            padding-bottom: 1rem;
        }
        
        h2:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 4px;
            background: var(--gradiente-verde);
            border-radius: 2px;
        }
        
        h3 {
            font-size: 1.75rem;
            color: var(--azul-ge);
        }
        
        p {
            color: var(--texto-medio);
            margin-bottom: 1.5rem;
        }
        
        a {
            text-decoration: none;
            color: inherit;
            transition: var(--transicion-rapida);
        }
        
        ul {
            list-style: none;
        }
        
        .container {
            width: 100%;
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        .section {
            padding: 5rem 0;
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .section-header h2 {
            display: inline-block;
            margin-bottom: 1rem;
        }
        
        .section-header p {
            max-width: 700px;
            margin: 0 auto;
            font-size: 1.1rem;
            color: var(--texto-claro);
        }
        
        /* =============================================
           BOTONES
        ============================================== */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            padding: 1rem 2rem;
            border-radius: var(--radio-md);
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: var(--transicion-rapida);
            border: none;
            outline: none;
            position: relative;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
        }
        
        .btn:active {
            transform: scale(0.98);
        }
        
        .btn:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: 0.5s;
        }
        
        .btn:hover:before {
            left: 100%;
        }
        
        .btn-primary {
            background: var(--gradiente-verde);
            color: white;
            box-shadow: 0 4px 15px rgba(0, 122, 51, 0.3);
        }
        
        .btn-primary:hover, .btn-primary:active {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 122, 51, 0.4);
        }
        
        .btn-secondary {
            background: var(--gradiente-azul);
            color: white;
            box-shadow: 0 4px 15px rgba(0, 85, 164, 0.3);
        }
        
        .btn-secondary:hover, .btn-secondary:active {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 85, 164, 0.4);
        }
        
        .btn-outline {
            background: transparent;
            color: var(--verde-ge);
            border: 2px solid var(--verde-ge);
        }
        
        .btn-outline:hover, .btn-outline:active {
            background: var(--verde-ge);
            color: white;
            transform: translateY(-3px);
        }
        
        .btn-lg {
            padding: 1.25rem 2.5rem;
            font-size: 1.1rem;
            border-radius: var(--radio-lg);
        }
        
        .btn-icon {
            width: 2.5rem;
            height: 2.5rem;
            padding: 0;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        
        /* =============================================
           HEADER Y NAVEGACIÓN
        ============================================== */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 122, 51, 0.1);
            padding: 1rem 0;
            transition: var(--transicion-rapida);
            -webkit-backdrop-filter: blur(10px);
        }
        
        .header.scrolled {
            padding: 0.75rem 0;
            box-shadow: var(--sombra-suave);
        }
        
        .nav-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        /* Logo */
        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }
        
        .logo-icon {
            width: 48px;
            height: 48px;
            background: var(--gradiente-verde);
            border-radius: var(--radio-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-family: 'Montserrat', sans-serif;
            font-weight: 900;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 122, 51, 0.3);
        }
        
        .logo-text {
            font-family: 'Montserrat', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            background: var(--gradiente-verde-azul);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            position: relative;
        }
        
        .logo-text:after {
            content: '🇬🇶';
            position: absolute;
            top: -5px;
            right: -35px;
            font-size: 1.5rem;
        }
        
        /* Navegación */
        .nav-links {
            display: flex;
            align-items: center;
            gap: 2rem;
        }
        
        .nav-link {
            position: relative;
            font-weight: 600;
            color: var(--texto-medio);
            padding: 0.5rem 0;
            transition: var(--transicion-rapida);
        }
        
        .nav-link:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 3px;
            background: var(--gradiente-verde);
            border-radius: 2px;
            transition: var(--transicion-rapida);
        }
        
        .nav-link:hover, .nav-link.active {
            color: var(--verde-ge);
        }
        
        .nav-link:hover:after, .nav-link.active:after {
            width: 100%;
        }
        
        /* Botones de autenticación */
        .auth-buttons {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .btn-login {
            background: transparent;
            color: var(--verde-ge);
            padding: 0.75rem 1.5rem;
        }
        
        .btn-register {
            background: var(--gradiente-verde);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radio-md);
        }
        
        /* Menú móvil */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--verde-ge);
            cursor: pointer;
            padding: 0.5rem;
        }
        
        /* =============================================
           HERO SECTION
        ============================================== */
        .hero {
            padding-top: 8rem;
            padding-bottom: 5rem;
            background: var(--gradiente-hero);
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .hero:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%);
        }
        
        .hero-content {
            position: relative;
            z-index: 1;
            text-align: center;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .hero h1 {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #FFFFFF, var(--dorado));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .hero-subtitle {
            font-size: 1.5rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 3rem;
            line-height: 1.6;
        }
        
        .hero-actions {
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            margin-top: 3rem;
        }
        
        .hero-stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 2rem;
            margin-top: 5rem;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: var(--radio-lg);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--dorado);
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* =============================================
           SERVICIOS DESTACADOS
        ============================================== */
        .services-section {
            background: var(--fondo-claro);
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .service-card {
            background: var(--fondo-blanco);
            border-radius: var(--radio-lg);
            padding: 2rem;
            box-shadow: var(--sombra-suave);
            transition: var(--transicion-rapida);
            border: 1px solid var(--borde);
            position: relative;
            overflow: hidden;
        }
        
        .service-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: var(--gradiente-verde);
        }
        
        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: var(--sombra-media);
        }
        
        .service-icon {
            width: 70px;
            height: 70px;
            border-radius: var(--radio-md);
            background: var(--verde-claro);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: var(--verde-ge);
        }
        
        .service-title {
            font-size: 1.5rem;
            color: var(--verde-oscuro);
            margin-bottom: 1rem;
        }
        
        .service-features {
            margin: 1.5rem 0;
        }
        
        .service-features li {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
            color: var(--texto-medio);
        }
        
        .service-features li:before {
            content: '✓';
            color: var(--verde-ge);
            font-weight: bold;
        }
        
        .service-price {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--verde-ge);
            margin: 1.5rem 0;
        }
        
        /* =============================================
           CATEGORÍAS PROFESIONALES
        ============================================== */
        .categories-section {
            background: var(--fondo-blanco);
        }
        
        .categories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 3rem;
        }
        
        .category-card {
            background: var(--fondo-blanco);
            border-radius: var(--radio-lg);
            padding: 2rem;
            text-align: center;
            box-shadow: var(--sombra-suave);
            transition: var(--transicion-rapida);
            border: 2px solid transparent;
        }
        
        .category-card:hover {
            border-color: var(--verde-ge);
            transform: translateY(-5px);
            box-shadow: var(--sombra-media);
        }
        
        .category-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .category-title {
            font-size: 1.25rem;
            color: var(--verde-oscuro);
            margin-bottom: 0.75rem;
        }
        
        .category-count {
            color: var(--texto-claro);
            font-size: 0.9rem;
        }
        
        /* =============================================
           MAPA INTERACTIVO
        ============================================== */
        .map-section {
            background: linear-gradient(135deg, var(--fondo-claro) 0%, #FFFFFF 100%);
            padding: 4rem 0;
        }
        
        .map-container {
            background: var(--fondo-blanco);
            border-radius: var(--radio-lg);
            box-shadow: var(--sombra-media);
            overflow: hidden;
            margin-top: 2rem;
        }
        
        .map-controls {
            padding: 1.5rem;
            border-bottom: 1px solid var(--borde);
            background: var(--fondo-blanco);
        }
        
        .search-box {
            display: flex;
            align-items: center;
            background: var(--fondo-claro);
            border-radius: var(--radio-md);
            padding: 0.75rem 1.5rem;
            margin-bottom: 1rem;
        }
        
        .search-box i {
            color: var(--texto-claro);
            margin-right: 1rem;
        }
        
        .search-box input {
            flex: 1;
            border: none;
            background: transparent;
            font-size: 1rem;
            color: var(--texto-oscuro);
            outline: none;
        }
        
        .search-box input::placeholder {
            color: var(--texto-claro);
        }
        
        .map-filters {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .filter-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .filter-group label {
            font-weight: 500;
            color: var(--texto-medio);
        }
        
        .filter-group select {
            padding: 0.5rem 1rem;
            border: 1px solid var(--borde);
            border-radius: var(--radio-sm);
            background: var(--fondo-blanco);
            color: var(--texto-medio);
            cursor: pointer;
            min-width: 150px;
        }
        
        .filter-group select:focus {
            outline: none;
            border-color: var(--verde-ge);
        }
        
        .map-wrapper {
            display: flex;
            height: 600px;
            position: relative;
        }
        
        .google-map {
            flex: 1;
            background: var(--fondo-claro);
            position: relative;
        }
        
        #google-map {
            width: 100%;
            height: 100%;
        }
        
        .map-sidebar {
            width: 350px;
            background: var(--fondo-blanco);
            border-left: 1px solid var(--borde);
            display: flex;
            flex-direction: column;
        }
        
        .sidebar-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--borde);
        }
        
        .sidebar-header h4 {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--verde-oscuro);
            margin-bottom: 0.5rem;
        }
        
        #results-count {
            font-size: 0.9rem;
            color: var(--texto-claro);
        }
        
        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
            -webkit-overflow-scrolling: touch;
        }
        
        .map-result-item {
            background: var(--fondo-claro);
            border-radius: var(--radio-md);
            padding: 1.25rem;
            margin-bottom: 1rem;
            cursor: pointer;
            transition: var(--transicion-rapida);
            border: 1px solid transparent;
        }
        
        .map-result-item:hover, .map-result-item:active {
            background: var(--verde-claro);
            border-color: var(--verde-ge);
            transform: translateX(5px);
        }
        
        .map-result-item.active {
            background: var(--verde-claro);
            border-color: var(--verde-ge);
        }
        
        .result-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }
        
        .result-category {
            font-size: 0.8rem;
            padding: 0.25rem 0.75rem;
            background: var(--azul-claro);
            color: var(--azul-ge);
            border-radius: 20px;
            font-weight: 500;
        }
        
        .result-price {
            color: var(--verde-ge);
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        .result-title {
            font-weight: 600;
            color: var(--texto-oscuro);
            margin-bottom: 0.5rem;
        }
        
        .result-location {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--texto-claro);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        .result-features {
            display: flex;
            gap: 1rem;
            font-size: 0.85rem;
            color: var(--texto-medio);
        }
        
        .result-features span {
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .empty-results {
            text-align: center;
            padding: 3rem 1rem;
            color: var(--texto-claro);
        }
        
        .empty-results i {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        .map-loading {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 3px solid var(--fondo-claro);
            border-top-color: var(--verde-ge);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* =============================================
           RESPONSIVE DESIGN
        ============================================== */
        @media (max-width: 1024px) {
            h1 { font-size: 3rem; }
            h2 { font-size: 2.25rem; }
            
            .hero-stats {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .map-wrapper {
                flex-direction: column;
                height: 800px;
            }
            
            .map-sidebar {
                width: 100%;
                height: 300px;
                border-left: none;
                border-top: 1px solid var(--borde);
            }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 0 1.5rem;
            }
            
            .section {
                padding: 3rem 0;
            }
            
            h1 { font-size: 2.5rem; }
            h2 { font-size: 2rem; }
            h3 { font-size: 1.5rem; }
            
            .nav-links {
                display: none;
                position: fixed;
                top: 70px;
                left: 0;
                right: 0;
                background: white;
                flex-direction: column;
                padding: 2rem;
                box-shadow: var(--sombra-media);
                z-index: 999;
            }
            
            .nav-links.active {
                display: flex;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .hero-actions {
                flex-direction: column;
                align-items: center;
                gap: 1rem;
            }
            
            .btn-lg {
                width: 100%;
                max-width: 300px;
            }
            
            .map-filters {
                flex-direction: column;
                align-items: stretch;
            }
            
            .filter-group {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .filter-group select {
                width: 100%;
            }
            
            .map-wrapper {
                height: 700px;
            }
        }
        
        @media (max-width: 480px) {
            .hero h1 { font-size: 2rem; }
            .hero-subtitle { font-size: 1.25rem; }
            
            .services-grid,
            .properties-grid,
            .categories-grid {
                grid-template-columns: 1fr;
            }
            
            .hero-stats {
                grid-template-columns: 1fr;
                padding: 1rem;
                gap: 1rem;
            }
            
            .stat-number {
                font-size: 1.75rem;
            }
            
            .container {
                padding: 0 1rem;
            }
        }
        
        /* Optimizaciones para WebView Android */
        @media (hover: none) and (pointer: coarse) {
            .btn, .nav-link, .map-result-item, .category-card, .service-card, .property-card {
                cursor: pointer;
                -webkit-tap-highlight-color: rgba(0, 122, 51, 0.1);
            }
            
            .btn:active {
                opacity: 0.8;
                transform: scale(0.98);
            }
            
            input, select, textarea {
                font-size: 16px !important; /* Prevenir zoom en iOS */
            }
        }
        
        /* Prevenir selección de texto en botones */
        .btn, .nav-link {
            user-select: none;
            -webkit-user-select: none;
        }
        
        /* Mejorar scroll en WebView */
        .sidebar-content, .map-result-item {
            -webkit-overflow-scrolling: touch;
        }
        
        /* Estilo para scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--fondo-claro);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--verde-ge);
            border-radius: 3px;
        }
        
        /* =============================================
           ANIMACIONES
        ============================================== */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-on-scroll.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* =============================================
           UTILITIES
        ============================================== */
        .text-center { text-align: center; }
        .mt-1 { margin-top: 1rem; }
        .mt-2 { margin-top: 2rem; }
        .mt-3 { margin-top: 3rem; }
        .mb-1 { margin-bottom: 1rem; }
        .mb-2 { margin-bottom: 2rem; }
        .mb-3 { margin-bottom: 3rem; }
        .hidden { display: none !important; }
        .visible { display: block !important; }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header" id="header">
        <div class="container">
            <nav class="nav-container">
                <!-- Logo -->
                <a href="#inicio" class="logo">
                    <div class="logo-icon">AX</div>
                    <div class="logo-text">abitaX</div>
                </a>
                
                <!-- Navegación -->
                <div class="nav-links" id="nav-links">
                    <a href="#inicio" class="nav-link active" onclick="closeMobileMenu()">Inicio</a>
                    <a href="#servicios" class="nav-link" onclick="closeMobileMenu()">Servicios</a>
                    <a href="#propiedades" class="nav-link" onclick="closeMobileMenu()">Propiedades</a>
                    <a href="#profesionales" class="nav-link" onclick="closeMobileMenu()">Profesionales</a>
                    <a href="#mapa" class="nav-link" onclick="closeMobileMenu()">Mapa</a>
                    <a href="#como-funciona" class="nav-link" onclick="closeMobileMenu()">¿Cómo funciona?</a>
                </div>
                
                <!-- Botones de Autenticación -->
                <div class="auth-buttons" id="auth-buttons">
                    <button class="btn btn-login" onclick="openModal('login')">
                        <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
                    </button>
                    <button class="btn btn-register" onclick="openModal('register')">
                        <i class="fas fa-user-plus"></i> Registrarse
                    </button>
                </div>
                
                <!-- Menú móvil -->
                <button class="mobile-menu-btn" id="mobile-menu-btn" onclick="toggleMobileMenu()">
                    <i class="fas fa-bars"></i>
                </button>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="inicio">
        <div class="container">
            <div class="hero-content">
                <h1 class="animate-on-scroll">
                    Conectamos Guinea Ecuatorial 🇬🇶<br>
                    <span style="color: var(--dorado);">con los mejores profesionales</span>
                </h1>
                <p class="hero-subtitle animate-on-scroll">
                    La primera superapp basada en mapas que integra profesionales de construcción, 
                    servicios de mantenimiento y propiedades en una sola plataforma moderna y segura.
                </p>
                
                <div class="hero-actions animate-on-scroll">
                    <button class="btn btn-primary btn-lg" onclick="scrollToServices()">
                        <i class="fas fa-search"></i> Buscar Servicios
                    </button>
                    <button class="btn btn-secondary btn-lg" onclick="openMapSection()">
                        <i class="fas fa-map-marked-alt"></i> Explorar Mapa
                    </button>
                    <a href="#como-funciona" class="btn btn-outline btn-lg">
                        <i class="fas fa-play-circle"></i> ¿Cómo funciona?
                    </a>
                </div>
                
                <div class="hero-stats animate-on-scroll">
                    <div class="stat-item">
                        <div class="stat-number">500+</div>
                        <div class="stat-label">Profesionales</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">1,200+</div>
                        <div class="stat-label">Servicios Activos</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">800+</div>
                        <div class="stat-label">Propiedades</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">98%</div>
                        <div class="stat-label">Clientes Satisfechos</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Servicios Destacados -->
    <section class="section services-section" id="servicios">
        <div class="container">
            <div class="section-header">
                <h2>Servicios Destacados</h2>
                <p>Los mejores profesionales verificados por nuestra comunidad</p>
            </div>
            
            <div class="services-grid">
                <!-- Servicio 1: Construcción -->
                <div class="service-card animate-on-scroll">
                    <div class="service-icon">
                        <i class="fas fa-hard-hat"></i>
                    </div>
                    <h3 class="service-title">Construcción y Reformas</h3>
                    <p>Profesionales certificados para todo tipo de proyectos de construcción y reformas.</p>
                    
                    <ul class="service-features">
                        <li>Albañiles certificados</li>
                        <li>Constructores generales</li>
                        <li>Arquitectos e ingenieros</li>
                        <li>Supervisores de obra</li>
                    </ul>
                    
                    <div class="service-price">Desde 25,000 XAF/día</div>
                    
                    <button class="btn btn-primary" onclick="selectService('construccion')">
                        <i class="fas fa-search"></i> Ver Profesionales
                    </button>
                </div>
                
                <!-- Servicio 2: Mantenimiento -->
                <div class="service-card animate-on-scroll">
                    <div class="service-icon" style="background: var(--azul-claro); color: var(--azul-ge);">
                        <i class="fas fa-tools"></i>
                    </div>
                    <h3 class="service-title">Mantenimiento Hogar</h3>
                    <p>Soluciones rápidas y confiables para el mantenimiento de tu hogar.</p>
                    
                    <ul class="service-features">
                        <li>Electricistas certificados</li>
                        <li>Fontaneros especializados</li>
                        <li>Técnicos de aire acondicionado</li>
                        <li>Pintores profesionales</li>
                    </ul>
                    
                    <div class="service-price">Desde 15,000 XAF/servicio</div>
                    
                    <button class="btn btn-primary" onclick="selectService('mantenimiento')">
                        <i class="fas fa-search"></i> Ver Profesionales
                    </button>
                </div>
                
                <!-- Servicio 3: Inmobiliaria -->
                <div class="service-card animate-on-scroll">
                    <div class="service-icon" style="background: var(--rojo-claro); color: var(--rojo-ge);">
                        <i class="fas fa-home"></i>
                    </div>
                    <h3 class="service-title">Inmobiliaria</h3>
                    <p>Encuentra la propiedad perfecta o alquila espacios temporales.</p>
                    
                    <ul class="service-features">
                        <li>Casas y apartamentos</li>
                        <li>Alquiler por día/hora</li>
                        <li>Terrenos y locales</li>
                        <li>Asesoría legal</li>
                    </ul>
                    
                    <div class="service-price">Desde 75,000 XAF/noche</div>
                    
                    <button class="btn btn-primary" onclick="selectService('inmobiliaria')">
                        <i class="fas fa-search"></i> Ver Propiedades
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- Categorías Profesionales -->
    <section class="section categories-section" id="profesionales">
        <div class="container">
            <div class="section-header">
                <h2>Encuentra por Categoría</h2>
                <p>Especialistas en cada área para todas tus necesidades</p>
            </div>
            
            <div class="categories-grid">
                <!-- Categoría 1 -->
                <a href="#mapa" class="category-card animate-on-scroll" onclick="filterCategory('albanil')">
                    <div class="category-icon">👷</div>
                    <h3 class="category-title">Albañiles</h3>
                    <p class="category-count">45 profesionales disponibles</p>
                </a>
                
                <!-- Categoría 2 -->
                <a href="#mapa" class="category-card animate-on-scroll" onclick="filterCategory('electricista')">
                    <div class="category-icon">⚡</div>
                    <h3 class="category-title">Electricistas</h3>
                    <p class="category-count">32 profesionales disponibles</p>
                </a>
                
                <!-- Categoría 3 -->
                <a href="#mapa" class="category-card animate-on-scroll" onclick="filterCategory('fontanero')">
                    <div class="category-icon">🚰</div>
                    <h3 class="category-title">Fontaneros</h3>
                    <p class="category-count">28 profesionales disponibles</p>
                </a>
                
                <!-- Categoría 4 -->
                <a href="#mapa" class="category-card animate-on-scroll" onclick="filterCategory('arquitecto')">
                    <div class="category-icon">📐</div>
                    <h3 class="category-title">Arquitectos</h3>
                    <p class="category-count">18 profesionales disponibles</p>
                </a>
                
                <!-- Categoría 5 -->
                <a href="#mapa" class="category-card animate-on-scroll" onclick="filterCategory('pintor')">
                    <div class="category-icon">🎨</div>
                    <h3 class="category-title">Pintores</h3>
                    <p class="category-count">24 profesionales disponibles</p>
                </a>
                
                <!-- Categoría 6 -->
                <a href="#mapa" class="category-card animate-on-scroll" onclick="filterCategory('frigorista')">
                    <div class="category-icon">❄️</div>
                    <h3 class="category-title">Frigoristas</h3>
                    <p class="category-count">15 profesionales disponibles</p>
                </a>
            </div>
        </div>
    </section>

    <!-- Mapa Interactivo -->
    <section class="section map-section" id="mapa">
        <div class="container">
            <div class="section-header">
                <h2>Explora Proveedores en el Mapa</h2>
                <p>Encuentra profesionales y propiedades por ubicación en toda Guinea Ecuatorial</p>
            </div>
            
            <div class="map-container">
                <!-- Barra de búsqueda y filtros -->
                <div class="map-controls">
                    <div class="search-box">
                        <i class="fas fa-search"></i>
                        <input type="text" id="map-search" placeholder="Buscar por ciudad, servicio o profesional..." 
                               onkeypress="if(event.key=='Enter') searchOnMap()">
                        <button class="btn btn-icon" onclick="searchOnMap()">
                            <i class="fas fa-arrow-right"></i>
                        </button>
                    </div>
                    
                    <div class="map-filters">
                        <div class="filter-group">
                            <label><i class="fas fa-filter"></i> Filtrar por:</label>
                            <select id="category-filter" onchange="filterMapMarkers()">
                                <option value="all">Todas las categorías</option>
                                <option value="construccion">Construcción</option>
                                <option value="mantenimiento">Mantenimiento</option>
                                <option value="inmobiliaria">Inmobiliaria</option>
                                <option value="albanil">Albañiles</option>
                                <option value="electricista">Electricistas</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <select id="city-filter" onchange="filterMapMarkers()">
                                <option value="all">Todas las ciudades</option>
                                <option value="malabo">Malabo</option>
                                <option value="bata">Bata</option>
                                <option value="ebebiyin">Ebebiyín</option>
                            </select>
                        </div>
                        
                        <button class="btn btn-outline" onclick="getUserLocation()">
                            <i class="fas fa-location-arrow"></i> Mi Ubicación
                        </button>
                    </div>
                </div>
                
                <!-- Contenedor del Mapa -->
                <div class="map-wrapper">
                    <div id="google-map" class="google-map"></div>
                    
                    <!-- Panel de resultados -->
                    <div class="map-sidebar">
                        <div class="sidebar-header">
                            <h4><i class="fas fa-map-pin"></i> Resultados Cercanos</h4>
                            <span id="results-count">0 proveedores encontrados</span>
                        </div>
                        <div class="sidebar-content" id="map-results">
                            <!-- Los resultados se cargarán aquí dinámicamente -->
                            <div class="empty-results">
                                <i class="fas fa-map-marker-alt"></i>
                                <p>Usa el mapa para explorar proveedores</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Capa de carga -->
                <div id="map-loading" class="map-loading">
                    <div class="loading-spinner"></div>
                    <p>Cargando mapa...</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Propiedades Destacadas -->
    <section class="section properties-section" id="propiedades">
        <div class="container">
            <div class="section-header">
                <h2>Propiedades Destacadas</h2>
                <p>Las mejores propiedades disponibles en Guinea Ecuatorial</p>
            </div>
            
            <div class="properties-grid">
                <!-- Propiedad 1 -->
                <div class="property-card animate-on-scroll">
                    <div class="property-image" style="background: var(--gradiente-azul);">
                        <div class="property-badge">Alquiler por Día</div>
                    </div>
                    <div class="property-content">
                        <h3>Villa Moderna en Malabo</h3>
                        <div class="property-price">450,000 XAF/día</div>
                        <div class="property-location">
                            <i class="fas fa-map-marker-alt"></i>
                            Malabo, Guinea Ecuatorial
                        </div>
                        <p>Exclusiva villa con piscina privada, jardín y todas las comodidades modernas.</p>
                        
                        <div class="property-features">
                            <div class="feature">
                                <i class="fas fa-bed"></i>
                                <span>4 Habitaciones</span>
                            </div>
                            <div class="feature">
                                <i class="fas fa-bath"></i>
                                <span>3 Baños</span>
                            </div>
                            <div class="feature">
                                <i class="fas fa-ruler-combined"></i>
                                <span>300 m²</span>
                            </div>
                        </div>
                        
                        <button class="btn btn-primary" style="width: 100%;" onclick="viewProperty(1)">
                            <i class="fas fa-eye"></i> Ver Detalles
                        </button>
                    </div>
                </div>
                
                <!-- Propiedad 2 -->
                <div class="property-card animate-on-scroll">
                    <div class="property-image" style="background: var(--gradiente-verde);">
                        <div class="property-badge" style="background: var(--verde-ge);">Venta</div>
                    </div>
                    <div class="property-content">
                        <h3>Apartamento Ejecutivo Bata</h3>
                        <div class="property-price">85,000,000 XAF</div>
                        <div class="property-location">
                            <i class="fas fa-map-marker-alt"></i>
                            Bata, Guinea Ecuatorial
                        </div>
                        <p>Moderno apartamento en zona exclusiva, ideal para inversión o vivienda.</p>
                        
                        <div class="property-features">
                            <div class="feature">
                                <i class="fas fa-bed"></i>
                                <span>3 Habitaciones</span>
                            </div>
                            <div class="feature">
                                <i class="fas fa-bath"></i>
                                <span>2 Baños</span>
                            </div>
                            <div class="feature">
                                <i class="fas fa-ruler-combined"></i>
                                <span>120 m²</span>
                            </div>
                        </div>
                        
                        <button class="btn btn-primary" style="width: 100%;" onclick="viewProperty(2)">
                            <i class="fas fa-eye"></i> Ver Detalles
                        </button>
                    </div>
                </div>
                
                <!-- Propiedad 3 -->
                <div class="property-card animate-on-scroll">
                    <div class="property-image" style="background: var(--gradiente-rojo);">
                        <div class="property-badge" style="background: var(--azul-ge);">Alquiler Mensual</div>
                    </div>
                    <div class="property-content">
                        <h3>Casa Familiar Ebebiyín</h3>
                        <div class="property-price">350,000 XAF/mes</div>
                        <div class="property-location">
                            <i class="fas fa-map-marker-alt"></i>
                            Ebebiyín, Guinea Ecuatorial
                        </div>
                        <p>Amplia casa familiar perfecta para estancias largas, con garaje y jardín.</p>
                        
                        <div class="property-features">
                            <div class="feature">
                                <i class="fas fa-bed"></i>
                                <span>5 Habitaciones</span>
                            </div>
                            <div class="feature">
                                <i class="fas fa-bath"></i>
                                <span>3 Baños</span>
                            </div>
                            <div class="feature">
                                <i class="fas fa-ruler-combined"></i>
                                <span>250 m²</span>
                            </div>
                        </div>
                        
                        <button class="btn btn-primary" style="width: 100%;" onclick="viewProperty(3)">
                            <i class="fas fa-eye"></i> Ver Detalles
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Cómo Funciona -->
    <section class="section how-it-works" id="como-funciona">
        <div class="container">
            <div class="section-header">
                <h2>¿Cómo funciona abitaX?</h2>
                <p>Encuentra y contrata servicios en solo 4 pasos simples</p>
            </div>
            
            <div class="steps-container">
                <!-- Paso 1 -->
                <div class="step animate-on-scroll">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <h3 class="step-title">Busca</h3>
                        <p>Encuentra profesionales o propiedades usando nuestro mapa interactivo o filtros avanzados.</p>
                    </div>
                </div>
                
                <!-- Paso 2 -->
                <div class="step animate-on-scroll">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <h3 class="step-title">Compara</h3>
                        <p>Revisa perfiles, precios, calificaciones y portafolios para tomar la mejor decisión.</p>
                    </div>
                </div>
                
                <!-- Paso 3 -->
                <div class="step animate-on-scroll">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <h3 class="step-title">Contacta</h3>
                        <p>Usa nuestro chat seguro para comunicarte directamente con el profesional o propietario.</p>
                    </div>
                </div>
                
                <!-- Paso 4 -->
                <div class="step animate-on-scroll">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <h3 class="step-title">Contrata</h3>
                        <p>Realiza el pago seguro a través de nuestra plataforma y recibe confirmación inmediata.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Final -->
    <section class="cta-section" id="contacto">
        <div class="container">
            <div class="cta-content">
                <h2 class="animate-on-scroll">¿Listo para transformar tu experiencia?</h2>
                <p class="animate-on-scroll">
                    Únete a miles de usuarios que ya confían en abitaX para encontrar los mejores profesionales y propiedades en Guinea Ecuatorial.
                </p>
                
                <div class="cta-buttons animate-on-scroll">
                    <button class="btn btn-primary btn-lg" onclick="openModal('register')">
                        <i class="fas fa-rocket"></i> Comenzar Ahora
                    </button>
                    <button class="btn btn-outline btn-lg" style="background: rgba(255,255,255,0.1); border-color: white; color: white;" onclick="openMapSection()">
                        <i class="fas fa-map-marked-alt"></i> Explorar Mapa
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <!-- Columna 1 -->
                <div>
                    <div class="footer-logo">abitaX</div>
                    <p class="footer-description">
                        La primera superapp basada en mapas de Guinea Ecuatorial. 
                        Conectamos personas, lugares y servicios para impulsar el desarrollo del país.
                    </p>
                    
                    <div class="social-links">
                        <a href="#" class="social-link" title="Facebook">
                            <i class="fab fa-facebook-f"></i>
                        </a>
                        <a href="#" class="social-link" title="Twitter">
                            <i class="fab fa-twitter"></i>
                        </a>
                        <a href="#" class="social-link" title="Instagram">
                            <i class="fab fa-instagram"></i>
                        </a>
                        <a href="#" class="social-link" title="LinkedIn">
                            <i class="fab fa-linkedin-in"></i>
                        </a>
                        <a href="#" class="social-link" title="WhatsApp">
                            <i class="fab fa-whatsapp"></i>
                        </a>
                    </div>
                </div>
                
                <!-- Columna 2 -->
                <div>
                    <h3 class="footer-title">Enlaces Rápidos</h3>
                    <ul class="footer-links">
                        <li><a href="#inicio">Inicio</a></li>
                        <li><a href="#servicios">Servicios</a></li>
                        <li><a href="#propiedades">Propiedades</a></li>
                        <li><a href="#profesionales">Profesionales</a></li>
                        <li><a href="#mapa">Mapa</a></li>
                        <li><a href="#como-funciona">¿Cómo funciona?</a></li>
                    </ul>
                </div>
                
                <!-- Columna 3 -->
                <div>
                    <h3 class="footer-title">Categorías</h3>
                    <ul class="footer-links">
                        <li><a href="#mapa" onclick="filterCategory('albanil')">👷 Albañiles</a></li>
                        <li><a href="#mapa" onclick="filterCategory('electricista')">⚡ Electricistas</a></li>
                        <li><a href="#mapa" onclick="filterCategory('fontanero')">🚰 Fontaneros</a></li>
                        <li><a href="#mapa" onclick="filterCategory('arquitecto')">📐 Arquitectos</a></li>
                        <li><a href="#mapa" onclick="filterCategory('pintor')">🎨 Pintores</a></li>
                        <li><a href="#mapa" onclick="filterCategory('frigorista')">❄️ Frigoristas</a></li>
                    </ul>
                </div>
                
                <!-- Columna 4 -->
                <div>
                    <h3 class="footer-title">Contacto</h3>
                    <ul class="footer-links">
                        <li><i class="fas fa-map-marker-alt"></i> Malabo, Guinea Ecuatorial</li>
                        <li><i class="fas fa-phone"></i> +240 222 123 456</li>
                        <li><i class="fas fa-envelope"></i> info@abitax.ge</li>
                        <li><i class="fas fa-clock"></i> Lun - Vie: 8:00 - 18:00</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2024 abitaX. Todos los derechos reservados. | 
                    <a href="#">Términos y Condiciones</a> | 
                    <a href="#">Política de Privacidad</a>
                </p>
                <p class="mt-1" style="font-size: 0.8rem; color: rgba(255,255,255,0.4);">
                    🇬🇶 Inspirado en los colores y valores de Guinea Ecuatorial
                </p>
            </div>
        </div>
    </footer>

    <!-- Modal de Login -->
    <div class="modal-overlay" id="login-modal">
        <div class="modal">
            <div class="modal-header">
                <h3><i class="fas fa-sign-in-alt"></i> Iniciar Sesión</h3>
                <button class="modal-close" onclick="closeModal('login')">×</button>
            </div>
            <div class="modal-body">
                <form id="login-form">
                    <div class="form-group">
                        <label>Email o Teléfono</label>
                        <input type="text" class="form-input" placeholder="tu@email.com o +240 XXX XXX XXX" required>
                    </div>
                    <div class="form-group">
                        <label>Contraseña</label>
                        <input type="password" class="form-input" placeholder="••••••••" required>
                    </div>
                    <div class="form-options">
                        <label>
                            <input type="checkbox"> Recordar sesión
                        </label>
                        <a href="#">¿Olvidaste tu contraseña?</a>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width: 100%;">
                        <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
                    </button>
                    <div class="form-divider">
                        <span>o continuar con</span>
                    </div>
                    <div class="social-login">
                        <button type="button" class="btn btn-google">
                            <i class="fab fa-google"></i> Google
                        </button>
                        <button type="button" class="btn btn-facebook">
                            <i class="fab fa-facebook-f"></i> Facebook
                        </button>
                    </div>
                    <div class="form-footer">
                        ¿No tienes cuenta? <a href="#" onclick="switchToRegister()">Regístrate aquí</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <!-- Modal de Registro -->
    <div class="modal-overlay" id="register-modal">
        <div class="modal">
            <div class="modal-header">
                <h3><i class="fas fa-user-plus"></i> Crear Cuenta</h3>
                <button class="modal-close" onclick="closeModal('register')">×</button>
            </div>
            <div class="modal-body">
                <form id="register-form">
                    <div class="form-tabs">
                        <button type="button" class="form-tab active">Usuario</button>
                        <button type="button" class="form-tab">Profesional</button>
                    </div>
                    
                    <div class="form-group">
                        <label>Nombre Completo *</label>
                        <input type="text" class="form-input" placeholder="Juan Pérez" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Email *</label>
                        <input type="email" class="form-input" placeholder="juan@email.com" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Teléfono *</label>
                        <input type="tel" class="form-input" placeholder="+240 XXX XXX XXX" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Contraseña *</label>
                        <input type="password" class="form-input" placeholder="••••••••" required>
                        <div class="password-strength">
                            <div class="strength-bar"></div>
                            <span>Seguridad: baja</span>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Confirmar Contraseña *</label>
                        <input type="password" class="form-input" placeholder="••••••••" required>
                    </div>
                    
                    <div class="form-checkbox">
                        <input type="checkbox" id="terms" required>
                        <label for="terms">
                            Acepto los <a href="#">Términos y Condiciones</a> y la <a href="#">Política de Privacidad</a>
                        </label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" style="width: 100%;">
                        <i class="fas fa-user-plus"></i> Crear Cuenta
                    </button>
                    
                    <div class="form-footer">
                        ¿Ya tienes cuenta? <a href="#" onclick="switchToLogin()">Inicia sesión</a>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        // =============================================
        // VARIABLES GLOBALES
        // =============================================
        let currentUser = null;
        let map = null;
        let markers = [];
        let infoWindow = null;
        let geocoder = null;
        let userMarker = null;
        
        // Datos de ejemplo para proveedores en Guinea Ecuatorial
        const providersData = [
            {
                id: 1,
                name: "Constructor Experto Malabo",
                category: "construccion",
                subcategory: "albanil",
                city: "malabo",
                lat: 3.7521,
                lng: 8.7737,
                price: "30,000 XAF/día",
                description: "Especialista en construcción de viviendas y reformas integrales",
                rating: 4.8,
                phone: "+240 222 111 111",
                features: ["Certificado", "10+ años exp", "Garantía"]
            },
            {
                id: 2,
                name: "Electricista Certificado Bata",
                category: "mantenimiento",
                subcategory: "electricista",
                city: "bata",
                lat: 1.8650,
                lng: 9.7679,
                price: "25,000 XAF/servicio",
                description: "Instalaciones eléctricas residenciales e industriales",
                rating: 4.9,
                phone: "+240 333 222 222",
                features: ["Urgencias 24h", "Certificado", "5 años exp"]
            },
            {
                id: 3,
                name: "Villa Moderna Malabo",
                category: "inmobiliaria",
                subcategory: "alquiler",
                city: "malabo",
                lat: 3.7450,
                lng: 8.7830,
                price: "450,000 XAF/día",
                description: "Villa exclusiva con piscina y todas las comodidades",
                rating: 4.7,
                phone: "+240 555 444 444",
                features: ["4 habitaciones", "Piscina", "WiFi"]
            },
            {
                id: 4,
                name: "Fontanero Profesional Ebebiyín",
                category: "mantenimiento",
                subcategory: "fontanero",
                city: "ebebiyin",
                lat: 2.1511,
                lng: 11.3353,
                price: "20,000 XAF/servicio",
                description: "Reparaciones e instalaciones de fontanería residencial",
                rating: 4.6,
                phone: "+240 666 777 888",
                features: ["Urgencias", "Material incluido", "Garantía"]
            },
            {
                id: 5,
                name: "Apartamento Ejecutivo Bata",
                category: "inmobiliaria",
                subcategory: "venta",
                city: "bata",
                lat: 1.8600,
                lng: 9.7700,
                price: "85,000,000 XAF",
                description: "Apartamento moderno en zona exclusiva de Bata",
                rating: 4.8,
                phone: "+240 777 888 999",
                features: ["3 habitaciones", "Seguridad 24h", "Vista al mar"]
            },
            {
                id: 6,
                name: "Arquitecto e Ingeniero Malabo",
                category: "construccion",
                subcategory: "arquitecto",
                city: "malabo",
                lat: 3.7580,
                lng: 8.7800,
                price: "75,000 XAF/consulta",
                description: "Proyectos arquitectónicos y supervision de obras",
                rating: 4.9,
                phone: "+240 888 999 000",
                features: ["Certificado", "15+ años exp", "Diseño 3D"]
            }
        ];
        
        // =============================================
        // INICIALIZACIÓN
        // =============================================
        document.addEventListener('DOMContentLoaded', function() {
            // Configurar animaciones al hacer scroll
            setupScrollAnimations();
            
            // Configurar navegación suave
            setupSmoothScroll();
            
            // Configurar eventos del header
            setupHeaderEvents();
            
            // Configurar menú móvil
            setupMobileMenu();
            
            // Verificar autenticación
            checkAuthStatus();
            
            // Configurar formularios
            setupForms();
            
            // Configurar interacciones
            setupInteractions();
            
            // Inicializar mapa si Google Maps está disponible
            if (typeof google !== 'undefined' && google.maps) {
                setTimeout(initMap, 1000);
            } else {
                // Intentar de nuevo después de 2 segundos
                setTimeout(function() {
                    if (typeof google !== 'undefined' && google.maps) {
                        initMap();
                    } else {
                        document.getElementById('map-loading').innerHTML = 
                            '<p style="color: #CE1126; text-align: center;">Google Maps no está disponible. Verifica tu conexión a internet.</p>';
                    }
                }, 2000);
            }
        });
        
        // =============================================
        // CONFIGURACIONES GENERALES
        // =============================================
        function setupScrollAnimations() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, { threshold: 0.1 });
            
            document.querySelectorAll('.animate-on-scroll').forEach(el => {
                observer.observe(el);
            });
        }
        
        function setupSmoothScroll() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const targetId = this.getAttribute('href');
                    if (targetId === '#') return;
                    
                    const target = document.querySelector(targetId);
                    if (target) {
                        // Cerrar menú móvil si está abierto
                        closeMobileMenu();
                        
                        // Scroll suave
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                        
                        // Actualizar navegación activa
                        updateActiveNav(targetId);
                    }
                });
            });
        }
        
        function setupHeaderEvents() {
            // Header scroll effect
            window.addEventListener('scroll', function() {
                const header = document.getElementById('header');
                if (window.scrollY > 50) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
                
                // Actualizar navegación activa basada en scroll
                updateActiveNavOnScroll();
            });
        }
        
        function setupMobileMenu() {
            const mobileMenuBtn = document.getElementById('mobile-menu-btn');
            const navLinks = document.getElementById('nav-links');
            
            if (mobileMenuBtn && navLinks) {
                mobileMenuBtn.addEventListener('click', toggleMobileMenu);
                
                // Cerrar menú al hacer clic en un enlace
                navLinks.querySelectorAll('a').forEach(link => {
                    link.addEventListener('click', closeMobileMenu);
                });
            }
        }
        
        function toggleMobileMenu() {
            const navLinks = document.getElementById('nav-links');
            if (navLinks) {
                navLinks.classList.toggle('active');
            }
        }
        
        function closeMobileMenu() {
            const navLinks = document.getElementById('nav-links');
            if (navLinks) {
                navLinks.classList.remove('active');
            }
        }
        
        function updateActiveNav(targetId) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === targetId) {
                    link.classList.add('active');
                }
            });
        }
        
        function updateActiveNavOnScroll() {
            const sections = document.querySelectorAll('section[id]');
            const scrollPos = window.scrollY + 100;
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                const sectionId = '#' + section.getAttribute('id');
                
                if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                    updateActiveNav(sectionId);
                }
            });
        }
        
        function checkAuthStatus() {
            // Simular usuario autenticado (en producción esto vendría del servidor)
            const isAuthenticated = false; // Cambiar a true para ver estado autenticado
            
            if (isAuthenticated) {
                document.getElementById('auth-buttons').style.display = 'none';
                currentUser = {
                    name: 'Juan Pérez',
                    email: 'juan@ejemplo.com',
                    type: 'profesional'
                };
            }
        }
        
        function setupForms() {
            // Configurar formulario de login
            const loginForm = document.getElementById('login-form');
            if (loginForm) {
                loginForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    // Aquí iría la lógica real de login
                    showNotification('Inicio de sesión exitoso', 'success');
                    closeModal('login');
                    simulateLogin();
                });
            }
            
            // Configurar formulario de registro
            const registerForm = document.getElementById('register-form');
            if (registerForm) {
                registerForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    showNotification('Cuenta creada exitosamente', 'success');
                    closeModal('register');
                    simulateLogin();
                });
            }
        }
        
        function setupInteractions() {
            // Cerrar modales al hacer clic fuera
            document.querySelectorAll('.modal-overlay').forEach(modal => {
                modal.addEventListener('click', function(e) {
                    if (e.target === this) {
                        const modalId = this.id.replace('-modal', '');
                        closeModal(modalId);
                    }
                });
            });
        }
        
        // =============================================
        // FUNCIONES DEL MAPA
        // =============================================
        function initMap() {
            if (!document.getElementById('google-map')) return;
            
            try {
                // Configuración inicial centrada en Guinea Ecuatorial
                const mapOptions = {
                    center: { lat: 1.6139, lng: 10.4670 },
                    zoom: 9,
                    mapTypeId: 'roadmap',
                    styles: [
                        {
                            "featureType": "administrative",
                            "elementType": "labels.text.fill",
                            "stylers": [{"color": "#444444"}]
                        },
                        {
                            "featureType": "landscape",
                            "elementType": "all",
                            "stylers": [{"color": "#f2f2f2"}]
                        },
                        {
                            "featureType": "poi",
                            "elementType": "all",
                            "stylers": [{"visibility": "off"}]
                        },
                        {
                            "featureType": "road",
                            "elementType": "all",
                            "stylers": [{"saturation": -100}, {"lightness": 45}]
                        },
                        {
                            "featureType": "road.highway",
                            "elementType": "all",
                            "stylers": [{"visibility": "simplified"}]
                        },
                        {
                            "featureType": "road.arterial",
                            "elementType": "labels.icon",
                            "stylers": [{"visibility": "off"}]
                        },
                        {
                            "featureType": "transit",
                            "elementType": "all",
                            "stylers": [{"visibility": "off"}]
                        },
                        {
                            "featureType": "water",
                            "elementType": "all",
                            "stylers": [{"color": "#c6e2ff"}, {"visibility": "on"}]
                        }
                    ],
                    disableDefaultUI: false,
                    zoomControl: true,
                    mapTypeControl: true,
                    scaleControl: true,
                    streetViewControl: true,
                    rotateControl: true,
                    fullscreenControl: true,
                    gestureHandling: 'greedy'
                };
                
                // Crear instancia del mapa
                map = new google.maps.Map(document.getElementById('google-map'), mapOptions);
                
                // Inicializar geocoder y infoWindow
                geocoder = new google.maps.Geocoder();
                infoWindow = new google.maps.InfoWindow();
                
                // Cargar marcadores de ejemplo
                loadMapMarkers();
                
                // Ocultar capa de carga
                document.getElementById('map-loading').style.display = 'none';
                
                // Actualizar lista de resultados
                updateResultsList();
                
            } catch (error) {
                console.error('Error al inicializar el mapa:', error);
                document.getElementById('map-loading').innerHTML = 
                    '<p style="color: #CE1126; text-align: center;">Error al cargar el mapa. Verifica tu clave API de Google Maps.</p>';
            }
        }
        
        function loadMapMarkers() {
            // Limpiar marcadores existentes
            clearMarkers();
            
            // Obtener filtros actuales
            const categoryFilter = document.getElementById('category-filter').value;
            const cityFilter = document.getElementById('city-filter').value;
            
            // Filtrar proveedores
            const filteredProviders = providersData.filter(provider => {
                const categoryMatch = categoryFilter === 'all' || provider.category === categoryFilter;
                const cityMatch = cityFilter === 'all' || provider.city === cityFilter;
                return categoryMatch && cityMatch;
            });
            
            // Crear marcadores para cada proveedor filtrado
            filteredProviders.forEach(provider => {
                const marker = createMarker(provider);
                markers.push(marker);
            });
            
            // Actualizar contador de resultados
            document.getElementById('results-count').textContent = 
                `${filteredProviders.length} proveedores encontrados`;
            
            // Ajustar vista del mapa para mostrar todos los marcadores
            if (filteredProviders.length > 0) {
                fitMapToMarkers();
            }
        }
        
        function createMarker(provider) {
            // Definir color según categoría
            let iconColor;
            switch(provider.category) {
                case 'construccion': iconColor = '#007A33'; break; // Verde
                case 'mantenimiento': iconColor = '#0055A4'; break; // Azul
                case 'inmobiliaria': iconColor = '#CE1126'; break; // Rojo
                default: iconColor = '#FFD700'; // Dorado
            }
            
            // Crear marcador personalizado
            const marker = new google.maps.Marker({
                position: { lat: provider.lat, lng: provider.lng },
                map: map,
                title: provider.name,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    fillColor: iconColor,
                    fillOpacity: 0.9,
                    strokeColor: '#FFFFFF',
                    strokeWeight: 2,
                    scale: 10
                },
                animation: google.maps.Animation.DROP
            });
            
            // Agregar evento de clic al marcador
            marker.addListener('click', () => {
                showMarkerInfo(marker, provider);
                highlightResultItem(provider.id);
            });
            
            return marker;
        }
        
        function showMarkerInfo(marker, provider) {
            const content = `
                <div class="marker-info">
                    <h4>${provider.name}</h4>
                    <p><strong>Categoría:</strong> ${getCategoryName(provider.category)}</p>
                    <p><strong>Precio:</strong> ${provider.price}</p>
                    <p><strong>Teléfono:</strong> ${provider.phone}</p>
                    <p>${provider.description}</p>
                    <div class="marker-features">
                        ${provider.features.map(f => `<span>${f}</span>`).join('')}
                    </div>
                    <button class="btn btn-primary" onclick="contactProvider(${provider.id})" 
                            style="margin-top: 10px; padding: 5px 15px; width: 100%;">
                        <i class="fas fa-comment"></i> Contactar
                    </button>
                </div>
            `;
            
            infoWindow.setContent(content);
            infoWindow.open(map, marker);
            
            // Centrar mapa en el marcador
            map.panTo(marker.getPosition());
        }
        
        function clearMarkers() {
            markers.forEach(marker => marker.setMap(null));
            markers = [];
        }
        
        function fitMapToMarkers() {
            if (markers.length === 0) return;
            
            const bounds = new google.maps.LatLngBounds();
            markers.forEach(marker => {
                bounds.extend(marker.getPosition());
            });
            
            map.fitBounds(bounds);
            
            // Asegurar un zoom máximo
            const listener = google.maps.event.addListener(map, "idle", function() {
                if (map.getZoom() > 12) map.setZoom(12);
                google.maps.event.removeListener(listener);
            });
        }
        
        function filterMapMarkers() {
            loadMapMarkers();
            updateResultsList();
        }
        
        function updateResultsList() {
            const resultsContainer = document.getElementById('map-results');
            const categoryFilter = document.getElementById('category-filter').value;
            const cityFilter = document.getElementById('city-filter').value;
            
            // Filtrar proveedores
            const filteredProviders = providersData.filter(provider => {
                const categoryMatch = categoryFilter === 'all' || provider.category === categoryFilter;
                const cityMatch = cityFilter === 'all' || provider.city === cityFilter;
                return categoryMatch && cityMatch;
            });
            
            if (filteredProviders.length === 0) {
                resultsContainer.innerHTML = `
                    <div class="empty-results">
                        <i class="fas fa-search"></i>
                        <p>No se encontraron resultados con los filtros actuales</p>
                        <button class="btn btn-outline mt-2" onclick="resetFilters()">
                            <i class="fas fa-redo"></i> Restablecer filtros
                        </button>
                    </div>
                `;
                return;
            }
            
            // Generar HTML de resultados
            resultsContainer.innerHTML = filteredProviders.map(provider => `
                <div class="map-result-item" id="result-${provider.id}" 
                     onclick="selectResult(${provider.id})">
                    <div class="result-header">
                        <span class="result-category">${getCategoryName(provider.category)}</span>
                        <span class="result-price">${provider.price}</span>
                    </div>
                    <h4 class="result-title">${provider.name}</h4>
                    <div class="result-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${getCityName(provider.city)} • ${provider.rating} ⭐
                    </div>
                    <p style="font-size: 0.9rem; color: var(--texto-medio); margin-bottom: 1rem;">
                        ${provider.description}
                    </p>
                    <div class="result-features">
                        ${provider.features.map(f => `<span><i class="fas fa-check"></i> ${f}</span>`).join('')}
                    </div>
                </div>
            `).join('');
        }
        
        function selectResult(providerId) {
            const provider = providersData.find(p => p.id === providerId);
            if (!provider) return;
            
            // Encontrar el marcador correspondiente
            const markerIndex = markers.findIndex(m => 
                m.getPosition().lat() === provider.lat && 
                m.getPosition().lng() === provider.lng
            );
            
            if (markerIndex !== -1) {
                // Simular clic en el marcador
                google.maps.event.trigger(markers[markerIndex], 'click');
            }
            
            // Resaltar elemento en la lista
            highlightResultItem(providerId);
        }
        
        function highlightResultItem(providerId) {
            // Remover clase active de todos los items
            document.querySelectorAll('.map-result-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Agregar clase active al item seleccionado
            const selectedItem = document.getElementById(`result-${providerId}`);
            if (selectedItem) {
                selectedItem.classList.add('active');
                selectedItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
        
        function searchOnMap() {
            const searchInput = document.getElementById('map-search').value.trim();
            
            if (!searchInput) {
                showNotification('Por favor ingresa un término de búsqueda', 'info');
                return;
            }
            
            // Mostrar carga
            document.getElementById('map-loading').style.display = 'flex';
            
            // Primero intentar geocodificar (si es una dirección)
            geocoder.geocode({ address: searchInput + ', Guinea Ecuatorial' }, (results, status) => {
                if (status === 'OK' && results[0]) {
                    // Mover mapa a la ubicación encontrada
                    map.setCenter(results[0].geometry.location);
                    map.setZoom(12);
                    
                    // Buscar proveedores cercanos
                    searchNearbyProviders(results[0].geometry.location);
                } else {
                    // Si no es una dirección, buscar por nombre en los proveedores
                    searchProvidersByName(searchInput);
                }
                
                // Ocultar carga
                setTimeout(() => {
                    document.getElementById('map-loading').style.display = 'none';
                }, 500);
            });
        }
        
        function searchProvidersByName(searchTerm) {
            const searchLower = searchTerm.toLowerCase();
            
            // Filtrar proveedores por nombre o descripción
            const searchResults = providersData.filter(provider => 
                provider.name.toLowerCase().includes(searchLower) ||
                provider.description.toLowerCase().includes(searchLower) ||
                getCategoryName(provider.category).toLowerCase().includes(searchLower)
            );
            
            // Actualizar filtros para mostrar resultados
            if (searchResults.length > 0) {
                // Si hay resultados, centrar en el primero
                map.setCenter({ lat: searchResults[0].lat, lng: searchResults[0].lng });
                map.setZoom(12);
                
                // Actualizar lista de resultados
                updateResultsList();
                
                showNotification(`Encontrados ${searchResults.length} resultados`, 'success');
            } else {
                showNotification('No se encontraron resultados para tu búsqueda', 'info');
            }
        }
        
        function searchNearbyProviders(location) {
            // Calcular distancia de cada proveedor a la ubicación
            const providersWithDistance = providersData.map(provider => {
                const distance = calculateDistance(
                    location.lat(), location.lng(),
                    provider.lat, provider.lng
                );
                return { ...provider, distance };
            });
            
            // Ordenar por distancia
            providersWithDistance.sort((a, b) => a.distance - b.distance);
            
            // Tomar los 10 más cercanos
            const nearestProviders = providersWithDistance.slice(0, 10);
            
            // Mostrar marcadores de los más cercanos
            showNotification(`Encontrados ${nearestProviders.length} proveedores cercanos`, 'success');
        }
        
        function getUserLocation() {
            if (!navigator.geolocation) {
                showNotification('Tu navegador no soporta geolocalización', 'error');
                return;
            }
            
            // Mostrar carga
            document.getElementById('map-loading').style.display = 'flex';
            
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const userLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    
                    // Mover mapa a la ubicación del usuario
                    map.setCenter(userLocation);
                    map.setZoom(14);
                    
                    // Agregar marcador del usuario
                    if (userMarker) {
                        userMarker.setMap(null);
                    }
                    
                    userMarker = new google.maps.Marker({
                        position: userLocation,
                        map: map,
                        title: 'Tu ubicación',
                        icon: {
                            path: google.maps.SymbolPath.CIRCLE,
                            fillColor: '#4285F4',
                            fillOpacity: 0.9,
                            strokeColor: '#FFFFFF',
                            strokeWeight: 3,
                            scale: 12
                        },
                        animation: google.maps.Animation.BOUNCE
                    });
                    
                    // Buscar proveedores cercanos
                    searchNearbyProviders(userLocation);
                    
                    // Ocultar carga
                    document.getElementById('map-loading').style.display = 'none';
                    
                    showNotification('Ubicación encontrada', 'success');
                },
                (error) => {
                    document.getElementById('map-loading').style.display = 'none';
                    
                    let errorMessage = 'No se pudo obtener tu ubicación';
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            errorMessage = 'Permiso de ubicación denegado';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMessage = 'Información de ubicación no disponible';
                            break;
                        case error.TIMEOUT:
                            errorMessage = 'Tiempo de espera agotado';
                            break;
                    }
                    
                    showNotification(errorMessage, 'error');
                }
            );
        }
        
        // =============================================
        // FUNCIONES AUXILIARES
        // =============================================
        function getCategoryName(category) {
            const categories = {
                'construccion': 'Construcción',
                'mantenimiento': 'Mantenimiento',
                'inmobiliaria': 'Inmobiliaria',
                'albanil': 'Albañil',
                'electricista': 'Electricista',
                'fontanero': 'Fontanero',
                'arquitecto': 'Arquitecto'
            };
            return categories[category] || category;
        }
        
        function getCityName(city) {
            const cities = {
                'malabo': 'Malabo',
                'bata': 'Bata',
                'ebebiyin': 'Ebebiyín'
            };
            return cities[city] || city;
        }
        
        function calculateDistance(lat1, lon1, lat2, lon2) {
            const R = 6371; // Radio de la Tierra en km
            const dLat = (lat2 - lat1) * Math.PI / 180;
            const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = 
                Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
                Math.sin(dLon/2) * Math.sin(dLon/2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            return R * c;
        }
        
        function contactProvider(providerId) {
            const provider = providersData.find(p => p.id === providerId);
            if (!provider) return;
            
            showNotification(`Contactando a ${provider.name}...`, 'info');
            // En producción: abrir modal de contacto o chat
        }
        
        function resetFilters() {
            document.getElementById('category-filter').value = 'all';
            document.getElementById('city-filter').value = 'all';
            filterMapMarkers();
        }
        
        // =============================================
        // FUNCIONES DE INTERFAZ
        // =============================================
        function openModal(modalId) {
            document.getElementById(modalId + '-modal').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId + '-modal').style.display = 'none';
            document.body.style.overflow = 'auto';
        }
        
        function switchToRegister() {
            closeModal('login');
            openModal('register');
        }
        
        function switchToLogin() {
            closeModal('register');
            openModal('login');
        }
        
        function showNotification(message, type = 'info') {
            // Crear elemento de notificación
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.remove()">×</button>
            `;
            
            // Estilos de notificación
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? 'var(--verde-ge)' : type === 'error' ? 'var(--rojo-ge)' : 'var(--azul-ge)'};
                color: white;
                padding: 1rem 1.5rem;
                border-radius: var(--radio-md);
                display: flex;
                align-items: center;
                gap: 1rem;
                z-index: 10000;
                animation: slideIn 0.3s ease;
                box-shadow: var(--sombra-media);
                max-width: 90vw;
            `;
            
            document.body.appendChild(notification);
            
            // Auto-remover después de 5 segundos
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 5000);
        }
        
        function scrollToServices() {
            document.getElementById('servicios').scrollIntoView({ behavior: 'smooth' });
            updateActiveNav('#servicios');
        }
        
        function openMapSection() {
            document.getElementById('mapa').scrollIntoView({ behavior: 'smooth' });
            updateActiveNav('#mapa');
        }
        
        function filterCategory(category) {
            showNotification(`Mostrando profesionales de ${getCategoryName(category)}`, 'info');
            // Redirigir al mapa con filtro aplicado
            openMapSection();
            setTimeout(() => {
                document.getElementById('category-filter').value = category;
                filterMapMarkers();
            }, 500);
        }
        
        function selectService(serviceType) {
            showNotification(`Buscando ${serviceType}...`, 'info');
            // Redirigir al mapa con filtro aplicado
            openMapSection();
            setTimeout(() => {
                document.getElementById('category-filter').value = serviceType;
                filterMapMarkers();
            }, 500);
        }
        
        function viewProperty(id) {
            showNotification(`Cargando propiedad #${id}...`, 'info');
            // En producción: abrir modal de detalles de propiedad
        }
        
        function simulateLogin() {
            currentUser = {
                name: 'Juan Pérez',
                email: 'juan@ejemplo.com',
                type: 'profesional'
            };
            
            document.getElementById('auth-buttons').style.display = 'none';
            showNotification('¡Bienvenido de nuevo, Juan!', 'success');
        }
        
        // Inicializar mapa cuando la API esté lista
        function initMapSystem() {
            if (typeof google !== 'undefined' && google.maps) {
                initMap();
            } else {
                setTimeout(initMapSystem, 100);
            }
        }
        
        // Agregar estilos de animación para notificaciones
        const animationStyle = document.createElement('style');
        animationStyle.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
            
            .notification button {
                background: none;
                border: none;
                color: white;
                font-size: 1.25rem;
                cursor: pointer;
                margin-left: auto;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .marker-info {
                padding: 10px;
                min-width: 250px;
                max-width: 300px;
            }
            
            .marker-info h4 {
                color: var(--verde-ge);
                margin-bottom: 10px;
                font-size: 1.1rem;
            }
            
            .marker-info p {
                margin-bottom: 8px;
                font-size: 0.9rem;
                line-height: 1.4;
            }
            
            .marker-features {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin: 10px 0;
            }
            
            .marker-features span {
                background: var(--fondo-claro);
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.8rem;
                color: var(--texto-medio);
            }
            
            /* Estilos para pasos */
            .steps-container {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-top: 3rem;
                position: relative;
            }
            
            .steps-container:before {
                content: '';
                position: absolute;
                top: 40px;
                left: 10%;
                right: 10%;
                height: 3px;
                background: linear-gradient(90deg, var(--verde-ge), var(--azul-ge));
                z-index: 1;
            }
            
            .step {
                flex: 1;
                text-align: center;
                position: relative;
                z-index: 2;
            }
            
            .step-number {
                width: 80px;
                height: 80px;
                background: var(--fondo-blanco);
                border: 3px solid var(--verde-ge);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                font-weight: 700;
                color: var(--verde-ge);
                margin: 0 auto 1.5rem;
                position: relative;
            }
            
            .step-content {
                padding: 0 1rem;
            }
            
            .step-title {
                font-size: 1.25rem;
                color: var(--verde-oscuro);
                margin-bottom: 0.75rem;
            }
            
            /* Footer */
            .footer {
                background: var(--texto-oscuro);
                color: white;
                padding: 4rem 0 2rem;
            }
            
            .footer-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 3rem;
                margin-bottom: 3rem;
            }
            
            .footer-logo {
                font-family: 'Montserrat', sans-serif;
                font-size: 2rem;
                font-weight: 900;
                color: white;
                margin-bottom: 1rem;
            }
            
            .footer-description {
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 1.5rem;
                line-height: 1.6;
            }
            
            .footer-title {
                color: white;
                font-size: 1.25rem;
                margin-bottom: 1.5rem;
                position: relative;
                padding-bottom: 0.75rem;
            }
            
            .footer-title:after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 40px;
                height: 3px;
                background: var(--verde-ge);
            }
            
            .footer-links li {
                margin-bottom: 0.75rem;
            }
            
            .footer-links a {
                color: rgba(255, 255, 255, 0.7);
                transition: var(--transicion-rapida);
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .footer-links a:hover {
                color: white;
                padding-left: 0.5rem;
            }
            
            .social-links {
                display: flex;
                gap: 1rem;
                margin-top: 1.5rem;
            }
            
            .social-link {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                justify-content: center;
                transition: var(--transicion-rapida);
            }
            
            .social-link:hover {
                background: var(--verde-ge);
                transform: translateY(-3px);
            }
            
            .footer-bottom {
                padding-top: 2rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
                color: rgba(255, 255, 255, 0.5);
                font-size: 0.9rem;
            }
            
            .footer-bottom a {
                color: var(--verde-ge);
            }
            
            /* Testimonios */
            .testimonials-section {
                background: var(--gradiente-azul);
                color: white;
                position: relative;
                overflow: hidden;
            }
            
            .testimonials-section:before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            }
            
            .section-header.white h2 {
                color: white;
            }
            
            .section-header.white h2:after {
                background: var(--dorado);
            }
            
            .testimonials-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }
            
            .testimonial-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: var(--radio-lg);
                padding: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .testimonial-content {
                font-style: italic;
                margin-bottom: 1.5rem;
                line-height: 1.8;
            }
            
            .testimonial-author {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            
            .author-avatar {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: var(--gradiente-dorado);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                color: var(--texto-oscuro);
            }
            
            .author-info h4 {
                color: white;
                margin-bottom: 0.25rem;
            }
            
            .author-info p {
                color: rgba(255, 255, 255, 0.8);
                margin: 0;
            }
            
            /* CTA Section */
            .cta-section {
                padding: 6rem 0;
                background: linear-gradient(135deg, var(--verde-oscuro) 0%, var(--verde-ge) 100%);
                color: white;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            
            .cta-section:before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,215,0,0.1) 0%, transparent 70%);
                animation: rotate 20s linear infinite;
            }
            
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .cta-content {
                position: relative;
                z-index: 2;
                max-width: 700px;
                margin: 0 auto;
            }
            
            .cta-content h2 {
                color: white;
                font-size: 3rem;
                margin-bottom: 1.5rem;
            }
            
            .cta-content p {
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.25rem;
                margin-bottom: 2.5rem;
            }
            
            .cta-buttons {
                display: flex;
                gap: 1.5rem;
                justify-content: center;
            }
            
            /* Propiedades */
            .properties-section {
                background: linear-gradient(135deg, var(--fondo-claro) 0%, #FFFFFF 100%);
            }
            
            .properties-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }
            
            .property-card {
                background: var(--fondo-blanco);
                border-radius: var(--radio-lg);
                overflow: hidden;
                box-shadow: var(--sombra-suave);
                transition: var(--transicion-rapida);
            }
            
            .property-card:hover {
                transform: translateY(-10px);
                box-shadow: var(--sombra-media);
            }
            
            .property-image {
                height: 220px;
                background: var(--gradiente-azul);
                position: relative;
                overflow: hidden;
            }
            
            .property-badge {
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: var(--rojo-ge);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: var(--radio-sm);
                font-size: 0.85rem;
                font-weight: 600;
            }
            
            .property-content {
                padding: 1.5rem;
            }
            
            .property-price {
                font-size: 1.75rem;
                font-weight: 700;
                color: var(--verde-ge);
                margin-bottom: 0.5rem;
            }
            
            .property-location {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: var(--texto-claro);
                margin-bottom: 1rem;
            }
            
            .property-features {
                display: flex;
                gap: 1.5rem;
                margin: 1rem 0;
            }
            
            .feature {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: var(--texto-medio);
            }
            
            /* Modal */
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 2000;
                padding: 1rem;
            }
            
            .modal {
                background: var(--fondo-blanco);
                border-radius: var(--radio-lg);
                width: 100%;
                max-width: 500px;
                max-height: 90vh;
                overflow-y: auto;
                animation: modalSlide 0.3s ease-out;
            }
            
            @keyframes modalSlide {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .modal-header {
                padding: 2rem 2rem 1rem;
                border-bottom: 1px solid var(--borde);
                position: relative;
            }
            
            .modal-body {
                padding: 2rem;
            }
            
            .modal-close {
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: var(--texto-claro);
                transition: var(--transicion-rapida);
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
            }
            
            .modal-close:hover {
                background: var(--fondo-claro);
                color: var(--rojo-ge);
            }
        `;
        document.head.appendChild(animationStyle);
    </script>
</body>
</html>''',

    # =============================================
    # 12. build.gradle (app level)
    # =============================================
    'abitaX_Android_Project/app/build.gradle': '''plugins {
    id 'com.android.application'
}

android {
    namespace 'com.abitax'
    compileSdk 34

    defaultConfig {
        applicationId "com.abitax"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        
        // Configuración para WebView
        buildConfigField "String", "GOOGLE_MAPS_API_KEY", "\"TU_CLAVE_API_DE_GOOGLE_MAPS\""
        
        // Configuración para diferentes densidades de pantalla
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.debug
        }
        debug {
            minifyEnabled false
            debuggable true
            applicationIdSuffix ".debug"
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    
    buildFeatures {
        viewBinding true
        buildConfig true
    }
    
    packagingOptions {
        resources {
            excludes += ['META-INF/DEPENDENCIES', 'META-INF/LICENSE', 'META-INF/LICENSE.txt', 'META-INF/NOTICE', 'META-INF/NOTICE.txt']
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.webkit:webkit:1.9.0'
    
    // Google Maps
    implementation 'com.google.android.gms:play-services-maps:18.2.0'
    implementation 'com.google.android.gms:play-services-location:21.0.1'
    
    // Navegación
    implementation 'androidx.navigation:navigation-fragment:2.7.6'
    implementation 'androidx.navigation:navigation-ui:2.7.6'
    
    // Lifecycle
    implementation 'androidx.lifecycle:lifecycle-viewmodel:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-livedata:2.7.0'
    
    // Testing
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    androidTestImplementation 'androidx.test:runner:1.5.2'
    androidTestImplementation 'androidx.test:rules:1.5.0'
}''',

    # =============================================
    # 13. build.gradle (project level)
    # =============================================
    'abitaX_Android_Project/build.gradle': '''// Top-level build file where you can add configuration options common to all sub-projects/modules.

plugins {
    id 'com.android.application' version '8.2.0' apply false
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}''',

    # =============================================
    # 14. settings.gradle
    # =============================================
    'abitaX_Android_Project/settings.gradle': '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "abitaX"
include ':app'
''',

    # =============================================
    # 15. gradle-wrapper.properties
    # =============================================
    'abitaX_Android_Project/gradle/wrapper/gradle-wrapper.properties': '''#Wed Dec 18 16:59:00 CET 2024
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.2-all.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
''',

    # =============================================
    # 16. gradlew (Linux/Mac script)
    # =============================================
    'abitaX_Android_Project/gradlew': '''#!/usr/bin/env sh

#
# Copyright 2015 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

##############################################################################
##
##  Gradle start up script for UN*X
##
##############################################################################

# Attempt to set APP_HOME
# Resolve links: $0 may be a link
PRG="$0"
# Need this for relative symlinks.
while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \(.*\)$'`
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=`dirname "$PRG"`"/$link"
    fi
done
SAVED="`pwd`"
cd "`dirname \"$PRG\"`/" >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

APP_NAME="Gradle"
APP_BASE_NAME=`basename "$0"`

# Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

# Use the maximum available, or set MAX_FD != -1 to use that value.
MAX_FD="maximum"

warn () {
    echo "$*"
} >&2

die () {
    echo
    echo "$*"
    echo
    exit 1
} >&2

# OS specific support (must be 'true' or 'false').
cygwin=false
msys=false
darwin=false
nonstop=false
case "`uname`" in
  CYGWIN* )
    cygwin=true
    ;;
  Darwin* )
    darwin=true
    ;;
  MINGW* )
    msys=true
    ;;
  NONSTOP* )
    nonstop=true
    ;;
esac

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

# Determine the Java version to use.
if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        # IBM's JDK on AIX uses strange locations for the executables
        JAVACMD="$JAVA_HOME/jre/sh/java"
    else
        JAVACMD="$JAVA_HOME/bin/java"
    fi
    if [ ! -x "$JAVACMD" ] ; then
        die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME"
    fi
else
    JAVACMD="java"
    which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH."
fi

# Increase the maximum file descriptors if we can.
if [ "$cygwin" = "false" -a "$darwin" = "false" -a "$nonstop" = "false" ] ; then
    MAX_FD_LIMIT=`ulimit -H -n`
    if [ $? -eq 0 ] ; then
        if [ "$MAX_FD" = "maximum" -o "$MAX_FD" = "max" ] ; then
            MAX_FD="$MAX_FD_LIMIT"
        fi
        ulimit -n $MAX_FD
        if [ $? -ne 0 ] ; then
            warn "Could not set maximum file descriptor limit: $MAX_FD"
        fi
    else
        warn "Could not query maximum file descriptor limit: $MAX_FD_LIMIT"
    fi
fi

# For Darwin, add options to specify how the application appears in the dock
if $darwin; then
    GRADLE_OPTS="$GRADLE_OPTS \"-Xdock:name=$APP_NAME\" \"-Xdock:icon=$APP_HOME/media/gradle.icns\""
fi

# For Cygwin or MSYS, switch paths to Windows format before running java
if $cygwin || $msys ; then
    APP_HOME=`cygpath --path --mixed "$APP_HOME"`
    CLASSPATH=`cygpath --path --mixed "$CLASSPATH"`
    
    JAVACMD=`cygpath --unix "$JAVACMD"`

    # We build the pattern for arguments to be converted via cygpath
    ROOTDIRSRAW=`find -L / -maxdepth 1 -mindepth 1 -type d 2>/dev/null`
    SEP=""
    for dir in $ROOTDIRSRAW ; do
        ROOTDIRS="$ROOTDIRS$SEP$dir"
        SEP="|"
    done
    OURCYGPATTERN="(^($ROOTDIRS))"
    # Add a user-defined pattern to the cygpath arguments
    if [ "$GRADLE_OPTS" ] ; then
        OURCYGPATTERN="$OURCYGPATTERN|($GRADLE_OPTS)"
    fi
    if [ "$OURCYGPATTERN" ] ; then
        GRADLE_CYGPATTERN="$OURCYGPATTERN"
    else
        GRADLE_CYGPATTERN="(.*)"
    fi
    # Now convert the arguments - kludge to limit ourselves to /bin/sh
    i=0
    for arg in "$@" ; do
        CHECK=`echo "$arg"|egrep -c "$OURCYGPATTERN" -`
        CHECK2=`echo "$arg"|egrep -c "^-"`                                 ### Determine if an option

        if [ $CHECK -ne 0 ] && [ $CHECK2 -eq 0 ] ; then                    ### Added a condition
            eval `echo args$i`=`cygpath --path --ignore --mixed "$arg"`
        else
            eval `echo args$i`="\"$arg\""
        fi
        i=$((i+1))
    done
    case $i in
        (0) set -- ;;
        (1) set -- "$args0" ;;
        (2) set -- "$args0" "$args1" ;;
        (3) set -- "$args0" "$args1" "$args2" ;;
        (4) set -- "$args0" "$args1" "$args2" "$args3" ;;
        (5) set -- "$args0" "$args1" "$args2" "$args3" "$args4" ;;
        (6) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" ;;
        (7) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" ;;
        (8) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" "$args7" ;;
        (9) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" "$args7" "$args8" ;;
    esac
fi

# Escape application args
save () {
    for i do printf %s\\\\n "$i" | sed "s/'/'\\\\\\\\''/g;1s/^/'/;\$s/\$/' \\\\\\\\/" ; done
    echo " "
}
APP_ARGS=$(save "$@")

# Collect all arguments for the java command, following the shell quoting and substitution rules
eval set -- $DEFAULT_JVM_OPTS $JAVA_OPTS $GRADLE_OPTS "\"-Dorg.gradle.appname=$APP_BASE_NAME\"" -classpath "\"$CLASSPATH\"" org.gradle.wrapper.GradleWrapperMain "$APP_ARGS"

# by default we should be in the "project root" (the directory that contains the "settings.gradle" file)
cd "$APP_HOME"

exec "$JAVACMD" "$@"
''',

    # =============================================
    # 17. gradlew.bat (Windows script)
    # =============================================
    'abitaX_Android_Project/gradlew.bat': '''@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%"=="" @echo off
@rem ##########################################################################
@rem
@rem  Gradle startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
@rem This is normally unused
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if %ERRORLEVEL% equ 0 goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar


@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

:end
@rem End local scope for the variables with windows NT shell
if %ERRORLEVEL% equ 0 goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE% equ 0 set EXIT_CODE=1
if not ""=="%GRADLE_EXIT_CONSOLE%" exit %EXIT_CODE%
exit /b %EXIT_CODE%

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
''',

    # =============================================
    # 18. proguard-rules.pro
    # =============================================
    'abitaX_Android_Project/app/proguard-rules.pro': '''# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile

# Configuración de ProGuard para abitaX

# Mantener clases nativas
-keepclasseswithmembernames class * {
    native <methods>;
}

# Mantener clases personalizadas
-keep class com.abitax.** { *; }
-keep class * extends android.app.Activity
-keep class * extends android.app.Application
-keep class * extends android.app.Service

# WebView
-keep class ** extends android.webkit.WebChromeClient {
   public *;
}

-keep class ** extends android.webkit.WebViewClient {
   public *;
}

# Google Maps
-keep class com.google.android.gms.maps.** { *; }
-keep interface com.google.android.gms.maps.** { *; }
-keep class * implements com.google.android.gms.maps.** { *; }

# Material Components
-keep class com.google.android.material.** { *; }
-keep interface com.google.android.material.** { *; }

# AndroidX
-keep class androidx.** { *; }
-keep interface androidx.** { *; }

# Keep - Library. Keep all public and protected classes, fields, and methods.
-keep public class * {
    public protected <fields>;
    public protected <methods>;
}

# Also keep - Enumerations. Keep the special static methods that are required in
# enumeration classes.
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Keep - Keep generic signature. Use this line if you use types that use
# generic types.
-keepattributes Signature

# Keep - Keep exception stack traces.
-keepattributes SourceFile,LineNumberTable

# Remove debug logs in release build
-assumenosideeffects class android.util.Log {
    public static boolean isLoggable(java.lang.String, int);
    public static int v(...);
    public static int i(...);
    public static int w(...);
    public static int d(...);
    public static int e(...);
}
''',

    # =============================================
    # 19. README.md
    # =============================================
    'abitaX_Android_Project/README.md': '''# abitaX 🇬🇶 - SuperApp de Guinea Ecuatorial

## 📱 Descripción
Aplicación móvil completa que integra servicios profesionales, propiedades y un sistema de mapas interactivo para Guinea Ecuatorial.

## ✨ Características principales
- 🗺️ **Mapa interactivo** con proveedores geolocalizados
- 🔧 **Servicios profesionales** verificados (construcción, mantenimiento, etc.)
- 🏠 **Propiedades** en alquiler y venta
- 🔍 **Búsqueda avanzada** por categoría, ciudad y ubicación
- 💬 **Chat integrado** (pendiente de implementación)
- 📱 **Diseño responsivo** optimizado para Android WebView
- 🎨 **Tema personalizado** con colores de Guinea Ecuatorial

## 🛠️ Requisitos técnicos
- **Android Studio**: 2022.3.1 o superior
- **JDK**: 17 o superior
- **Android SDK**: API 24 (Android 7.0) mínimo
- **Google Maps API**: Clave requerida

## 🚀 Configuración rápida

### 1. Obtener clave API de Google Maps
1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las APIs:
   - **Maps JavaScript API**
   - **Geocoding API**
   - **Places API**
4. Crea credenciales → Clave API
5. Copia tu clave API

### 2. Configurar el proyecto
1. Abre Android Studio
2. Selecciona "Open an Existing Project"
3. Navega a la carpeta `abitaX_Android_Project`
4. Espera a que Gradle sincronice

### 3. Configurar API Key
Reemplaza en dos archivos:

**A. En `app/src/main/res/values/strings.xml`:**
```xml
<string name="google_maps_key">TU_CLAVE_API_AQUÍ</string>