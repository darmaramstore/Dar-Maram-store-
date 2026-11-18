package com.darmaram.store

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebSettings
import android.webkit.SslErrorHandler
import android.net.http.SslError

class MainActivity : Activity() {
    private lateinit var webView: WebView
    private val storeUrl = "https://darmaramstore.wordpress.com/"

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        webView = WebView(this).apply {
            setBackgroundColor(android.graphics.Color.rgb(18, 18, 18))
            settings.apply {
                javaScriptEnabled = true
                domStorageEnabled = true
                databaseEnabled = false
                allowFileAccess = true
                allowContentAccess = false
                allowFileAccessFromFileURLs = false
                allowUniversalAccessFromFileURLs = false
                javaScriptCanOpenWindowsAutomatically = false
                setSupportMultipleWindows(false)
                mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                    safeBrowsingEnabled = true
                }
            }
            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                    val uri = request?.url ?: return true
                    return routeUrl(uri)
                }

                @Deprecated("Deprecated in Android API")
                override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                    val uri = runCatching { Uri.parse(url ?: return true) }.getOrNull() ?: return true
                    return routeUrl(uri)
                }

                override fun onReceivedSslError(view: WebView?, handler: SslErrorHandler?, error: SslError?) {
                    handler?.cancel()
                }
            }
        }

        CookieManager.getInstance().apply {
            setAcceptCookie(true)
            setAcceptThirdPartyCookies(webView, false)
        }
        setContentView(webView)
        if (savedInstanceState == null || webView.restoreState(savedInstanceState) == null) {
            webView.loadUrl("file:///android_asset/index.html")
        }
    }

    // Keep normal web pages inside the store app; send only phone/email/app links outside.
    private fun routeUrl(uri: Uri): Boolean {
        val scheme = uri.scheme?.lowercase()
        val host = uri.host?.lowercase()
        if (scheme == "https" && host in setOf("wa.me", "api.whatsapp.com")) {
            runCatching { startActivity(Intent(Intent.ACTION_VIEW, uri)) }
            return true
        }
        return when (scheme) {
            "https", "http" -> false
            "tel", "mailto", "whatsapp", "sms" -> {
                runCatching { startActivity(Intent(Intent.ACTION_VIEW, uri)) }
                true
            }
            else -> true
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        if (::webView.isInitialized) webView.saveState(outState)
        super.onSaveInstanceState(outState)
    }

    @Deprecated("Deprecated in Android API")
    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) webView.goBack() else super.onBackPressed()
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