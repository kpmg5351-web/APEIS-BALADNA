package com.example;

import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.io.File;

public class MainActivity extends AppCompatActivity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            File jsCache = new File(getCacheDir(), "WebView/Default/HTTP Cache/Code Cache/js");
            if (!jsCache.exists()) jsCache.mkdirs();
            File wasmCache = new File(getCacheDir(), "WebView/Default/HTTP Cache/Code Cache/wasm");
            if (!wasmCache.exists()) wasmCache.mkdirs();
        } catch (Exception e) {
            // ignore
        }

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setDatabaseEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        webView.addJavascriptInterface(new WebAppInterface(), "AndroidBridge");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (url.endsWith(".apk") || url.contains("abees-baladna")) {
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        startActivity(intent);
                    } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "أنت تعمل بالفعل داخل تطبيق أندرويد المثبت!", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }
                return false;
            }
        });
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    public class WebAppInterface {
        @JavascriptInterface
        public void saveToNativeStorage(String key, String value) {
            try {
                SharedPreferences prefs = getSharedPreferences("AbeesAppStorage", MODE_PRIVATE);
                prefs.edit().putString(key, value).apply();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        @JavascriptInterface
        public String getFromNativeStorage(String key) {
            try {
                SharedPreferences prefs = getSharedPreferences("AbeesAppStorage", MODE_PRIVATE);
                return prefs.getString(key, "");
            } catch (Exception e) {
                e.printStackTrace();
                return "";
            }
        }

        @JavascriptInterface
        public void makePhoneCall(final String phoneNumber) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    try {
                        Intent intent = new Intent(Intent.ACTION_DIAL);
                        intent.setData(Uri.parse("tel:" + phoneNumber));
                        startActivity(intent);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        }

        @JavascriptInterface
        public void openWhatsApp(final String phoneNumber) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String url = "https://api.whatsapp.com/send?phone=" + phoneNumber;
                        Intent intent = new Intent(Intent.ACTION_VIEW);
                        intent.setData(Uri.parse(url));
                        startActivity(intent);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }
}
