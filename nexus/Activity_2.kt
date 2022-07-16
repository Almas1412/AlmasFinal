package com.example.nexus

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button


class Activity_2 : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_2)

        val loginButton: Button = findViewById(R.id.button)
        loginButton.setOnClickListener {
            val intent = Intent (this,LoginActivity::class.java)
            startActivity(intent)
        }
        val registerbutton: Button = findViewById(R.id.button2)
        registerbutton.setOnClickListener {
            val regintent = Intent(this,RegisterActivity::class.java)
            startActivity(regintent)
        }
    }
}