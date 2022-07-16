package com.example.nexus

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.*
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.database.*
import com.google.zxing.BarcodeFormat
import com.google.zxing.EncodeHintType
import com.google.zxing.qrcode.QRCodeWriter

class MainPage : AppCompatActivity() {



    internal var user: User? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main_page)

        val logoutbtn: Button = findViewById(R.id.logoutbtn)
        logoutbtn.setOnClickListener {
            FirebaseAuth.getInstance().signOut()
            val intent = Intent (this,Activity_2::class.java)
            startActivity(intent)
        }
        val user23 = FirebaseAuth.getInstance().currentUser
        val reference = FirebaseDatabase.getInstance().getReference("Users").child(FirebaseAuth.getInstance().currentUser!!.uid)
        val userId = user23?.uid
        val addbalancebtn:ImageButton=findViewById(R.id.imageButton)
        addbalancebtn.setOnClickListener {
            val intent = Intent (this,AddBalance::class.java)
            startActivity(intent)
        }

        val usernametv:TextView=findViewById(R.id.nametxt)
        val balancetv:TextView=findViewById(R.id.balancetxt)

        val menuListener = object : ValueEventListener {
            override fun onCancelled(databaseError: DatabaseError) {
                // handle error
            }
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                user = dataSnapshot.getValue(User::class.java)
                usernametv.text = user?.name
                balancetv.text = user?.balance.toString()

            }
        }
        val qrview:ImageView = findViewById(R.id.QRView)
        qrview.setImageBitmap(getQrCodeBitmap(userId.toString()))
        reference.addListenerForSingleValueEvent(menuListener)



    }
    fun getQrCodeBitmap(uid: String,): Bitmap {
        val size = 100 //pixels
        val qrCodeContent = "$uid"
        val hints = hashMapOf<EncodeHintType, Int>().also { it[EncodeHintType.MARGIN] = 1 } // Make the QR code buffer border narrower
        val bits = QRCodeWriter().encode(qrCodeContent, BarcodeFormat.QR_CODE, size, size)
        return Bitmap.createBitmap(size, size, Bitmap.Config.RGB_565).also {
            for (x in 0 until size) {
                for (y in 0 until size) {
                    it.setPixel(x, y, if (bits[x, y]) Color.BLACK else Color.WHITE)
                }
            }
        }
    }
}