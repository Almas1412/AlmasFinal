package com.example.nexus

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Patterns
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.ktx.auth
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase

class LoginActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth;





    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)
        auth = Firebase.auth

        val backbutton: ImageButton = findViewById(R.id.imageButton5)
        backbutton.setOnClickListener {
            val intent = Intent (this,Activity_2::class.java)
            startActivity(intent)
        }

        val loginbutton: Button = findViewById(R.id.button6)
        loginbutton.setOnClickListener {
            user_login()
        }
    }
    private fun user_login(){
        val edittextmail:EditText = findViewById(R.id.email)
        val edittextpassword:EditText = findViewById(R.id.password)
        val email = edittextmail.text.toString().trim()
        val password = edittextpassword.text.toString().trim()

        if(email.isEmpty()){
            edittextmail.setError("Email is required!")
            edittextmail.requestFocus()
            return
        }
        if(!Patterns.EMAIL_ADDRESS.matcher(email).matches()){
            edittextmail.setError("Enter the valid Email!")
            edittextmail.requestFocus()
            return
        }
        if(password.isEmpty()){
            edittextpassword.setError("Enter the password!")
            edittextpassword.requestFocus()
            return
        }
        if(password.length<6){
            edittextpassword.setError("Min password lenght must be more than 6")
            edittextpassword.requestFocus()
            return
        }

        auth.signInWithEmailAndPassword(email,password)
            .addOnCompleteListener(this) { task ->
                if(task.isSuccessful){
                    val user = FirebaseAuth.getInstance().currentUser
                    if (user != null) {
                        if(user.isEmailVerified){

                            val intent = Intent (this,MainPage::class.java)

                            startActivity(intent)
                        }
                        else
                        {
                            user.sendEmailVerification()
                            Toast.makeText(this,"Check your email", Toast.LENGTH_SHORT).show()
                        }
                    }
                }
                else{
                    Toast.makeText(this,"authorization failed", Toast.LENGTH_SHORT).show()
                }
            }
    }

}
