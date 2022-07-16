package com.example.nexus

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Editable
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.TextView
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener


class AddBalance : AppCompatActivity() {

    internal var user: User? = null

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_add_balance)
        val balancetv: TextView =findViewById(R.id.textView12)
        val addbalancebtn:Button=findViewById(R.id.button4)


        val backbutton: ImageButton = findViewById(R.id.imageButton2)
        backbutton.setOnClickListener {
            val intent = Intent (this,MainPage::class.java)
            startActivity(intent)
        }
        val reference = FirebaseDatabase.getInstance().getReference("Users").child(FirebaseAuth.getInstance().currentUser!!.uid)
        val menuListener = object : ValueEventListener {
            override fun onCancelled(databaseError: DatabaseError) {
                // handle error
            }
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                user = dataSnapshot.getValue(User::class.java)
                balancetv.text =user?.balance.toString()


            }
        }
        val etl: EditText = findViewById(R.id.editTextNumber)
        val userid = FirebaseAuth.getInstance().currentUser!!.uid
        reference.addListenerForSingleValueEvent(menuListener)
        addbalancebtn.setOnClickListener {
            val adding_balance: Int = etl.text.toString().toInt()
            val current_balance:Int = balancetv.text.toString().toInt()
            val new_balance:Int = adding_balance+current_balance
            reference.child("balance").setValue(new_balance)

        }
    }
}