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
import com.google.firebase.auth.ktx.auth
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.ktx.Firebase

class RegisterActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth;
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)
        auth = Firebase.auth

        val backbutton: ImageButton = findViewById(R.id.imageButton5)
        backbutton.setOnClickListener {
            val intent = Intent (this,Activity_2::class.java)
            startActivity(intent)
        }

        val registerbutton: Button = findViewById(R.id.button3)



        registerbutton.setOnClickListener {
            registerUser()

        }

    }
    private fun registerUser(){
        val etemail: EditText = findViewById(R.id.email)
        val etpassword: EditText = findViewById(R.id.password)
        val etname: EditText = findViewById(R.id.editTextTextPersonName)
        val email = etemail.text.toString().trim()
        val password = etpassword.text.toString().trim()
        val name = etname.text.toString().trim()


        if(email.isEmpty()){
            etemail.setError("Email is required!")
            etemail.requestFocus()
            return
        }
        if(!Patterns.EMAIL_ADDRESS.matcher(email).matches()){
            etemail.setError("Enter the valid Email!")
            etemail.requestFocus()
            return
        }
        if(password.isEmpty()){
            etpassword.setError("Enter the password!")
            etpassword.requestFocus()
            return
        }
        if(password.length<6){
            etpassword.setError("Min password lenght must be more than 6")
            etpassword.requestFocus()
            return
        }
        if(name.isEmpty()){
            etname.setError("Name is required!")
            etname.requestFocus()
            return
        }
        auth.createUserWithEmailAndPassword(email,password)
            .addOnCompleteListener (this){task ->
                if(task.isSuccessful){

                    FirebaseAuth.getInstance().currentUser?.let {
                        val user = User(it.uid,name,email)
                        FirebaseDatabase.getInstance().getReference("Users")
                            .child(it.uid)
                            .setValue(user).addOnCompleteListener(this){task ->
                                if(task.isSuccessful){
                                    Toast.makeText(this,"registered successfully",Toast.LENGTH_SHORT).show()
                                }
                                else{
                                    Toast.makeText(this,"registration failed",Toast.LENGTH_SHORT).show()
                                }
                            }
                    }
                }else{
                    Toast.makeText(this,"registration failed",Toast.LENGTH_SHORT).show()
                }
            }


    }

}
