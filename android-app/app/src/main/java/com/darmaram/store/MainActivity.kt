package com.darmaram.store

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Build
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebSettings

class MainActivity : Activity() {
    private lateinit var webView: WebView
    private val assetHome = "file:///android_asset/index.html"

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        WebView.setWebContentsDebuggingEnabled(false)

        webView = WebView(this).apply {
            settings.apply {
                javaScriptEnabled = true // Required by the bundled, first-party store interface.
                domStorageEnabled = false
                allowFileAccess = true // Required only to load the bundled android_asset storefront.
                allowContentAccess = false
                allowFileAccessFromFileURLs = false
                allowUniversalAccessFromFileURLs = false
                javaScriptCanOpenWindowsAutomatically = false
                setSupportMultipleWindows(false)
                mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    safeBrowsingEnabled = true
                }
            }
            webViewClient = StoreWebViewClient()
        }

        CookieManager.getInstance().apply {
            setAcceptCookie(false)
            setAcceptThirdPartyCookies(webView, false)
        }
        setContentView(webView)
        if (savedInstanceState == null) {
            webView.loadUrl(assetHome)
        } else {
            webView.restoreState(savedInstanceState)
        }
    }

    private inner class StoreWebViewClient : WebViewClient() {
        override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
            val uri = request?.url ?: return true
            return handleNavigation(uri)
        }

        @Deprecated("Deprecated in Android API")
        override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
            val uri = runCatching { Uri.parse(url ?: return true) }.getOrNull() ?: return true
            return handleNavigation(uri)
        }

        private fun handleNavigation(uri: Uri): Boolean {
            val scheme = uri.scheme?.lowercase()
            val url = uri.toString()

            // Keep navigation inside the app limited to its bundled storefront.
            if (scheme == "file" && url.startsWith("file:///android_asset/")) return false

            // Open secure web links and WhatsApp outside the app; never launch arbitrary schemes.
            if (scheme == "https" || scheme == "http") {
                return openExternal(uri)
            }
            if (scheme == "whatsapp") {
                return openExternal(uri)
            }
            return true
        }

        private fun openExternal(uri: Uri): Boolean {
            return try {
                startActivity(Intent(Intent.ACTION_VIEW, uri))
                true
            } catch (_: Exception) {
                true
            }
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        webView.saveState(outState)
        super.onSaveInstanceState(outState)
    }

    @Deprecated("Deprecated in Android API")
    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }

    override fun onDestroy() {
        if (::webView.isInitialized) {
            webView.stopLoading()
            webView.loadUrl("about:blank")
            webView.removeAllViews()
            webView.destroy()
        }
        super.onDestroy()
    }
}
